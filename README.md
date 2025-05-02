 # API для социальной сети Yatube

REST API для блоговой платформы с возможностью публикации постов, подписки на авторов и комментирования.

## 📌 Стек технологий

- Python 3.9
- Django 3.2
- Django REST Framework 3.12
- Djoser (аутентификация)
- Simple JWT (токены)

## 🚀 Как запустить проект

1. Клонировать репозиторий и перейти в него:
```bash
git clone https://github.com/al3eon/api_final_yatube.git
cd api_final_yatube
```
2. Создать и активировать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
# venv\Scripts\activate   # Для Windows
python3 -m pip install --upgrade pip
```
3. Установить зависимости:
```bash
pip install -r requirements.txt
```
4. Выполни миграции:
```bash
python3 manage.py migrate
```
5. Запустить сервер:
```bash
python3 manage.py runserver
```

 ## 📚 Документация API
После запуска проекта документация будет доступна по адресу:

http://127.0.0.1:8000/redoc/ (Redoc)

## Автор
[al3eon](https://github.com/al3eon) - разработчик проекта
