'''
Modulo para implementacion de la interfaz del servicio
'''

from abc import ABC, abstractmethod
from typing import Union
from .utils import check_existing_settings
import subprocess


from typeguard import TypeCheckError
from dynaconf.utils.boxing import DynaBox as ServiceSettings 

class Service(ABC):
    
    @abstractmethod
    def check_existing_settings(
        self,
        settings_file_name:str,
        service_type:str
    ) -> Union[TypeCheckError,FileNotFoundError, ValueError, ServiceSettings]:
        return check_existing_settings(settings_file_name, service_type)
    
    
    @abstractmethod
    def validate_config():
        ...
    
    
    def on_startup(self) -> str:
        service_public_ip = subprocess.run(
            "curl ifconfig.me", 
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        return service_public_ip
    
    
    @abstractmethod
    def create_end_point():
        ...
    
    
    @abstractmethod
    def execute(self):
        ...
    
    
    @abstractmethod
    def get_name():
        ...
        
        
    @abstractmethod
    def get_settings():
        ...
        
    
    @abstractmethod    
    def get_service():
        ... 
        