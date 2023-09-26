import logging
from argparse import ArgumentParser
from .patterns.rabbitmq import RabbitMQConnector
from src.patterns.adapter import Adapter

from flask import Response

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
argument_parser = ArgumentParser()
argument_parser.add_argument('--service')
rabbitmq = RabbitMQConnector()
response = Response()
adapter = Adapter()
command_line_arguments = argument_parser.parse_args()
built_service = adapter.build(
    command_line_arguments.service,
    rabbitmq,
    response
)
built_service.execute()


