# User\Referrals app

[![python](https://img.shields.io/badge/python-3.10_-blue?style=flat-square)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-0.109.0-critical?style=flat-square)](https://fastapi.tiangolo.com/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.25-critical?style=flat-square)](https://www.sqlalchemy.org//)
[![alembic](https://img.shields.io/badge/alembic-1.13.1_-violet?style=flat-square)](https://alembic.sqlalchemy.org//)
[![redis](https://img.shields.io/badge/aioredis-2.0.1-violet?style=flat-square)](https://alembic.sqlalchemy.org//)


## Описание

<details>
<summary><b>ЗАДАНИЯ:</b></summary>

- регистрация и аутентификация пользователя;
- аутентифицированный пользователь должен иметь возможность создать или удалить свой реферальный код. 
- Одновременно может быть активен только 1 код. 
- При создании кода обязательно должен быть задан его срок годности;
- возможность получения реферального кода по email адресу реферера;
- возможность регистрации по реферальному коду в качестве реферала;	
- получение информации о рефералах по id реферера;
- UI документация (Swagger/ReDoc).

Стек:
- Fastapi
- SQLAlchemy(async)
- Alembic(async)
- Aioredis
- Postgresql(via asyncpg)
- Pydantic

Реализовано:
- Архитектурный паттерн DDD
- Код стилизован с помощью black
- Полный асинк
- Все круды для работы с моделями
- Авторизация JWT
- Все ручки для работы с реф.кодом и для удаления\редактирования юзера доступны только после авторизации
- Кешированы все основные операции


</details>


## Для запуска проекта

- Cоздать и активировать виртуальное окружение
- Клонировать репозиторий и перейти в него
- python -m pip install --upgrade pip
- pip install -r requirements.txt
- Создать .env по примеру .env_example
- Поднять локально Redis
- Выполнить миграции(alembic upgrade head)
- Запустить проект:

```
cd src
uvicorn runner:app --port 5555 --reload
или запустить main.py
```
Запустить сваггер:
```
http://127.0.0.1:5555/docs
```

## Для запуска проекта в докере

- Вписать в .env_prod данные почты
- перейти в директорию проджекта и ввести команду:
```
docker compose up --build
```