import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tasks_router import router as task_router
from users_router import router as user_router
from oauth2_jwt import router as oauth2_jwt_router
from database import create_db as metadata_db_migrations


app = FastAPI(
    title='Task Challenge', description='Technical Challenge - Fastapi', docs_url='/swagger-ui', 
    version='1.0.0', summary='Task API and auth using oauth2-jwt.')

metadata_db_migrations()  # create all database migrations config.

origins = [
    "http://localhost:8000",
    "http://localhost:8080/swagger-ui",
]

app.add_middleware(CORSMiddleware, 
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

### ROUTERS
app.include_router(oauth2_jwt_router)  # FROM OAUTH2 JWT AUTHENTICATED - AUTHORIZED
app.include_router(user_router)
app.include_router(task_router)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
