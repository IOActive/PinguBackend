import json
import pika
from django.conf import settings 



def get_queue_element(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.QUEUE_HOST))
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue=queue_name)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return False, json.loads(body)
    else:
        return True, {}
    
def read_queue_elements(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.QUEUE_HOST))
    msgs = []
    while True:
        chl = connection.channel()
        method_frame, header_frame, body = chl.basic_get(queue=queue_name)
        if method_frame:
            print("body : ", body)
            msgs.append(body.decode('utf-8'))
        else:
            print("No more messages returned")
            connection.close()
            break
    
    json_object = json.loads("{}")
    json_object['messages'] = msgs
    if len(msgs) > 0:
        return False, json_object
    else:
        return True, json_object
    

def queue_exists(queue_name):
    parameters = pika.ConnectionParameters(host=settings.QUEUE_HOST)
    conn = pika.BlockingConnection(parameters=parameters)
    channel = conn.channel()
    try:
        channel.queue_declare(queue=queue_name, passive=True)
        conn.close()
        return True
    except:
        conn.close()
        return False


def create_queue(queue_name):
    parameters = pika.ConnectionParameters(host=settings.QUEUE_HOST)
    conn = pika.BlockingConnection(parameters=parameters)
    channel = conn.channel()
    try:
        channel.exchange_declare(exchange='src', durable=True)
        channel.queue_declare(queue=queue_name)
        channel.queue_bind(exchange='src', queue=queue_name)
        conn.close()
    except:
        conn.close()


def publish(queue_name, body):
    parameters = pika.ConnectionParameters(host=settings.QUEUE_HOST)
    conn = pika.BlockingConnection(parameters=parameters)
    channel = conn.channel()
    channel.basic_publish(exchange='src',
                          routing_key=queue_name,
                          body=body.encode('utf-8'))
    conn.close()


def get_channel():
    parameters = pika.ConnectionParameters(host=settings.QUEUE_HOST)
    conn = pika.BlockingConnection(parameters=parameters)
    channel = conn.channel()
    return channel
