# from typing import Any
from tracker.models import requestsLogs


class RequstLogging:
    
    def __init__(self,get_response) -> None:
        self.get_response = get_response
        
    def __call__ (self,request):
        request_info = request
        print(vars(request_info))
        print(self.get_response(request))
        
        requestsLogs.objects.get(
            request_info = vars(request_info),
            request_type = request_info.method,
            request_method = request_info.path,
        )
        
        return self.get_response(request)