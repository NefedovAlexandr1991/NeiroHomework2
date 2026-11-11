from fastapi import FastAPI
from api.endpoint import ans, app
import uvicorn
from llm.llm import get_token, ask

#@app.post("/", summary="Answer")
#async def ans(prompt: str):
    #token = get_token(url, key)
    #response = ask(token, prompt, model="GigaChat-2")
    #return {"message": response.json()["choices"][0]["message"]["content"]}

if __name__ == "__main__":
    uvicorn.run("main:app")