# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import modal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
stub = modal.Stub("form_generator")

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
origins = [
    "https://chat.openai.com",
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


items = {}


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


# Create a custom image with the required dependencies installed
# image = modal.Image.debian_slim().pip_install()
image = modal.Image.debian_slim().pip_install()


@stub.asgi(image=image)
def fastapi_app():
    return app


# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     item_id = len(items) + 1
#     items[item_id] = item
#     return item


# @app.get("/items/", response_model=List[Item])
# async def read_items(skip: int = 0, limit: int = 10):
#     return list(items.values())[skip : skip + limit]


# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: int):
#     item = items.get(item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item


# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: int, item: Item):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     items[item_id] = item
#     return item


# @app.delete("/items/{item_id}", response_model=Item)
# async def delete_item(item_id: int):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item = items.pop(item_id)
#     return item
