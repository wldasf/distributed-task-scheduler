import pika
import json
import uuid
from models import Task, Session

def submit_task(task_data, priority=0):
    if not 0 <= priority <= 10:
        raise ValueError("Priority must be between 0 and 10")

    session = Session()
    task = Task(
        task_id=str(uuid.uuid4()),
        priority=priority,
        status='pending',
        data=json.dumps(task_data)
    )
    session.add(task)
    session.commit()
    task_id = task.task_id
    session.close()

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True, arguments={'x-max-priority': 10})
    message = {
        'task_id': task_id,
        'data': task_data,
        'priority': priority
    }
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task),
        properties=pika.BasicProperties(
            delivery_mode=2,
            priority=priority
        )
    )
    print(f" [x] Sent task {task['task_id']}")
    connection.close()

if __name__ == '__main__':
    submit_task({"description": "High priority task"}, priority=10)
    submit_task({"description": "Low priority task"}, priority=1)
