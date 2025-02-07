def create_task(task_id, description):
    task = {
        "task_id": task_id,
        "description": description,
        "status": "PENDING"
    }
    return task

if __name__ == "__main__":
    task1 = create_task(1, "Process user data")
    task2 = create_task(2, "Generate daily report")

    print("Task 1:", task1)
    print("Task 2:", task2)

