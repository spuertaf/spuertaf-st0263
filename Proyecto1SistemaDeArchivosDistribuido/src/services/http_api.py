"""
JSON petition = {
    'command' : ,
    'file' : ,
}
"""

from ..utils.index_table import IndexTable
from typing import Union
import os

from flask import Flask, Response, request

class HttpApiService:
    def __init__(
        self,
        data_nodes_table: IndexTable, 
        name:str = "http-service"
    ):
        self.name = name
        self.__data_nodes_table: IndexTable = data_nodes_table
        self.__service = Flask(self.name)
        self.__request: Union[None, dict]  = None
        
    
    def validate_request(self) -> None:
        @self.__service.before_request
        def check_request_json():
            json_request:dict = request.get_json()
            match request.path.upper():
                case "/GET":
                    assert json_request["file_name"], f'Expected {{"command": "GET", "file_name": ...}} got {json_request}' 
                case "/PUT":
                    assert json_request["file_path"], f'Expected {{"command": "PUT", "file_path": ...}} got {json_request}'
                case "/SEARCH":
                    assert json_request["regex"], f'Expected {{"command": "SEARCH", "regex": ...}} got {json_request}'
                case "/LIST":
                    ...
                case _:
                    raise ValueError(f'Command {json_request["command"]} not supported!')
            self.__request = json_request
            
    
    
    def act_on_error(self, response: Response) -> None:
        @self.__service.errorhandler(Exception)
        def handle_exceptions(error):
            response.data = str(error)
            response.status = os.environ["ERROR-status"]
            return response
    
        
    def handle_put(self, response: Response):
        ...
        return response
        
        
    def handle_get(self, response: Response):
        ...
         
        
    def handle_search(self, response: Response):
        @self.__service.route("/SEARCH", methods=["GET"])
        def _search_regex():
            regex:str = self.__request["regex"]
            nodes_with_file:list[str] = self.__data_nodes_table.search_file(regex)
            ### revisar repeticion
            response.data = str(nodes_with_file)
            response.status = os.environ["OK-status"]
            ###
            return response

    
    def handle_list(self, response: Response):
        @self.__service.route("/LIST", methods=["GET"])
        def _list_data_nodes():
            regex:str = '.*'
            nodes_with_file:list[str] = self.__data_nodes_table.search_file(regex)
            ### revisar repeticion
            response.data = str(nodes_with_file)
            response.status = os.environ["OK-status"]
            ###
            return response
    
    
    def build(self, response: Response):
        self.validate_request()
        self.act_on_error(response)
        self.handle_search(response)
        self.handle_list(response)
        self.__service.run(
            host='0.0.0.0', port=8080
        ) # host y port
       
        
if __name__ == "__main__":
    data_nodes_table = IndexTable()
    service = HttpApiService(data_nodes_table)
    response = Response()
    service.build(response)

    
        