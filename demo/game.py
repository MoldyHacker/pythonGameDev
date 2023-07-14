from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.collision_model import CollisionManagerGrid, CircleShape
from cocos.layer import Layer
from cocos.director import director
from cocos.scene import Scene
from pyglet.window import key


class Actor(Sprite):
    def __init__(self, x, y, color):
        # double underscore = dunderscore, or dunder
        super().__init__('img/ball.png', color=color)

        pos = Vector2(x, y)
        self.position = pos

        self.cshape = CircleShape(pos, self.width / 2)

        self.speed = 100


class MainLayer(Layer):
    def __init__(self):
        super().__init__()

        self.player = Actor(320, 240, (0, 0, 255))
        self.add(self.player)

        for pos in [(100, 100), (540, 380), (540, 100), (100, 300)]:
            self.add(Actor(pos[0], pos[1], (255, 0, 0)))

        for pos in [(300, 300), (140, 360), (520, 250)]:
            self.add(Actor(pos[0], pos[1], (0, 255, 0)))

        cell = self.player.width * 1.25
        self.collman = CollisionManagerGrid(0, 640, 0, 480, cell, cell)

        self.schedule(self.update)

    def update(self, delta_time):
        print(delta_time)

        horizontal_movement = keyboard[key.RIGHT] - keyboard[key.LEFT]

        vertical_movement = keyboard[key.UP] - keyboard[key.DOWN]

        pos = self.player.position

        new_x = pos[0] + self.player.speed * horizontal_movement * delta_time
        new_y = pos[1] + self.player.speed * vertical_movement * delta_time

        self.player.position = (new_x, new_y)

        self.player.cshape.center = self.player.position

        self.collman.clear()
        
        if new_x < 640 and new_x > 0 and new_y < 480 and new_y > 0:
            self.player.position = (new_x, new_y)
            self.player.cshape.center = self.player.position


        for _, actor in self.children:
            self.collman.add(actor)

        for pickup in self.collman.iter_colliding(self.player):
            self.remove(pickup)


if __name__ == "__main__":
    director.init(caption="Cocos Demo")

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    layer = MainLayer()
    scene = Scene(layer)

    director.run(scene)