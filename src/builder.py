from .service import Service
from .services.manager import ManagerService 
from .services.list_files import ListFilesService
from .services.search_files import SearchFilesService

from flask import Response
from datetime import datetime

from typeguard import typechecked

class Builder:
    @typechecked
    def __init__(self, service: Service):
        self.__service = service
    
    
    def build(self, response:Response) -> Service:
        service = self.__service
        if isinstance(service, ManagerService):
            end_points_routes = list(service.get_settings().get("end-points").keys())
            service.validate_config()
            service.check_request(end_points_routes[0])
            service.create_end_point(
                end_point_route=end_points_routes[0],
                end_point_function=service.make_request,
                response = response
            )
            service.act_on_error(response)
            service.act_on_grpc_error(response)
            service.act_on_kafka_error(response)
            return service
        
        
        elif isinstance(service, ListFilesService) or isinstance(service,SearchFilesService):
            service.on_startup()
            end_point:str = service.get_settings().get("end-point")
            service.add_server_functions()
            service.create_end_point(end_point)
            return service
                
                    
if __name__ == "__main__":
    r = Response()
    m = ManagerService()
    d = Builder(m)
    s = d.build(r)
    s.get_service().run()
    
    