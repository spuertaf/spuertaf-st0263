from typing import Union
import logging
import json

import pika
from pika.exceptions import AMQPConnectionError

class RabbitMQConnector():
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    
    def __init__(self) -> None:
        if not self._initialized:
            self._initialized = True
    
        
    def establish_connection(self, host:str, port:int) -> Union[pika.BlockingConnection, AMQPConnectionError]:
            self.__connection =  pika.BlockingConnection(
                pika.ConnectionParameters(host=host, port = port)
            )
            return self
            
    
    def establish_channel(self):
        self.__channel = self.__connection.channel()
        return self
    

    def publish(self, queue_name:str, message:str):
        self.__channel.basic_publish(
            exchange='', 
            routing_key=queue_name, 
            body=message,
            properties= pika.BasicProperties(content_type='text/plain', delivery_mode=1)
        )
        logging.info(f"New message \'{message}\' published to queue \'{queue_name}\'\n")
    
    
    def consume(self, queue_name:str) -> list:
        """Consumes messages from a given queue and returns a list of them.

        Args:
            queue_name (str): _description_

        Returns:
            list: _description_
        """
        def bytes_to_dict(messages:list) -> list:
            """Converts every position of a given bytes messages list to json 

            Args:
                messages (list): _description_

            Returns:
                list: _description_
            """
            return list(map(lambda message: json.loads(message.decode('utf-8').replace("'",'"')), messages))
        
        messages = []
        while True:
            method_frame, _, body = self.__channel.basic_get(queue_name)
            if method_frame:
                messages.append(body)
                self.__channel.basic_ack(method_frame.delivery_tag)
            else:
                break
        self.__channel.queue_purge(queue=queue_name) #delete all the messages in queue
        return bytes_to_dict(messages)
    
    
    """def close_connection(self):
        self.__connection.close()"""
        
    
if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    r = RabbitMQConnector()
    r.establish_connection("54.235.255.168",5672)
    r.establish_channel()
    r.publish("pending.list_files", "{'request_id': 'e5cedc902f760d4faac8ea4bf79bf6e45ea7c32b3c5277c2b77c814a8edd2894', 'service': 'list-files', 'arguments': '*'}")
    #print(r.consume("pending.list_files"))
    