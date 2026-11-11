from fastapi import FastAPI, HTTPException
from llm.llm import get_token, ask
from pydantic import BaseModel, Field, constr, conint
import logging

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', encoding='utf-8')
app = FastAPI()

class Prompt(BaseModel):
    """Модель для создания новой задачи."""
    text: str = Field(
        min_length=3,           # Минимальная длина строки
        max_length=1000,         # Максимальная длина строки
        description="Промпт к модели",  # Описание для документации
        examples=["Какая погода в Москве?"]  # Пример значения
    )

@app.post("/")
async def ans(prompt: Prompt):
    #token = get_token(url, key)
    response = ask(prompt.text, model="GigaChat-2", temperature = 0.3)
    #print(response.status_code)
    if response.status_code == 400 or response.status_code == 401 or response.status_code == 403 or response.status_code == 404:
        logging.error(f'Произошла ошибка {response.status_code}')
        raise HTTPException(status_code=response.status_code, detail="Item not found 4xx")
    elif response.status_code == 500 or response.status_code == 501 or response.status_code == 502 or response.status_code == 503 or response.status_code == 504:
        logging.error(f'Произошла ошибка {response.status_code}')
        raise HTTPException(status_code=response.status_code, detail="Item not found 5xx")
    else:
        logging.info(f'Промпт отправлен {prompt.text}. Ответ получен {response.json()["choices"][0]["message"]["content"]}')
        return {"message": response.json()["choices"][0]["message"]["content"]}