import cocos.actions as action
from cocos.tiles import load

RIGHT = action.RotateBy(90, 1)
LEFT = action.RotateBy(-90, 1)


def move(x, y):
    duration = abs(x + y) / 100.0
    return action.MoveBy((x, y), duration=duration)


class Scenario:
    def __init__(self, tmx_file, map_layer, turrets, bunker, enemy_start):
        self.tmx_file_name = tmx_file
        self.map_layer_name = map_layer
        self.turret_slots = turrets
        self.bunker_position = bunker
        self.enemy_start = enemy_start

    @property
    def enemy_actions(self):
        return self._enemy_actions

    @enemy_actions.setter
    def enemy_actions(self, action_list):
        self._enemy_actions = action.Delay(0)
        for step in action_list:
            self._enemy_actions += step

    def get_background(self):
        tmx_map_layers = load('assets/{}.tmx'.format(self.tmx_file_name))
        bg = tmx_map_layers[self.map_layer_name]
        bg.set_view(0, 0, bg.px_width, bg.px_height)
        return bg


def get_scenario_1():
    turret_slots = [(96, 320), (288, 288), (448, 320), (96, 96), (320, 96), (512, 96)]
    bunker_position = (48, 400)
    enemy_start = (-80, 176)
    sc = Scenario('level1', 'map1', turret_slots, bunker_position, enemy_start)
    sc.enemy_actions = [RIGHT, move(640, 0), LEFT, move(0, 224), LEFT, move(-512, 0)]
    return sc
