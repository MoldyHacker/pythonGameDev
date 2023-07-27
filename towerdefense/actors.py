import pyglet.media
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.collision_model import CircleShape, AARectShape
from cocos.actions import IntervalAction, Delay, CallFunc, MoveBy
from pyglet.image import ImageGrid, Animation, load
import math
from pyglet.media import load as mload

raw = load('assets/explosion.png')
seq = ImageGrid(raw, 1, 8)
explosion_img = Animation.from_image_sequence(seq, 0.07, False)

turret_shot_sfx = mload('assets/sfx/cannon-shot.mp3')
bunker_explosion_sfx = mload('assets/sfx/explosion.mp3')
tank_explosion_sfx = mload('assets/sfx/hit.mp3')
turret_placement_sfx = mload('assets/sfx/heavy_thud.mp3')


class HealthBar(Sprite):
    def __init__(self):
        super().__init__('assets/health_bar.png', color=(255, 0, 0), position=(-20, 0))

        self.green_sprite = Sprite('assets/health_bar.png', color=(0, 255, 0), position=(0, 0))
        self.add(self.green_sprite)

    def update_percent(self, percent_full):
        # Clamp the percentage between 0 and 100
        percent_full = max(0, min(100, percent_full))

        # Update the scale_y property of the green sprite based on the percentage
        self.green_sprite.scale_y = percent_full / 100

        # lock the green sprite to one side
        full_height = self.height  # The height of the overall health bar
        green_height = self.green_sprite.height * self.green_sprite.scale_y
        self.green_sprite.position = (0, (full_height - green_height) / 2)


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

        self.starting_health = 100
        self.health = 100
        self.points = 20
        self.destroyed_by_player = False

        # self.health_percentage = str(round(self.health / self.starting_health * 100)) + '%'

        # Challenge add health label next to enemy tank
        # self.health_label = Label(
        #     self.health_percentage,
        #     font_name='Oswald',
        #     font_size=24,
        #     anchor_x='left',
        #     anchor_y='center'
        # )
        # self.health_label.position = self.width // 2, self.height // 2
        # self.add(self.health_label)

        self.health_bar = HealthBar()
        self.health_bar.position = self.width // 2 + 5, self.height + 5
        self.add(self.health_bar)

        self.do(actions)

    def explode(self):
        self.parent.add(Explosion(self.position))
        tank_explosion_sfx.play()
        self.kill()

    def hit(self):
        self.health -= 25
        # self.do(Hit())
        # self.health_label.element.text = "{}%".format(self.health)
        self.health_bar.update_percent(self.health / self.starting_health * 100)

        if self.health <= 0 and self.is_running:
            self.destroyed_by_player = True
            self.explode()


class Bunker(Actor):
    def __init__(self, x, y):
        super().__init__('bunker.png', x, y)
        self.health = 100

    def collide(self, other):
        if isinstance(other, Enemy):
            self.health -= 10
            other.explode()
            if self.health <= 0 and self.is_running:
                bunker_explosion_sfx.play()
                self.kill()


class Shoot(Sprite):
    def __init__(self, pos, travel_path, enemy):
        super().__init__('shoot.png', position=pos)
        self.do(MoveBy(travel_path, 0.1) + CallFunc(self.kill) + CallFunc(enemy.hit))
        turret_shot_sfx.play()


class TurretSlot:
    def __init__(self, pos, side):
        self.cshape = AARectShape(Vector2(*pos), side * 0.5, side * 0.5)


class Turret(Actor):
    def __init__(self, x, y):
        super().__init__('turret.png', x, y)
        self.add(Sprite('range.png', opacity=50, scale=5))
        self.cshape.r = self.width * 5 / 2
        self.target = None
        self.period = 1.0
        self.elapsed = 0.0
        self.schedule(self._shoot)
        turret_placement_sfx.play()

    def _shoot(self, delta_time):
        if self.elapsed < self.period:
            self.elapsed += delta_time
        elif self.target is not None:
            self.elapsed = 0.0
            target_path = Vector2(self.target.x - self.x, self.target.y - self.y)
            pos = self.cshape.center + target_path.normalized() * 20
            self.parent.add(Shoot(pos, target_path, self.target))

    def collide(self, other):
        self.target = other
        if self.target is not None:
            x, y = other.x - self.x, other.y - self.y
            angle = -math.atan2(y, x)
            self.rotation = math.degrees(angle)
