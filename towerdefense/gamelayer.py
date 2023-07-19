from cocos.scene import Scene
from cocos.layer import Layer
from cocos.director import director
from cocos.collision_model import CollisionManagerGrid
from cocos.scenes import FadeTransition, SplitColsTransition
from cocos.text import Label
from cocos.actions import Delay, CallFunc
from towerdefense.scenario import get_scenario_1
# import towerdefense.actors as actors
import towerdefense.mainmenu as mainmenu
import random


def new_game():
    scenario = get_scenario_1()
    background = scenario.get_background()
    return Scene(background)
