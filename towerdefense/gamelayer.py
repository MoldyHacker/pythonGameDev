from cocos.scene import Scene
from cocos.layer import Layer
from cocos.director import director
from cocos.collision_model import CollisionManagerGrid
from cocos.scenes import FadeTransition, SplitColsTransition
from cocos.text import Label
from cocos.actions import Delay, CallFunc
from towerdefense.scenario import get_scenario_1
import towerdefense.actors as actors
import towerdefense.mainmenu as mainmenu
import random


def new_game():
    scenario = get_scenario_1()
    background = scenario.get_background()
    hud = HUD()  # was None
    game_layer = GameLayer(hud, scenario)
    return Scene(background, game_layer, hud)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self, hud, scenario):
        super().__init__()
        self.hud = hud
        self.scenario = scenario

        self.bunker = actors.Bunker(*scenario.bunker_position)
        self.add(self.bunker)

        w, h = director.get_window_size()
        cell_size = 32

        self.collman_enemies = CollisionManagerGrid(0, w, 0, h, cell_size, cell_size)
        self.collman_slots = CollisionManagerGrid(0, w, 0, h, cell_size, cell_size)

        for slot in scenario.turret_slots:
            self.collman_slots.add(actors.TurretSlot(slot, cell_size))

        self.score = 0
        self.scrap = 40
        self.turrets = []

        self.schedule(self.game_loop)

    @property
    def scrap(self):
        return self._scrap

    @scrap.setter
    def scrap(self, val):
        self._scrap = val
        self.hud.update_scrap(val)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, val):
        self._score = val
        self.hud.update_score(val)

    # @property
    # def bunker_health(self):
    #     return self._bunker_health
    #
    # @bunker_health.setter
    # def bunker_health(self, val):
    #     self._bunker_health = val
    #     self.hud.update_bunker_health(val)

    def create_enemy(self):
        spawn_x, spawn_y = self.scenario.enemy_start

        x = spawn_x + random.uniform(-10, 10)
        y = spawn_y + random.uniform(-10, 10)

        self.add(actors.Enemy(x, y, self.scenario.enemy_actions))

    def game_loop(self, _):
        self.collman_enemies.clear()

        for obj in self.get_children():
            if isinstance(obj, actors.Enemy):
                self.collman_enemies.add(obj)

        for obj in self.collman_enemies.iter_colliding(self.bunker):
            self.bunker.collide(obj)

        for turret in self.turrets:
            obj = next(self.collman_enemies.iter_colliding(turret), None)
            turret.collide(obj)

        if random.random() < 0.005:
            self.create_enemy()

    def on_mouse_press(self, x, y, buttons, mod):
        slots = self.collman_slots.objs_touching_point(x, y)
        if len(slots) > 0 and self.scrap >= 20:
            self.scrap -= 20
            slot = next(iter(slots))
            turret = actors.Turret(*slot.cshape.center)
            self.turrets.append(turret)
            self.add(turret)
            # TODO: Challenge if turret is present in slot, don't place.

    def remove(self, obj):
        if obj is self.bunker:
            director.replace(SplitColsTransition(game_over()))
        elif isinstance(obj, actors.Enemy) and obj.destroyed_by_player:
            self.score += obj.points
            self.scrap += 5
        super().remove(obj)


class HUD(Layer):
    def __init__(self):
        super().__init__()
        w, h = director.get_window_size()
        self.score_text = self._create_text(60, h - 40)
        self.scrap_text = self._create_text(w - 60, h - 40)
        self.bunker_health_text = self._create_text(w // 2, h - 40)

    def _create_text(self, x, y):
        text = Label(font_size=18,
                     font_name='Oswald',
                     anchor_x='center',
                     anchor_y='center')
        text.position = (x, y)
        self.add(text)
        return text

    def update_score(self, score):
        self.score_text.element.text = 'Score: {}'.format(score)

    def update_scrap(self, scrap):
        self.scrap_text.element.text = 'Scrap: {}'.format(scrap)

    def update_bunker_health(self, bunker_health):
        self.bunker_health_text.element.text = 'Bunker Health: {}'.format(bunker_health)


def game_over():
    w, h = director.get_window_size()
    layer = Layer()
    text = Label('Game Over',
                 position=(w * 0.5, h * 0.5),
                 font_name='Oswald',
                 font_size=72,
                 anchor_x='center',
                 anchor_y='center')
    layer.add(text)
    scene = Scene(layer)
    menu_scene = FadeTransition(mainmenu.new_menu())  # added mainmenu to the new_menu
    show_menu = lambda: director.replace(menu_scene)
    scene.do(Delay(3) + CallFunc(show_menu))  # removed mainmenu. from the show menu
    return scene
