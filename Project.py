from Queue import *
from Node import *
from dataclasses import dataclass, field
from typing import Any
import math
from time import sleep
from dataclasses import dataclass, field
from typing import Any
from time import perf_counter
from functools import wraps
import threading
@dataclass
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
class Searchalgorithm():
    __slots__ = ('Barricade' ,'Food' , 'Pacman','Branching_fuctor','BoardBorder','RootNode','RootNodeForAStar','ClosedList','count' , 'countAStar' , 'countDFS' , 'countBFS')
    def __init__(self, Pacman , Food , Barricade , Branching_fuctor=4):
        self.Barricade = Barricade
        self.Food = Food
        self.Pacman = Pacman
        self.Branching_fuctor  = Branching_fuctor
        self.BoardBorder = [(0,0) , (19,29)]
        self.RootNode = self.making_node(None , self.Pacman)[0]
        self.RootNodeForAStar = self.making_nodeForAStar(None , self.Pacman)[0]
        self.ClosedList =  []
        self.count = 0
    def time_calculation(func):
        @wraps(func)
        def wr_decorator(*args , **kwargs):
            start_time = perf_counter()
            value = func(*args , **kwargs)
            end_time= perf_counter()
            run_time = end_time - start_time
            return value , run_time
        return wr_decorator
    @time_calculation
    def BFS(self)->None :
        _fringe = MYFIFOQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNode);
        _fringe.PutInOrder(self.making_node(self.RootNode , _addjacent  ))
        _Result = []
        order = {}
        while True:
            Checking_Node = _fringe.get()
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                if self.goal_test(Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            _ResultCordinate = []
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)!=0:
                                obj = Searchalgorithm(self.Pacman , self.Food , self.Barricade)
                                PreAnwser = obj.AStar()
                                return ((_ResultCordinate , self.ClosedList , True) , PreAnwser)
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expand(Checking_Node , _fringe)





    @time_calculation
    def DFS(self)->None :
        _fringe = MYLIFOQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNode);
        _fringe.PutInOrder(self.making_node(self.RootNode , _addjacent  ))
        _Result = []
        while True:
            Checking_Node = _fringe.get()
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                if self.goal_test(Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            _ResultCordinate = []
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)!=0:
                                obj = Searchalgorithm(self.Pacman , self.Food , self.Barricade)
                                PreAnwser = obj.AStar()
                                return ((_ResultCordinate , self.ClosedList , True) , PreAnwser)
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expand(Checking_Node , _fringe)
    @time_calculation
    def AStar(self) ->None:
        _fringe = MYPriorityQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNodeForAStar);
        _fringe.PutInOrder(self.making_nodeForAStar(self.RootNodeForAStar , _addjacent  ))
        _Result = []
        while True:
            Checking_Node = _fringe.get()[2]
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                next(self)
                if self.goal_test(Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            _ResultCordinate = []
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)!=0:
                                obj = Searchalgorithm(self.Pacman , self.Food , self.Barricade)
                                PreAnwser = obj.AStar()
                                return ((_ResultCordinate , self.ClosedList , True) , PreAnwser)
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expandNodeForAStar(Checking_Node , _fringe)






    def adjacent_generator_for_BF1(self , node):
        _addjacant=[
        (node.x + 1 , node.y) ,
        (node.x  , node.y+1)  ,
        (node.x -1 , node.y) ,
        (node.x , node.y-1)

        ]
        return _addjacant
    def board_border(self,Node):
        if(Node.x>self.BoardBorder[0][0] and Node.y>self.BoardBorder[0][1] and Node.x<self.BoardBorder[1][0] and Node.y<self.BoardBorder[1][1] ):
            return True

    def making_node(self,parrent , *Address):
        l = []

        for item in Address[0]:
            node  = Node()
            node.x = item[0]
            node.y = item[1]
            node.parrent =  parrent
            l.append(node)
        return l
    def making_nodeForAStar(self,parrent , *Address):
        l = []
        for item in Address[0]:
            node  = AStarNode()
            node.x = item[0]
            node.y = item[1]
            _food = self.Food[0]
            try:
                node.value = math.sqrt((item[0]-_food[0])**2 + (item[1]-_food[1])**2)+parrent.TravelledDistance+1
                node.TravelledDistance = parrent.TravelledDistance + 1
            except:
                node.value = math.sqrt((item[0]-_food[0])**2 + (item[1]-_food[1])**2)+1
                node.TravelledDistance = 1
            node.parrent =  parrent
            l.append(node)
        return l
    def _making_nodeForUCS(self,parrent , *Address)->list:
        l = []
        for item in Address[0]:
            node  = AStarNode()
            node.x = item[0]
            node.y = item[1]
            try:
                node.value = parrent.TravelledDistance+1
                node.TravelledDistance = parrent.TravelledDistance + 1
            except:
                node.value = 1
                node.TravelledDistance = 1
            node.parrent =  parrent
            l.append(node)
        return l
    def barricade_checking(self , node):
        if ((node.x , node.y)) not in self.Barricade:
            return True
    def goal_test(self , node ):
        if ((node.x,node.y)) in self.Food:
            self.Food.remove((node.x,node.y))
            return True
    def expand(self , node , _fringe):
        addjacent =self.making_node(node , self.adjacent_generator_for_BF1(node))
        for ChildNode in addjacent:
            if (ChildNode.x ,ChildNode.y)  not in self.ClosedList and self.barricade_checking(ChildNode) and self.board_border(ChildNode):
                _fringe.put(ChildNode)

    def expandNodeForAStar(self , node , _fringe):
        addjacent =self.making_nodeForAStar(node , self.adjacent_generator_for_BF1(node))
        for ChildNode in addjacent:
            if (ChildNode.x , ChildNode.y) not in self.ClosedList and self.barricade_checking(ChildNode) and self.board_border(ChildNode):
                _fringe.put(ChildNode)
    def __enter__(self):
        return self
    def __exit__(self , exc_type , exc_val , exc_tb ):
        return True
    def __next__(self):
        self.count+=1
        return self.count













