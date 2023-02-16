import csv
import pandas as pd

class AbstractDB:
    
    def __init__(self, params=None):
        raise NotImplementedError(f"{AbstractDB.__class__.__name__} __init__() is not implemented")
    
    def write(self, item):
        raise NotImplementedError(f"{AbstractDB.__class__.__name__} write() is not implemented")
    
    def read(self, query):
        raise NotImplementedError(f"{AbstractDB.__class__.__name__} read() is not implemented")


class consoleDB(AbstractDB):
    
    def __init__(self, params=None):
        pass
    
    def write(self, item):
        print(f"Got entry of type {item.__class__.__name__}, values are: {vars(item)}")
        

class csvDB(AbstractDB):
    
    def __init__(self, params=None):
        assert params is not None and isinstance(params, dict) and "path" in params and isinstance(params.get('path'),str)
        self.path = params["path"]
        self.type = params.get("type", None)
        self.fields = params.get("fields", None)
        assert self.fields is not None
        
    def write(self, item):
        if self.type is not None:
            assert isinstance(item, self.type)
        assert self.fields is not None
        with open(self.path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(item.as_dict())
        print(f"Wrote entry of type {item.__class__.__name__}, values are: {item.__dict__}")
        
    def read(self, query=None):
        if query is None:
            # default to outputting a pandas dataframe from the path
            return pd.read_csv(self.path)
        raise ValueError(f"{self.__class__.__name__} does not support queries at this time.")