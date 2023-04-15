from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")
