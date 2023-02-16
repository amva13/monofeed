import threading
from mq import AbstractQueue, TickQueue
from schema import Tick
from db import AbstractDB, consoleDB

class ProducerThread(threading.Thread):
    
    def __init__(self):
        super().__init__()

class ConsumerThread(threading.Thread):
    
    def __init__(self):
        super().__init__()
        
class WriterEnqueueThread(ProducerThread):
    
    def __init__(self, item, queue):
        assert isinstance(queue, AbstractQueue)
        super().__init__()
        
class TickWriterDefaultEnqueueThread(WriterEnqueueThread):
    
    def __init__(self, item, queue):
        super().__init__(item=item, queue=queue)
        assert isinstance(queue, TickQueue)
        assert isinstance(item, Tick)
        self.tick = item
        self.mq = queue
        
    def run(self):
        self.mq.enqueue(self.tick)
        
        
class WriterDequeueThread(ConsumerThread):
    
    def __init__(self, queue, db):
        assert isinstance(queue, AbstractQueue)
        assert isinstance(db, AbstractDB)
        super().__init__()
        

class TickWriterDefaultDequeueThread(WriterDequeueThread):
    
    def __init__(self, queue, db):
        super().__init__(queue,db)
        assert isinstance(queue, TickQueue)
        self.mq = queue
        self.db = db
        
    def run(self):
        while True:
            tick = self.mq.dequeue()
            assert isinstance(tick, Tick)
            self.db.write(tick)