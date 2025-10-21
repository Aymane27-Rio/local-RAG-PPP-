from fastapi import FastAPI, Body

app = FastAPI(title="Chat Service", version="1.0")

conversations = {}

@app.post("/add")
def add_message(pdf_id: str = Body(...), role: str = Body(...), message: str = Body(...)):
    if pdf_id not in conversations:
        conversations[pdf_id] = []
    conversations[pdf_id].append({"role": role, "content": message})
    return {"count": len(conversations[pdf_id])}

@app.get("/get/{pdf_id}")
def get_conversation(pdf_id: str):
    return conversations.get(pdf_id, [])
