from fastapi import FastAPI, Body

app = FastAPI(title="Chat Service", version="1.0")

# In-memory message store
chat_history = []


@app.get("/")
def root():
    return {"message": "Chat Service is running"}


@app.post("/save")
def save_message(user: str = Body(...), message: str = Body(...)):
    """
    Save a chat message from either user or assistant.
    """
    chat_history.append({"user": user, "message": message})
    return {"status": "saved", "count": len(chat_history)}


@app.get("/history")
def get_history():
    """
    Retrieve all stored chat messages.
    """
    return chat_history


@app.post("/clear")
def clear_history():
    """
    Optional: clear all chat messages (for debugging or new session).
    """
    chat_history.clear()
    return {"status": "cleared", "count": 0}
