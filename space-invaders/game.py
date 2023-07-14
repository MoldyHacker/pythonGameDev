from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.collision_model import CollisionManagerGrid, AARectShape
from cocos.layer import Layer
from cocos.director import director
from cocos.scene import Scene
from cocos.text import Label
from pyglet.window import key
from pyglet.image import load as iload, ImageGrid, Animation
from pyglet.media import load as mload
from random import random


def load_animation(image):
    seq = ImageGrid(iload(image), 2, 1)
    return Animation.from_image_sequence(seq, 0.5)


TYPES = {
    '1': (load_animation('img/alien1.png'), 40),
    '2': (load_animation('img/alien2.png'), 20),
    '3': (load_animation('img/alien3.png'), 10)
}


class Actor(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)

        pos = Vector2(x, y)
        self.position = pos

        self.cshape = AARectShape(pos, self.width * 0.5, self.height * 0.5)

    def move(self, offset):
        self.position += offset
        self.cshape.center += offset

    def update(self, delta_time):
        pass

    def collide(self, other):
        pass


class Alien(Actor):
    def __init__(self, x, y, alien_type, column=None):
        animation, points = TYPES[alien_type]
        super().__init__(animation, x, y)
        self.points = points
        self.column = column

    def on_exit(self):
        super().on_exit()
        if self.column:
            self.column.remove(self)


class AlienColumn:
    def __init__(self, x, y):
        alien_types = enumerate(['3', '3', '2', '2', '1'])

        # self.aliens = []
        # for i, alien_type in alien_types:
        #     self.aliens.append(Alien(x, i + 60, alien_type, self))

        self.aliens = [
            Alien(x, i * 60, alien_type, self)
            for i, alien_type in alien_types
        ]

    def remove(self, alien):
        self.aliens.remove(alien)

    def should_turn(self, direction):
        if len(self.aliens) == 0:
            return False
        else:
            alien = self.aliens[0]

        x, width = alien.x, alien.parent.width

        return x >= width - 50 and direction == 1 or x <= 50 and direction == -1


class Swarm:
    def __init__(self, x, y):
        self.columns = [
            AlienColumn(x + i * 60, y)
            for i in range(10)
        ]

        self.speed = Vector2(10, 0)
        self.direction = 1

        self.elapsed = 0.0
        self.period = 1.0

    def side_reached(self):
        return any(map(lambda col: col.should_turn(self.direction), self.columns))

    def __iter__(self):
        for column in self.columns:
            for alien in column.aliens:
                yield alien

    def update(self, delta_time):
        self.elapsed += delta_time
        while self.elapsed >= self.period:
            self.elapsed -= self.period
            movement = self.direction * self.speed

            if self.side_reached():
                self.direction *= -1
                movement = Vector2(0, -10)

            for alien in self:
                alien.move(movement)


class PlayerCannon(Actor):
    def __init__(self, x, y):
        super().__init__('img/cannon.png', x, y)
        self.speed = Vector2(200, 0)

    def collide(self, other):
        other.kill()
        self.kill()

    def update(self, delta_time):
        horizontal_movement = keyboard[key.RIGHT] - keyboard[key.LEFT]
        left_edge = self.width * 0.5
        right_edge = self.parent.width - left_edge

        print(left_edge, self.x, right_edge)

        if left_edge <= self.x <= right_edge:
            self.move(self.speed * horizontal_movement * delta_time)


class HUD(Layer):
    def __init__(self):
        super().__init__()

        w, h = director.get_window_size()
        self.score_text = Label('', font_size=18)
        self.score_text.position = (20, h - 40)

        self.lives_text = Label('', font_size=18)
        self.lives_text.position = (w - 100, h - 40)

        self.add(self.score_text)
        self.add(self.lives_text)

    def update_score(self, score):
        self.score_text.element.text = 'Score: {}'.format(score)

    def update_lives(self, lives):
        self.lives_text.element.text = 'Lives: {}'.format(lives)

    def show_game_over(self, message):
        w, h = director.get_window_size()
        game_over_text = Label(message, font_size=50, anchor_x='center', anchor_y='center')
        game_over_text.position = (w * 0.5, h * 0.5)
        self.add(game_over_text)

    # def create_player(self):
    #     self.player = PlayerCannon(self.width * 0.5, 50)
    #
    #     self.add(self.player)
    #     self.hud.update_lives(self.lives)


class GameLayer(Layer):
    def __init__(self, hud):
        super().__init__()
        self.hud = hud

        w, h = director.get_window_size()
        self.width = w
        self.height = h

        self.lives = 3
        self.score = 0

        cell = 1.25 * 50
        self.collman = CollisionManagerGrid(0, w, 0, h, cell, cell)

        self.update_score()
        self.create_player()

        self.schedule(self.game_loop)

    def create_player(self):
        self.player = PlayerCannon(self.width * 0.5, 50)
        self.add(self.player)
        self.hud.update_lives(self.lives)

    def update_score(self, points=0):
        self.score += points
        self.hud.update_score(self.score)

    def game_loop(self, delta_time):
        for _, actor in self.children:
            actor.update(delta_time)


if __name__ == '__main__':
    director.init(caption='Space Invaders', width=800, height=650)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    main_scene = Scene()
    hud_layer = HUD()
    main_scene.add(hud_layer, z=1)

    game_layer = GameLayer(hud_layer)
    main_scene.add(game_layer, z=0)
    director.run(main_scene)
