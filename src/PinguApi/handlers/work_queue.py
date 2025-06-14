# Copyright 2024 IOActive
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pika
from django.conf import settings 
from  pika.exceptions import ChannelError, ChannelClosedByBroker
from logging import getLogger



def get_queue_element(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.QUEUE_HOST))
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue=queue_name)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return False, json.loads(body)
    else:
        return True, {}
    
def read_queue_elements(queue_name: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.QUEUE_HOST))
        msgs = []
        while True:
            chl = connection.channel()
            method_frame, header_frame, body = chl.basic_get(queue=queue_name.lower())
            if method_frame:
                msgs.append(json.loads(body.decode('utf-8')))
            else:
                getLogger('PinguAPI').info("No more messages returned")
                connection.close()
                break
        if len(msgs) > 0:
            return False, msgs
        else:
            return True, msgs
        
    except ChannelClosedByBroker as e:
        #getLogger('PinguAPI').exception(e)
        return True, []
    

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
