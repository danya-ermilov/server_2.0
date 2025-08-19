from fastapi import FastAPI

from app.routers import admins, carts, products, users

app = FastAPI()


app.include_router(users.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(admins.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
