#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import os
import io

import pika
import newick

import newick_io
import newick_io.to_database


print("Coucou ! (from print)")
sys.stdout.write("Coucou ! (from sys.stdout.write)")
sys.stdout.flush()


# Parse CLOUDAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url_str)



def aPrintingFunction(ch, method, properties, body):
    print("aPrintingFunction has been called !")
    print(properties)
    print(body)
    return

def theCallbackFunction(ch, method, properties, body):
    print("inside theCallbackFunction")
    
    with io.open('the_example_newick_tree.tre', encoding='utf8') as fp:
      trees = newick.load(fp)
      
      # -> postgresql database
      newick_io.to_database.save_to_postgresql(trees[0], os.environ.get('DATABASE_URL'))
    
    # datas are ready inside the postgresql database : send a response back to NodeJS
    the_connection = pika.BlockingConnection(params)
    the_channel = the_connection.channel()
    #the_channel.queue_declare(queue='myQueue4', durable=False)
    the_channel.basic_publish(exchange='', routing_key='myQueue4', body='the body')
    return


print("connection …")
connection = pika.BlockingConnection(params) # Connect to CloudAMQP
print("channel …")
channel = connection.channel() # start a channel
channel.queue_declare(queue='myQueue4') # Declare a queue

print("channel.basic_consume …")
channel.basic_consume('myQueue4', theCallbackFunction, auto_ack=True) # auto_ack=True <- if 'myQueue' does not exists, do not sent a 404 error

print("channel.start_consuming …")
channel.start_consuming() # start consuming (blocks)

print("connection.close …")
connection.close()
