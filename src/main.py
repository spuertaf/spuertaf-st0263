import logging
from argparse import ArgumentParser
from .adapter import Adapter

from flask import Response

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
argument_parser = ArgumentParser()
argument_parser.add_argument('--service')
response = Response()
adapter = Adapter()
command_line_arguments = argument_parser.parse_args()
built_service = adapter.build(
    command_line_arguments.service,
    response
)
built_service.execute()


