import queue
task_queue = queue.Queue()

def create_task(task_id, description):
    task = {
        "task_id": task_id,
        "description": description,
        "status": "PENDING"
    }
    return task

def submit_task(task_queue, task):
    task_queue.put(task)
    print(f"Task {task['task_id']} submitted to the queue.")

if __name__ == "__main__":
    task1 = create_task(1, "Process user data")
    task2 = create_task(2, "Generate daily report")
    task3 = create_task(3, "Run weekly backups")

    submit_task(task_queue, task1)
    submit_task(task_queue, task2)
    submit_task(task_queue, task3)

    print(f"\nTask queue size: {task_queue.qsize()}")
