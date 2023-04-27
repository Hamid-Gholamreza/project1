
"""from dataclasses import dataclass, field
from typing import Any , ClassVar

@dataclass
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

@dataclass
class Node():
    x : int
    y : int
    parrent : 'Node'
@dataclass
class AStarNode(Node):
    value : float
    TravelledDistance : float"""
from dataclasses import dataclass, field
from typing import Any
@dataclass
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
class Node(object):
    def __init__(self, *args):
        self.x = None
        self.y = None
        self.parrent = None

class AStarNode(Node):
    def __init__(self, *args):
        super(Node, self).__init__(*args)
        self.value = None
        self.TravelledDistance = None

