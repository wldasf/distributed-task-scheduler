import pika
import json
import uuid

def submit_task(task_data, priority=0):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    task = {
            'task_id': str(uuid.uuid4()),
            'priority': priority,
            'data': task_data
    }

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
    print(f" [x] Sent task {task['task_id']}")

    connection.close()

if __name__ == '__main__':
    submit_task({'type': 'example', 'payload': 'do something'}, priority=1)

