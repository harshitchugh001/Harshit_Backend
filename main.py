from database import client
from fastapi import APIRouter
from fastapi import FastAPI
from routes import route


app = FastAPI()



if client.server_info():
    print("Connected to MongoDB Atlas")


app.include_router(route.router)


