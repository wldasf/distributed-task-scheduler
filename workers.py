import pika
import json
import threading
import datetime
import time
from models import Task, SessionMaker

task_assignments = {}
lock = threading.Lock()

def process_task(task_data, worker_id, task_id):
    print(f" [{worker_id}] Processing task {task_id}")

    session = SessionMaker()
    task = session.query(Task).filter_by(task_id=task_id).first()
    if task:
        task.status = 'in-progress'
        task.worker_id = worker_id
        task.started_at = datetime.datetime.now(datetime.UTC)
        session.commit()
    session.close()

    time.sleep(2)

    session = SessionMaker()
    task = session.query(Task).filter_by(task_id=task_id).first()
    if task:
        task.status = 'completed'
        task.completed_at = datetime.datetime.now(datetime.UTC)
        session.commit()
    session.close()

    print(f" [{worker_id}] Completed task {task_id}")

def worker_function(worker_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True, arguments={'x-max-priority': 10})
    channel.basic_qos(prefetch_count=1)
    
    def callback(ch, method, properties, body):
        message = json.loads(body)
        task_id = task['task_id']
        task_data = message['data']
        process_task(task_data, worker_id, task_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print(f" [{worker_id}] Waiting for tasks.")
    channel.start_consuming()

if __name__ == '__main__':
    NUM_WORKERS = 3
    workers = []
    for i in range(NUM_WORKERS):
        worker_id = f"worker-{i}"
        worker_thread = threading.Thread(target=worker_function, args=(worker_id,), daemon=True)
        worker_thread.start()
        workers.append(worker_thread)
        print(f"Started {worker_id}")

    try:
        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        print("Shutting down workers...")
