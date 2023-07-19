from towerdefense.gamelayer import new_game
from cocos.menu import Menu, MenuItem
from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.actions import ScaleTo
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition
import pyglet.app


class MainMenu(Menu):
    def __init__(self):
        super().__init__('Tower Defense')

        self.font_title['font_name'] = 'Oswald'

        self.font_item['font_name'] = 'Oswald'
        self.font_item_selected['font_name'] = 'Oswald'

        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = list()
        items.append(MenuItem('New Game', self.on_new_game))
        items.append(MenuItem('Quit', pyglet.app.exit))

        self.create_menu(items, ScaleTo(1.25, duration=0.25), ScaleTo(1.0, duration=0.25))

    def on_new_game(self):
        director.push(FadeTRTransition(new_game(), duration=2))


def new_menu():
    scene = Scene()
    color_layer = ColorLayer(205, 133, 63, 255)

    scene.add(MainMenu(), z=1)
    scene.add(color_layer, z=0)

    return scene
