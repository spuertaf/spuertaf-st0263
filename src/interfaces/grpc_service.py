from .service import Service
from abc import abstractmethod
import subprocess
from ..patterns.rabbitmq import RabbitMQConnector
from ..services.configs.contracts.list_files_service_pb2 import ListFilesRequest, ListFilesResponse

class GrpcService(Service):
    
    @abstractmethod
    def get_mi_ip(self) -> str:
        service_public_ip = subprocess.run(
            "curl ifconfig.me", 
            shell=True,
            capture_output=True,
            text=True
        ).stdout
        return service_public_ip
    
    
    @abstractmethod
    def handle_pending_requests(
        self, 
        rabbitmq_connector:RabbitMQConnector,
        queue_name_2_publish:str,
        pending_requests:list 
    ):
        ...
    
    
    @abstractmethod
    def on_startup(
        self, 
        rabbitmq_connector:RabbitMQConnector,
        queue_name_2_consume:str,
        queue_name_2_publish:str,
        on_startup_function:callable
    ):
        pending_requests:list = rabbitmq_connector.consume(queue_name_2_consume)
        print(f"Pending requests: {len(pending_requests)}")
        on_startup_function(rabbitmq_connector,queue_name_2_publish, pending_requests)
    
    