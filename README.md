   # ***fastapi_challenge_task***
Technical Challenge - Fastapi

## Objective:
● Create an API with the endpoints below in the other section.\
● Use a public repo in github and share it with the person that sent you the
challenge.\
● For the above endpoints implements oauth2 for the authentication.\
● For every call made to any endpoint store the ip address, country that belongs to
this ip address and the state of the weather in this country.\
● For the weather use an api that gives you this information.\
● Use Postgres as a database engine.\
● prepare a Dockerfile or Compose tu test locally your solution.\
● Build a READM.md file with all the documentation including api doc, postman files,
json files and so on.

______________________________
## Endpoints a desarrollar:

> ***Create a New Task***
> > HTTP Method: POST
> > 
> > Endpoint: /tasks
> >
> > Functionality:
> > > Accepts a JSON body with a taskName and description.\
> > > Stores the task with a unique taskId, a taskName, description, and status (default
status: "pending").\
> > > Returns the created task as a JSON response.
>
> ***Get All Tasks***
> > HTTP Method: GET
> > 
> > Endpoint: /tasks
> >
> > Functionality:
> > > Retrieves all tasks from.\
> > > Returns a JSON array of tasks.
>
> ***Get a Single Task by ID***
> > HTTP Method: GET
> > 
> > Endpoint: /tasks/{taskId}
> >
> > Functionality:
> > > Retrieves a task by its taskId.\
> > > Returns the task as a JSON response if it exists, otherwise returns a 404 error.
>
> ***Update a Task***
> > HTTP Method: PUT
> > 
> > Endpoint: /tasks/{taskId}
> >
> > Functionality:
> > > Accepts a JSON body with updated values (taskName, description, status).\
> > > Updates the task if it exists.\
> > > Returns the updated task as a JSON response.
>
> ***Delete a Task***
> > HTTP Method: DELETE
> > 
> > Endpoint: /tasks/{taskId}
> >
> > Functionality:
> > > Deletes a task by taskId.\
> > > Returns a success message or a 404 error if the task doesn't exist.

***************************

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

-------------------------

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
```diff
- python -m unittest test/test_api.py
```

### ⚡ Create docker image and run:
1. ```diff
   + docker build -t task-app .
   ```
2. ```diff
   + docker run -d -p 8000:8000 task-app
   ```

### ⚡ Run docker-compose and show logs:
1. ```diff
   @@ docker-compose up -d --build @@
   ```
2. ```diff
   @@ docker-compose logs -f @@
   ```
