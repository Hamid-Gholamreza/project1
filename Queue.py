from queue import *
from random import*
from dataclasses import dataclass, field
from typing import Any
from time import sleep
@dataclass
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
class MYFIFOQueue(Queue):
    def __init__(self,BrSelf,  *args):
        super(Queue, self).__init__(*args)
        self.queue=Queue(maxsize=0)
        self._Brself = BrSelf
    def empty(self):
        return self.queue.empty()
    def get(self):
        return self.queue.get()
    def put(self , node):
        return self.queue.put(node)
    def PutInOrder(self,*args):
        for arg in args[0]:
            if arg not in self._Brself.Barricade:
                self.queue.put(arg)

class MYLIFOQueue(Queue):
    def __init__(self,BrSelf,  *args):
        print(args)
        super(Queue, self).__init__(*args)
        self.queue=LifoQueue(maxsize=0)
        self._Brself = BrSelf
    def empty(self):
        return self.queue.empty()
    def get(self):
        return self.queue.get()
    def put(self, node):
        return self.queue.put(node)
    def PutInOrder(self,*args):
        for arg in args[0]:
            if arg not in self._Brself.Barricade:
                print(args)
                self.queue.put(arg)
class MYPriorityQueue():
    def __init__(self,BrSelf,  *args):

        self.queue=PriorityQueue(maxsize=0)
        self._Brself = BrSelf


    def empty(self):
        return self.queue.empty()
    def get(self):
        return self.queue.get()
    def put(self , node):
        self.queue.put((node.value,random(),node))

    def PutInOrder(self,*args):
        for arg in args[0]:
            if arg not in self._Brself.Barricade:
                self.queue.put((arg.value,random(),arg))
