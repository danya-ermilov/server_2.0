from fastapi import FastAPI

from app.routers import users
from app.routers import products


app = FastAPI()


app.include_router(users.router)
app.include_router(products.router)



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
