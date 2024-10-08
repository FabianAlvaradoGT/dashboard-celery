from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Task(BaseModel):
    id: int
    name: str
    status: str = "Pending"
    progress: int = 0


tasks = [
    Task(id=1, name="Process Images"),
    Task(id=2, name="Generate Report"),
    Task(id=3, name="Send Notifications"),
]


@app.get("/tasks")
async def get_tasks():
    return tasks


@app.post("/tasks/{task_id}/execute")
async def execute_task(task_id: int):
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        task.status = "Running"
        task.progress = 0
        # Simulate task execution
        for _ in range(10):
            await asyncio.sleep(0.5)
            task.progress += random.randint(5, 15)
            if task.progress > 100:
                task.progress = 100
        task.status = "Completed"
        return {"message": f"Task {task_id} executed successfully"}
    return {"message": "Task not found"}, 404


@app.get("/stats")
async def get_stats():
    total = len(tasks)
    running = sum(1 for task in tasks if task.status == "Running")
    completed = sum(1 for task in tasks if task.status == "Completed")
    pending = total - running - completed
    return {
        "total": total,
        "running": running,
        "completed": completed,
        "pending": pending,
    }
