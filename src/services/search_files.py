from ..service import Service
from typing import Union
from concurrent import futures
import logging
from ..utils import check_current_OS
import os
from .configs.contracts import search_files_service_pb2_grpc
from .configs.contracts.search_files_service_pb2 import SearchFilesRequest, SearchFilesResponse 
import fnmatch

from typeguard import typechecked, TypeCheckError
from grpc._server import _Server as GrpcServer
import grpc
from dynaconf.utils.boxing import DynaBox as ServiceSettings


class SearchFilesService(Service):
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
    
    
    def on_startup(self):
        self.__public_ip = super().on_startup()
    
    
    def add_server_functions(self):
        #añadir las funcionalidades de la clase al servidor
        search_files_service_pb2_grpc.add_SearchFilesServicer_to_server(SearchFilesService(), self.__service)
         
    
    @typechecked
    def create_end_point(self, listening_port:str) -> Union[TypeCheckError, None]:
        #añado puertos de escucha a peticiones
        self.__service.add_insecure_port(listening_port)
        logging.info(f"Server now listening on IP {self.__public_ip} Port {listening_port}\n")
        
        
    def make_response(self, request:SearchFilesRequest, context) -> SearchFilesResponse:
        logging.info(f"New request received from peer: {context.peer()}")
        current_OS = check_current_OS()
        if current_OS == "Linux":
            data_folder_path = f"src/{self.__settings.get('data-folder-name')}"
        elif current_OS == "Windows":
            data_folder_path = f"src\{self.__settings.get('data-folder-name')}"
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
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    search_files = SearchFilesService()
    search_files.on_startup()
    search_files.add_server_functions()
    search_files.create_end_point("[::]:8080")
    service = search_files.get_service()
    service.start()
    service.wait_for_termination()
