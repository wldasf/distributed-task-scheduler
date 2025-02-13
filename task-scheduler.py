import queue
import threading
import time

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

def worker_function(task_queue):
    while True:
        try:    
            task = task_queue.get(timeout=1)
            if task:
                print(f"Worker thread {threading.current_thread().name}: Processing task {task['task_id']} - {task['description']}")
                task['status'] = "RUNNING"
                time.sleep(2)
                task['status'] = "COMPLETED"
                print(f"Worker thread {threading.current_thread().name}: Task {task['task_id']} completed.")
                task_queue.task_done()
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Worker thread {threading.current_thread().name} encountered an error: {e}")
            break

# Modified scheduler_function (snippet)
def scheduler_function(task_queue, num_workers):
    worker_index = 0
    task_order = list(task_queue.queue) # Get the tasks in the queue at the start
    for task_peek in task_order: # Iterate through the initial tasks
        worker_name = f"Worker-{worker_index + 1}"
        print(f"Scheduler: Assigning task {task_peek['task_id']} to {worker_name}")
        task_peek['assigned_to'] = worker_name
        worker_index = (worker_index + 1) % num_workers
    print("Created and started scheduler thread.") # Moved print here

if __name__ == "__main__":
    task1 = create_task(1, "Process user data")
    task2 = create_task(2, "Generate daily report")
    task3 = create_task(3, "Run weekly backups")
    task4 = create_task(4, "Clean up temp files")
    task5 = create_task(5, "Optimize database")

    submit_task(task_queue, task1)
    submit_task(task_queue, task2)
    submit_task(task_queue, task3)
    submit_task(task_queue, task4)
    submit_task(task_queue, task5)

    num_workers = 3
    workers = []
    for i in range(num_workers):
        thread = threading.Thread(target=worker_function, args=(task_queue,), name=f"Worker-{i+1}")
        workers.append(thread)
        thread.start()

    print(f"\nCreated and start {num_workers} worker threads.")

    scheduler_thread = threading.Thread(target=scheduler_function, args=(task_queue, num_workers), name="Scheduler")
    scheduler_thread.start()
    
    print("\nCreated and started scheduler thread.")

    time.sleep(7)
    print("\nMain thread finished waiting.")
