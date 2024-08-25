# Приложение для Благотворительного фонда поддержки котиков QRKot

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Технологический стек
- Python 3.9.10
- FastAPI 0.78.0
- SQLAlchemy 1.4.36
- uvicorn 0.17.6
- Alembic 1.7.7
- FastAPI_users 10.0.4

## Основные функции

- **Создание благотворительных проектов**: Администрация может открывать благотворительные проекты с описанием целевого назначения проекта и требуемой суммы

- **Внесение пожертвований**: Зарегистрированные пользователи могу вносить пожертвования. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму

- **Система управления пользователями**: Возможность регистрации новых пользователей и их аутентификация с использованием JWT-тоеконов


## Локальное развертывание проекта

- **Клонировать репозиторий**

```
git clone git@github.com:ikhit/cat_charity_fund.git
```

- **Перейти в директорию проекта**

- **Создать виртуальное окружение, активировать его и установить зависимости**

```
python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt
```

- **Создать файл .env и заполнить его данными. Пример указан в файле .env.example**

- **Применить миграции**

```
alembic upgrade head
```

- **Запустить приложение**

```
uvicorn app.main:app
```

- **Документация к проекту будет доступна по адресу**

```
http://127.0.0.1:8000/docs
```

## Автор прокта 

**Игорь Хитрик - [ikhit](https://github.com/ikhit)**

