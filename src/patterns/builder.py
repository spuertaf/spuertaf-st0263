from ..interfaces.service import Service
from ..services.manager import ManagerService 
from ..services.list_files import ListFilesService
from ..services.search_files import SearchFilesService

from flask import Response
from .rabbitmq import RabbitMQConnector
from datetime import datetime

from typeguard import typechecked

class Builder:
    @typechecked
    def __init__(self, service: Service):
        self.__service = service
    
    
    def build(
        self, 
        rabbitmq_connector:RabbitMQConnector,
        response:Response = None
        ) -> Service:
        service = self.__service
        if isinstance(service, ManagerService):
            if response is None:
                #raise ...
                pass
            end_points_routes = list(service.get_settings().get("end-points").keys())
            service.validate_config()
            service.check_request(end_points_routes[0])
            service.assign_id_2_request()
            service.create_end_point(
                end_point_route=end_points_routes[0],
                end_point_function=service.make_request,
                response = response
            )
            service.conf_rabbitmq_connection(rabbitmq_connector, response)
            service.act_on_error(response)
            service.act_on_grpc_error(response)
            return service
        
        
        elif isinstance(service, ListFilesService) or isinstance(service,SearchFilesService):
            service.get_mi_ip()
            service.add_server_functions()
            service.conf_rabbitmq_connection(rabbitmq_connector)
            service.on_startup(service.handle_pending_requests)
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
    
    