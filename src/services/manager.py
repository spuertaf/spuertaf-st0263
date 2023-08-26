from ..service import Service
from typing import Union
from .configs.contracts import list_files_service_pb2 as list_files_pb2
from .configs.contracts.list_files_service_pb2 import ListFilesResponse  
from .configs.contracts import list_files_service_pb2_grpc as list_files_pb2_grpc
from .configs.contracts import search_files_service_pb2 as search_files_pb2
from .configs.contracts.search_files_service_pb2 import SearchFilesResponse
from .configs.contracts import search_files_service_pb2_grpc as search_files_pb2_grpc
import logging


from typeguard import typechecked, TypeCheckError
from dynaconf.utils.boxing import DynaBox as ServiceSettings
from flask import Flask, request, Response
import grpc
from grpc._channel import _InactiveRpcError


class ManagerService(Service):
    
    def __init__(self, name:str = "manager-service", settings_file_name = "settings.json"):
        self.__name = name
        self.settings_file_name = settings_file_name
        self.__settings = self.check_existing_settings()
        self.__service = Flask(name)
        self.__request = None
    
    
    def check_existing_settings(self) -> Union[TypeCheckError,FileNotFoundError, ValueError, ServiceSettings]:
        return super().check_existing_settings(
            settings_file_name = self.settings_file_name, 
            service_type= self.__name
        )
    
    
    #checkear que existan response settings OK status y ERROR status
    def validate_config(self) -> Union[ValueError, None]:
        ...
    
    
    def check_request(self, end_point_route:str) -> Union[ValueError, AssertionError, None]:
        @self.__service.before_request
        def check_json():
                json_request:dict = request.get_json()
                if json_request is None:
                    raise ValueError()
                expected_arguments:list = self.__settings.get("end-points")[end_point_route]
                received_arguments = list(json_request.keys())
                assert len(set(expected_arguments) - set(received_arguments)) == 0, f"{expected_arguments} where expected; got {received_arguments}."
                recognized_services = self.__settings.get("services")
                #checkear que el servicio que se pone en la peticion se encuentra en la lista de servicios reconocidos
                requested_service:str = json_request.get("service")
                assert requested_service.lower() in recognized_services, f"Service {requested_service} is not a valid service to request."
                self.__request = json_request
    
    
    def make_request(self, response:Response) -> None:
        request = self.__request
        
        if request is None:
            return  
        
        requested_service:str = request["service"]
        print(requested_service)
        recognized_services:list = self.__settings.get("services")
        service_response: Union[None, ListFilesResponse, SearchFilesResponse] = None
        if requested_service == recognized_services[0]:
            #list-files
            grpc_connection = grpc.insecure_channel(self.__settings.get("redirect").get(recognized_services[0]))
            grpc_stub = list_files_pb2_grpc.ListFilesServiceStub(grpc_connection)
            list_files_request = list_files_pb2.ListFilesRequest()
            list_files_response:ListFilesResponse = grpc_stub.make_response(list_files_request)
            service_response:ListFilesResponse = list_files_response 
            
        elif requested_service == recognized_services[1]:
            #search-files
            grpc_connection = grpc.insecure_channel(self.__settings.get("redirect").get(recognized_services[1]))
            grpc_stub = search_files_pb2_grpc.SearchFilesStub(grpc_connection)
            search_files_request = search_files_pb2.SearchFilesRequest(file_to_search_pattern=self.__request["arguments"])
            search_files_response:SearchFilesResponse =  grpc_stub.make_response(search_files_request)
            service_response:SearchFilesResponse = search_files_response
        
        response.data = f"{service_response.files}"
        response.status = service_response.status_code
    

    @typechecked
    def create_end_point(
        self,
        end_point_route:str,
        end_point_function:callable,
        response: Response
    ) -> Union[None, TypeCheckError, Response]:
        @self.__service.route(end_point_route)
        def handle_request():
            end_point_function(response)
            return response
        
    
    def act_on_error(self, response:Response) -> Response:
        @self.__service.errorhandler(Exception)
        def handle_exception(error):
            response.data = str(error)
            response.status = self.__settings.get("response")["ERROR-status"]
            return response
    
    
    def act_on_grpc_error(self, response:Response) -> Response:
        @self.__service.errorhandler(_InactiveRpcError)
        def handle_grpc_error(error):
            response.data = f"{self.__request['service']} service inactive"
            response.status = self.__settings.get("response")["ERROR-status"]
            return response
    
    
    def act_on_kafka_error(self, response:Response):
        ...
    
    
    def execute(self):
        self.__service.run()
    
    
    def get_name(self):
        return self.__name
            
            
    def get_settings(self) -> ServiceSettings:
        return self.__settings        
            
            
    def get_service(self) -> Flask:
        return self.__service
    
    
    def get_request(self) -> dict:
        return self.__request
    

if __name__ == "__main__":
    m = ManagerService()
    r = Response()
    print(m.get_request())
    m.check_request("/list-files")
    m.create_end_point("/list-files",m.make_request,r)
    m.act_on_grpc_error(r)
    m.act_on_error(r)
    m.get_service().run()
    