# FastAPI installer

### FastAPI - Uvicorn
pip install fastapi "uvicorn[standard]"

### JWT Auth
pip install python-multipart
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"

### Random generate secret key
openssl rand -hex 32

### ORM SqlAlchemy
pip install sqlalchemy

### Postgres Database Drive
pip install psycopg2-binary

### Environments config
pip install python-dotenv

### Engine (contry city state) info
pip install geocoder

### Async request client
pip install httpx

### PEP8 python standart code
pip install autopep8

### Generate requirements
pip freeze > requirements.txt
pip install -r requirements.txt

### Uvicorn run server in dev
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### App Structure
├── src
│   ├── models
│   │   ├── __init__.py
│   │   └── models.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── users_router.py
│   │   └── tasks_router.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── databases
│   │   ├── __init__.py
│   │   └── database.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── middleware.py
│   │   └── oauth2_jwt.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_api.py
│   ├── __init__.py
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .dockerignore
├── .env
├── requirements.txt
├── LICENSE
├── README.md
└── commands.md
