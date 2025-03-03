import pika
import json
import threading
import time
from sqlalchemy.orm import Session
from models import Task, engine, Session as SessionMaker

NUM_WORKERS = 3
workers = [f"worker-{i}" for i in range(NUM_WORKERS)]
task_assignments = {}
lock = threading.Lock()

def process_task(task_data, worker_id):
    task_id = task_data['task_id']
    print(f" [{worker_id}] Processing task {task_id}")

    session = SessionMaker()
    task = session.query(Task).filter_by(task_id=task_id).first()
    if task:
        task.status = 'in-progress'
        task.worker_id = worker_id
        task.started_at = time.time()
        session.commit()
    session.close()

    time.sleep(2 + task_data['priority'])

    session = SessionMaker()
    task = session.query(Task).filter_by(task_id=task_id).first()
    if task:
        task.status = 'completed'
        task.completed_at = time.time()
        session.commit()
    session.close()

    print(f" [{worker_id}] Completed task {task_id}")
    with lock:
        del task_assignments[task_id]

def callback(ch, method, properties, body):
    task = json.loads(body)
    task_id = task['task_id']
    print(f" [Scheduler] Received task {task_id}")

    session = SessionMaker()
    db_task = Task(
        task_id=task_id,
        priority=task['priority'],
        status='pending'
    )
    session.add(db_task)
    session.commit()
    session.close()

    with lock:
        available_worker = workers[len(task_assignments) % NUM_WORKERS]
        task_assignments[task_id] = available_worker

    worker_thread = threading.Thread(target=process_task, args=(task, available_worker))
    worker_thread.start()

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_scheduler():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(" [Scheduler] Waiting for tasks. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__name__':
    start.scheduler()
