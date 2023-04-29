from Queue import *
from Node import *
from dataclasses import dataclass, field
from typing import Any
import math
import random
from time import sleep
from dataclasses import dataclass, field
from typing import Any
from time import perf_counter
from functools import wraps
import threading
MiddleNode = 0
MiddleNode1 = 0
run_time  = 0
@dataclass
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
class Searchalgorithm():
    __slots__ = ('Barricade' ,'Food' , 'Pacman','Branching_fuctor','BoardBorder','RootNode','RootNodeForAStar' ,'RootNodeForIDS', 'RootNodeForUCS','ClosedList','count' , 'countAStar' , 'countDFS' , 'countBFS' , 'UCSDict')
    def __init__(self, Pacman , Food , Barricade ,UCSDict = [] ,  Branching_fuctor=4):
        self.Barricade = Barricade
        self.Food = Food
        self.Pacman = Pacman
        self.Branching_fuctor  = Branching_fuctor
        self.BoardBorder = [(0,0) , (19,29)]
        self.RootNode = self.making_node(None , self.Pacman)[0]
        self.RootNodeForAStar = self.making_nodeForAStar(None , self.Pacman)[0]
        #self.RootNodeForUCS = self.making_nodeForUCS(None , self.Pacman)[0]
        self.RootNodeForIDS = self.making_nodeForIDS(None , self.Pacman)[0]
        self.ClosedList =  []
        self.count = 0
        self.UCSDict = {}

    def time_calculation(func):
        @wraps(func)
        def wr_decorator(*args , **kwargs):
            start_time = perf_counter()
            value = func(*args , **kwargs)
            end_time= perf_counter()
            global run_time
            run_time = run_time +  end_time - start_time
            return value
        return wr_decorator
    @time_calculation
    def BFS(self)->None :
        _fringe = MYFIFOQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNode);
        _fringe.PutInOrder(self.making_node(self.RootNode , _addjacent  ))
        _Result = []
        order = {}
        _ResultCordinate = []
        global run_time
        while True:
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            Checking_Node = _fringe.get()
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                if self.goal_test(temp:=Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)>1:
                                self.Food.remove((temp.x , temp.y))
                                obj = Searchalgorithm([(temp.x , temp.y)] , self.Food , self.Barricade)
                                PreAnwser = obj.BFS()
                                for i in PreAnwser[0]:
                                    _ResultCordinate.append(i)
                                for i in PreAnwser[1]:
                                    self.ClosedList.append(i)
                                return _ResultCordinate, self.ClosedList , True and PreAnwser[2],run_time
                            return (_ResultCordinate , self.ClosedList , True , run_time)
                else:
                    self.expand(Checking_Node , _fringe)
                    if(_fringe.empty()):
                        return([] , self.ClosedList , False , run_time)





    @time_calculation
    def DFS(self)->None :
        _fringe = MYFIFOQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNode);
        _fringe.PutInOrder(self.making_node(self.RootNode , _addjacent  ))
        _Result = []
        order = {}
        _ResultCordinate = []
        global run_time
        while True:
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            Checking_Node = _fringe.get()
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                if self.goal_test(temp:=Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)>1:
                                self.Food.remove((temp.x , temp.y))
                                obj = Searchalgorithm([(temp.x , temp.y)], self.Food , self.Barricade)
                                PreAnwser = obj.DFS()
                                for i in PreAnwser[0]:
                                    _ResultCordinate.append(i)
                                for i in PreAnwser[1]:
                                    self.ClosedList.append(i)
                                return _ResultCordinate, self.ClosedList , True and PreAnwser[2]
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expand(Checking_Node , _fringe)
                    if(_fringe.empty()):
                        return([] , self.ClosedList , False)
    @time_calculation
    def AStar(self) ->None:
        _fringe = MYPriorityQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNodeForAStar);
        _fringe.PutInOrder(self.making_nodeForAStar(self.RootNodeForAStar , _addjacent  ))
        _Result = []
        while True:
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            Checking_Node = _fringe.get()[2]
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                next(self)
                if self.goal_test(temp:=Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            _ResultCordinate = []
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)>1:
                                self.Food.remove((temp.x , temp.y))
                                obj = Searchalgorithm([(temp.x , temp.y)] , self.Food , self.Barricade)
                                PreAnwser = obj.DFS()
                                for i in PreAnwser[0]:
                                    _ResultCordinate.append(i)
                                for i in PreAnwser[1]:
                                    self.ClosedList.append(i)
                                return _ResultCordinate, self.ClosedList , True and PreAnwser[2]
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expandNodeForAStar(Checking_Node , _fringe)
                    if(_fringe.empty()):
                        return([] , self.ClosedList , False)
    @time_calculation
    def UCS(self) ->None:
        _fringe = MYPriorityQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNodeForUCS);
        _fringe.PutInOrder(self.making_nodeForUCS(self.RootNodeForUCS , _addjacent  ))
        _Result = []
        while True:
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            Checking_Node = _fringe.get()[2]
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                next(self)
                if self.goal_test(temp:=Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            _ResultCordinate = []
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)>1:
                                self.Food.remove((temp.x , temp.y))
                                obj = Searchalgorithm([(temp.x , temp.y)] , self.Food , self.Barricade)
                                PreAnwser = obj.UCS()
                                for i in PreAnwser[0]:
                                    _ResultCordinate.append(i)
                                for i in PreAnwser[1]:
                                    self.ClosedList.append(i)
                                return _ResultCordinate, self.ClosedList , True and PreAnwser[2]
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expandNodeForAStar(Checking_Node , _fringe)
                    if(_fringe.empty()):
                        return([] , self.ClosedList , False)
    def IDSCaller(self , MAXDepth):
        for i in range(3,MAXDepth):
            obj = Searchalgorithm(self.Pacman, self.Food , self.Barricade)
            Result = obj.IDS(i)
            if(Result[2]==True):
                return Result
            else:
                pass
        return ([] , self.ClosedList , False)


    @time_calculation
    def IDS(self , MAXDepth)->None :
        _fringe = MYFIFOQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNodeForIDS);
        _fringe.PutInOrder(self.making_nodeForIDS(self.RootNodeForIDS , _addjacent  ))
        _Result = []
        order = {}
        _ResultCordinate = []
        global run_time
        while True:
            if(_fringe.empty()):
                return([] , self.ClosedList , False)
            Checking_Node = _fringe.get()
            if(Checking_Node.TravelledDistance>MAXDepth):
                return([] , self.ClosedList , False)
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                if self.goal_test(temp:=Checking_Node):
                    while True:
                        _Result.append(Checking_Node)
                        Checking_Node = Checking_Node.parrent
                        if(Checking_Node == None):
                            for i in _Result:
                                _ResultCordinate.append((i.x , i.y , next(self)))
                            if len(self.Food)>1:
                                self.Food.remove((temp.x , temp.y))
                                obj = Searchalgorithm([(temp.x , temp.y)], self.Food , self.Barricade)
                                PreAnwser = obj.IDSCaller()
                                for i in PreAnwser[0]:
                                    _ResultCordinate.append(i)
                                for i in PreAnwser[1]:
                                    self.ClosedList.append(i)
                                return _ResultCordinate, self.ClosedList , True and PreAnwser[2]
                            return (_ResultCordinate , self.ClosedList , True)
                else:
                    self.expandNodeForAStar(Checking_Node , _fringe)
                    if(_fringe.empty()):
                        return([] , self.ClosedList , False)





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
    def making_nodeForUCS(self,parrent , *Address):
        l = []
        for item in Address[0]:
            node  = AStarNode()
            node.x = item[0]
            node.y = item[1]
            _food = self.Food[0]
            try:
                node.value = self.UCSDict.find((x,y))
                node.TravelledDistance = parrent.TravelledDistance + 1
            except:
                node.value = self.UCSDict.find((x,y))
                node.TravelledDistance = 1
            node.parrent =  parrent
            l.append(node)
        return l
    def making_nodeForIDS(self,parrent , *Address):
        l = []
        for item in Address[0]:
            node  = AStarNode()
            node.x = item[0]
            node.y = item[1]
            _food = self.Food[0]
            try:
                node.TravelledDistance = parrent.TravelledDistance + 1
            except:
                node.TravelledDistance = 1
            node.parrent =  parrent
            l.append(node)
        return l
    def barricade_checking(self , node):
        if ((node.x , node.y)) not in self.Barricade:
            return True
    def goal_test(self , node ):
        if ((node.x,node.y)) in self.Food:
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

    def CustomBFS(self , event)->None :
        global CommonClosedlist
        global MiddleNode
        global MiddleNode1
        _fringe = MYFIFOQueue(self)
        _addjacent  = self.adjacent_generator_for_BF1(self.RootNode);
        _fringe.PutInOrder(self.making_node(self.RootNode , _addjacent  ))
        _Result = []
        order = {}
        while True:
            if(event.is_set()):
                return
            Checking_Node = _fringe.get()
            if((Checking_Node.x , Checking_Node.y) not in self.ClosedList and self.barricade_checking(Checking_Node) and self.board_border(Checking_Node)):
                self.ClosedList.append((Checking_Node.x , Checking_Node.y))
                for item in CommonClosedlist:
                    if((item.x == Checking_Node.x and item.y == Checking_Node.y)):
                        MiddleNode = Checking_Node
                        MiddleNode1 = item
                        event.set()
                        return
                CommonClosedlist.append(Checking_Node)
                self.expand(Checking_Node , _fringe)
                if(_fringe.empty()):
                    return([] , self.ClosedList , False)
    @time_calculation
    def bi_directional(self):

        event = threading.Event()
        a = Searchalgorithm(self.Pacman , self.Food , self.Barricade)
        b = Searchalgorithm(self.Food ,self.Pacman  , self.Barricade)
        t1 = threading.Thread(target = a.CustomBFS,args=(event,))
        t2 = threading.Thread(target = b.CustomBFS ,args=(event,))
        t1.start()
        t2.start()
        event.wait()
        _Result = []
        _Result1 = []
        global MiddleNode
        global MiddleNode1
        _ResultCordinate = []
        _ResultCordinate1 = []


        if(event.is_set()):
            try:
                while True:

                    MiddleNode3 = MiddleNode1
                    _ResultCordinate.append((MiddleNode3.x , MiddleNode3.y))
                    MiddleNode1 = MiddleNode1.parrent
                    if(MiddleNode3 == None):
                        break
            except:
                pass
            while True:
                _Result.append(MiddleNode)
                MiddleNode = MiddleNode.parrent
                if(MiddleNode == None):
                    for i in _Result:
                        _ResultCordinate1.append((i.x , i.y))
                    return (_ResultCordinate , _ResultCordinate1)
    def __enter__(self):
        return self
    def __exit__(self , exc_type , exc_val , exc_tb ):
        return True
    def __next__(self):
        self.count+=1
        return self.count


CommonClosedlist = []










