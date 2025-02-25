import os

import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.routes import auth

app = FastAPI()

app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key="eajhageaufhgueagf")


@app.get("/")
def read_root():
    return {"message": "FastAPI running on Cloud Run"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
