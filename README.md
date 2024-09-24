# fastapi_challenge_task
Technical Challenge - Fastapi

## ⚡ Use local with virtual environment.
1. Create dir:
   ```shell
   mkdir dirname && cd dirname
   ```
3. Clone repository:
   ```shell
   git clone https://github.com/dlibenp/fastapi_challenge_task.git
   ```
4. Create virtual environment:
   ```shell
   python3 -m venv venv
   ```
6. Init virtual environment:
   ```shell
   source venv/bin/activate
   ```
8. Install requirenment:
   ```shell
   pip install -r requirenment.txt
   ```

## ⚡ Run
```shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file=.env
```

## ⚡ Auth API
### Register endpoint
```shell
curl -X 'POST' 'http://localhost:8000/users/me/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "admin", "email": "admin@mail.com",
  "password": "admin"
}'
```

### Login endpoint
```shell
curl -X 'POST' 'http://localhost:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin@mail.com&password=admin&scope=&client_id=&client_secret='
```

### Me endpoint
```shell
curl -X 'GET' 'http://localhost:8000/users/me/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

## ⚡ User API
### Find users endpoint
```shell
curl -X 'GET' 'http://localhost:8000/api/v1/users/?limit=10&offset=0' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Find user endpoint
```shell
curl -X 'GET' 'http://localhost:8000/api/v1/users/<ID>' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Create user endpoint
```shell
curl -X 'POST' 'http://localhost:8000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "test", "email": "test@mail.com",
  "password": "test"
}'
```

### Update user endpoint
```shell
curl -X 'PUT' 'http://localhost:8000/api/v1/users/<ID>' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{ "is_active": false }'
```

### Delete user endpoint
```shell
curl -X 'DELETE' 'http://localhost:8000/api/v1/users/<ID>' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Find weather endpoint
```shell
curl -X 'GET' 'http://localhost:8000/api/v1/weather/?limit=10&offset=0' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Find tasks endpoint
```shell
curl -X 'GET' 'http://localhost:8000/api/v1/tasks/?limit=10&offset=0' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Find task endpoint
```shell
curl -X 'GET' 'http://localhost:8000/api/v1/tasks/<ID>' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Create task endpoint
```shell
curl -X 'POST' 'http://localhost:8000/api/v1/tasks/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "my task name",
  "description": "description about task",
  "status": "pending"
}'
```

### Update task endpoint
```shell
curl -X 'PUT' \
  'http://localhost:8000/api/v1/tasks/<ID>' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{ "status": "created" }'
```

### Delete task endpoint
```shell
curl -X 'DELETE' 'http://localhost:8000/api/v1/tasks/<ID>' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer <TOKEN>'
```

### Create User's task endpoint
```shell
curl -X 'POST' 'http://localhost:8000/api/v1/tasks/users/<USER-ID>' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{ "name": "task new",  
  "description": "description task",
  "status": "pending"
}'
```

### Find User's tasks endpoint
```shell
curl -X 'GET' 'http://localhost:8000/api/v1/tasks/users/<USER-ID>?limit=10&offset=0' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN>'
```

### ⚡ Test:
```shell
python -m unittest test/test_api.py
```

### ⚡ Create docker image and run:
1. ```shell
   docker build -t task-app .
   ```
2. ```shell
   docker run -d -p 8000:8000 task-app
   ```

### ⚡ Run docker-compose and show logs:
1. ```shell
   docker-compose up -d --build
   ```
2. ```shell
   docker-compose logs -f
   ```