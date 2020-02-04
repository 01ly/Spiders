
import requests

def register(method,api):
    def fuxk(func):
        def wrapper(self,*args,**kwargs):
            session = requests.Session()
            config = func(self,*args,**kwargs)
            response = session.request(method,api,**config)
            data = response.json()
            return data
        return wrapper
    return fuxk