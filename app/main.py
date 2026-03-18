from fastapi import FastAPI
from .routes import router

app = FastAPI(title="FASTAPI Demo")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CollegeDB API"}