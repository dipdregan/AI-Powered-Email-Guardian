from fastapi import FastAPI

app = FastAPI()

# Mock data for users
users = [
    {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
]

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI example!"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return user
    return {"message": "User not found"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
