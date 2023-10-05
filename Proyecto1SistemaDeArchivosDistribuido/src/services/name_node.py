
from ..utils.index_table import IndexTable

class NameNodeService:
    def __init__(
        self,
        data_nodes_table: IndexTable,
        http_api_service
    ) -> None:
        self.__data_nodes_table = data_nodes_table
        
        
    def attendGrpcRequest(
        self, 
        request, 
        context) -> ...:
        ...

            
    def init_http_service(self):
        ...
    
    
    def attendHttpRequest(self):
        ...
        
        
    
    def build(self):
        ...
    
    
    
    