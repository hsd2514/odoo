from fastapi import FastAPI

app = FastAPI()

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}
