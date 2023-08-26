from typing import Union
import platform

from typeguard import typechecked, TypeCheckError
from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox as ServiceSettings

@typechecked
def check_existing_settings(
        settings_file_name:str,
        service_type:str
    ) -> Union[TypeCheckError, FileNotFoundError, ValueError, ServiceSettings]:
        service_settings_file = Dynaconf(settings_files=[settings_file_name])
        if service_settings_file is None:
            raise FileNotFoundError("Service config file was not found.")
        service_settings = service_settings_file.get(service_type)
        if service_settings:
            return service_settings
        raise ValueError(f"Service settings not found or empty on file: {settings_file_name}\n Service name must match service settings name on config file.")

    
def rename_2_current_OS(folder_path:str) -> str:
    current_OS = platform.system()
    if current_OS == 'Windows':
        folder_path.replace('/','\\')
    elif current_OS == 'Linux':
        folder_path.replace('\\','/')
    return folder_path