import uvicorn

from fastapi import FastAPI


web_app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        "main:web_app",
        host="localhost",
        port=8000,
    )
