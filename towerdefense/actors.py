from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.collision_model import CircleShape, AARectShape
from cocos.actions import IntervalAction, Delay, CallFunc, MoveBy
from pyglet.image import ImageGrid, Animation, load
import math


raw = load('assets/explosion.png')
seq = ImageGrid(raw, 1, 8)
explosion_img = Animation.from_image_sequence(seq, 0.07, False)


class Actor(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)
        pos = Vector2(x, y)
        self.position = pos

        self._cshape = CircleShape(pos, self.width * 0.5)

    @property
    def cshape(self):
        self._cshape.center = Vector2(self.x, self.y)
        return self._cshape


class Hit(IntervalAction):
    def init(self, duration=0.5):
        self.duration = duration

    def update(self, pct_elapsed):
        self.target.color = (255, 255 * pct_elapsed, 255 * pct_elapsed)


class Explosion(Sprite):
    def __init__(self, pos):
        super().__init__(explosion_img, pos)
        self.do(Delay(1) + CallFunc(self.kill))


class Enemy(Actor):
    def __init__(self, x, y, actions):
        super().__init__('tank.png', x, y)

        self.health = 100
        self.points = 20
        self.destroyed_by_player = False

        self.do(actions)

    def explode(self):
        self.parent.add(Explosion(self.position))
        self.kill()

    def hit(self):
        self.health -= 25
        self.do(Hit())

        if self.health <= 0 and self.is_running:
            self.destroyed_by_player = True
            self.explode()



