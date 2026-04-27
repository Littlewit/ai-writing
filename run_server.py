import uvicorn
from api import app

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="localhost", port=8000, log_level="info")