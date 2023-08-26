from .builder import Builder
import pkgutil
import importlib
from . import services
from typing import Union
from .service import Service

from typeguard import typechecked
from flask import Response


class Adapter(Builder):
    def __init__(self):
        self.__plug_in:dict = self.gen_plug_in()
    
    
    def gen_plug_in(self) -> dict:
        def get_services_in_package(package) :
            services = []
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"{package.__name__}.{module_name}")
                classes = [module_class for _, module_class in module.__dict__.items() if isinstance(module_class, type)]
                services.append((module_name, classes[-1], ))
            return services
        plug_in = {
            service_name : service_instance() for service_name, service_instance in get_services_in_package(services)
        }
        return plug_in
    
    
    @typechecked
    def build(
            self, 
            argument_name:str, 
            response:Response
        ) -> Union[ValueError, Service]:
        try:
            service_to_build = self.__plug_in[argument_name]
            super().__init__(service_to_build)
            service_built = super().build(response)
            return service_built
        except KeyError:
            raise ValueError(f"Service {argument_name} is not a valid service to request.",
                             f"Allowed services are the following {self.__plug_in.keys()}\n")