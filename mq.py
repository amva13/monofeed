from queue import SimpleQueue
from schema import Tick

class AbstractQueue:
    def __init__(self, max_size):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented __init__()")
    
    def enqueue(self, item):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented enqueue")
    
    def dequeue(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented dequeue")
    
    def isEmpty(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented isEmpty")
    
    def isFull(self):
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented isFull")
 

class DefaultQueue(AbstractQueue):
    
    def __init__(self, max_size=100, timeout=60):
        assert isinstance(max_size, int) and isinstance(timeout, int)
        self.Q = SimpleQueue()
        self.timeout = timeout
    
    def enqueue(self, item):
        return self.Q.put(item, timeout=self.timeout)
    
    def dequeue(self):
        return self.Q.get(timeout=self.timeout)
    
    def isEmpty(self):
        return self.Q.empty()
    
    def isFull(self):
        return self.Q.full()

    
class TickQueue(DefaultQueue):
    
    def enqueue(self, item):
        assert isinstance(item,Tick)
        return super().enqueue(item)