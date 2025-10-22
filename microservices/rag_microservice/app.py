from fastapi import FastAPI, Body
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableSequence

app = FastAPI(title="RAG Service", version="1.0")

@app.get("/")
def root():
    return {"message": "RAG Service is running"}


@app.post("/build-vector-db")
async def build_vector_db(content: list[str] = Body(...)):
    """Create a Chroma DB from a list of document strings."""
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        chunks = text_splitter.create_documents(content)

        db = Chroma.from_documents(
            documents=chunks,
            embedding=OllamaEmbeddings(model="znbang/bge:small-en-v1.5-q8_0"),
            collection_name="local-rag"
        )
        return {"status": "success", "chunk_count": len(chunks)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query")
async def query(question: str = Body(...)):
    """Ask a question to the RAG chain."""
    try:
        llm = ChatOllama(model="deepseek-r1:1.5b")
        db = Chroma(collection_name="local-rag", embedding_function=OllamaEmbeddings(model="znbang/bge:small-en-v1.5-q8_0"))

        query_prompt = PromptTemplate(
            input_variables=["question"],
            template="""Answer the question based only on the provided context.
            If you cannot find the answer, say so.
            Question: {question}"""
        )

        retriever = MultiQueryRetriever.from_llm(db.as_retriever(), llm, prompt=query_prompt)

        main_prompt = ChatPromptTemplate.from_template(
            "Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        )

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | main_prompt
            | llm
            | StrOutputParser()
        )

        result = chain.invoke(question)
        return {"answer": result}

    except Exception as e:
        return {"error": str(e)}
