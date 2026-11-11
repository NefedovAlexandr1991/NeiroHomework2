from gigachat import GigaChat
import os
import uuid
import requests
import json
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError
from cache.cache import ttl_cache
from dotenv import load_dotenv


url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
load_dotenv()
key = os.getenv('key')

def get_token(url, key):
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {key}"
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    token = json.loads(response.text)
    return token["access_token"]

@ttl_cache(ttl_seconds=600)
def ask(prompt, model="GigaChat-2", temperature=0.3):
    token = get_token(url, key)
    API_URL = "https://api.giga.chat/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты помощник. Отвечай коротко и по существу."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }
    r = requests.post(API_URL, headers=headers, json=body, verify=False, timeout=60)
        #r.raise_for_status()
    return r
    #except HTTPError as http_err:
        #logging.error(f"HTTP error occurred: {http_err} - Статус: {r.status_code}")
    # Здесь можно реализовать специфическую логику для разных HTTP-ошибок
    #except Timeout as timeout_err:
        #logging.error(f"Request timed out: {timeout_err} - Сервер не ответил")
        # Повторный запрос с увеличенным таймаутом
    #except ConnectionError as conn_err:
        #logging.error(f"Connection error: {conn_err} - Проверьте доступность сервера")
        # Логирование и, возможно, повтор запроса с задержкой
    #except RequestException as req_err:
        #logging.error(f"Unexpected error occurred: {req_err}")
        # Общая обработка для всех остальных ошибок библиотеки requests
    #except Exception as e:
        #logging.error(f"An unexpected error occurred: {e}")
    #else:
        #logging.info("Запрос успешно выполнен")
        # Обработка успешных результатов
    #finally:
        #logging.info("Завершение операции")