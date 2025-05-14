import uvicorn
from Backend.main import app  # import the FastAPI app object

if __name__ == "__main__":
    uvicorn.run("Backend.main:app", host="127.0.0.1", port=8000, reload=True)