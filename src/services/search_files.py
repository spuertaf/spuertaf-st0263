from ..interfaces.grpc_service import GrpcService
from typing import Union
from concurrent import futures
import logging
from ..scripts.utils import rename_2_current_OS
import os
from .configs.contracts import search_files_service_pb2_grpc
from ..patterns.rabbitmq import RabbitMQConnector
import json
from .configs.contracts.search_files_service_pb2 import SearchFilesRequest, SearchFilesResponse 
import fnmatch

from typeguard import typechecked, TypeCheckError
from grpc._server import _Server as GrpcServer
import grpc
from dynaconf.utils.boxing import DynaBox as ServiceSettings


class SearchFilesService(GrpcService):
    @typechecked
    def __init__(self, name:str = "search-files-service", settings_file_name:str = "settings.json"):
        self.__name = name
        self.settings_file_name = settings_file_name
        self.__settings = self.check_existing_settings()
        self.__service:GrpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    
    def check_existing_settings(self) -> Union[FileNotFoundError, ValueError, ServiceSettings]:
        return super().check_existing_settings(
            settings_file_name = self.settings_file_name, 
            service_type= self.__name
        )
        
    #añadir validaciones de response
    def validate_config(self) -> Union[ValueError, None]:
        end_points:Union[str, list] = self.__settings.get('end-points')
        if end_points is None:
            raise ValueError(f"A configuration for endpoints does not exist on settings file {self.settings_file_name}")
        if not isinstance(end_points, (str, list)):
            raise ValueError(f"End points must be string or list not {type(end_points)}")
        data_folder:str = self.__settings.get('data-folder-name')
        if data_folder is None:
            raise ValueError(f"A data folder is not specified in settings file {self.settings_file_name}")
        if not isinstance(data_folder, str):
            raise ValueError(f"Data folder name must be string not {type(end_points)}")
        if not os.path.exists(f"src\{data_folder}"):
            raise ValueError(f"Data folder {data_folder} does not exist")
        if not os.path.isdir(f"src\{data_folder}/"):
            raise ValueError("Data folder must be a directory")
        #verificar que parametros de la respuesta si existen
        #verificar que servidor de kafka si existe
        
    
    def get_mi_ip(self) -> str:
        self.__public_ip = super().get_mi_ip()
    
    
    def add_server_functions(self):
        #añadir las funcionalidades de la clase al servidor
        search_files_service_pb2_grpc.add_SearchFilesServicer_to_server(SearchFilesService(), self.__service)
    
    
    def conf_rabbitmq_connection(self, rabbitmq_connector:RabbitMQConnector):
        rabbitmq_connector.establish_connection(
            host=self.__settings.get("rabbitmq").get("server"),
            port=self.__settings.get("rabbitmq").get("port")
    
        )
        rabbitmq_connector.establish_channel()
        self.__rabbitmq_connector = rabbitmq_connector
    
    
    def send_email(self, receiver: str, pending_request: str, request_id: str, response: str):
        super().send_email(receiver, pending_request, request_id, response)
    
    
    #### revisar esto
    def handle_pending_requests(
        self, 
        rabbitmq_connector:RabbitMQConnector,
        queue_name_2_publish:str,
        pending_requests:list 
    ) -> list:
        if len(pending_requests) == 0:
            return pending_requests
        
        pending_request:json = pending_requests[0]
        pending_request_reponse = self.make_response(
            SearchFilesRequest(file_to_search_pattern=pending_request["arguments"]),
            context="rabbitmq"
        )
        pending_request['response'] = pending_request_reponse.files
        
        self.send_email(
            receiver=pending_request["email"],
            pending_request=pending_request["arguments"],
            request_id=pending_request["request_id"],
            response = pending_request_reponse.files
        )
        pending_requests.pop(0) #the list gets updated
        return self.handle_pending_requests(rabbitmq_connector, queue_name_2_publish, pending_requests)
    
    
    ####revisar esta funcion
    def on_startup(
        self,
        on_startup_function:callable
    ) -> None:
        super().on_startup(
            rabbitmq_connector=self.__rabbitmq_connector, 
            queue_name_2_consume = self.__settings.get("rabbitmq").get("pending-requests-topic"),
            queue_name_2_publish = self.__settings.get("rabbitmq").get("resolved-pending-requests-topic"),
            on_startup_function=on_startup_function
        )
    
    
    @typechecked
    def create_end_point(self, listening_port:str) -> Union[TypeCheckError, None]:
        #añado puertos de escucha a peticiones
        self.__service.add_insecure_port(listening_port)
        logging.info(f"Server now listening on IP {self.__public_ip} Port {listening_port}\n")
        
        
    def make_response(self, request:SearchFilesRequest, context) -> SearchFilesResponse:
        logging.info(f"New request received from peer: {context}")
        data_folder_path = rename_2_current_OS(f"src\{self.__settings.get('data-folder-name')}")
        all_files_in_folder = [file for file in os.listdir(data_folder_path) if os.path.isfile(os.path.join(data_folder_path, file))]
        search_pattern = request.file_to_search_pattern
        found_files = [file for file in all_files_in_folder if fnmatch.fnmatch(file, search_pattern)]
        logging.info(f"Requested {search_pattern} | Found Files: {found_files}\n")
        return SearchFilesResponse(
            status_code=self.__settings.get("response")["OK-status"], 
            files=found_files, 
        )
    
    
    def execute(self):
        self.__service.start()
        self.__service.wait_for_termination()
    
    
    def get_name(self) -> str:
        return self.__name  
    
    
    def get_settings(self) -> ServiceSettings:
        return self.__settings
    
    
    def get_service(self) -> GrpcServer:
        return self.__service
    

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    r = RabbitMQConnector()
    search_files = SearchFilesService()
    search_files.add_server_functions()
    search_files.conf_rabbitmq_connection(r)
    search_files.on_startup(search_files.handle_pending_requests)
