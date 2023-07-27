import pyglet.resource
from cocos.director import director
from towerdefense.mainmenu import new_menu
from pyglet.media import load as mload

music = mload('assets/sfx/battle-music.mp3')


if __name__ == '__main__':
    pyglet.resource.path.append('assets')
    pyglet.resource.reindex()

    pyglet.font.add_file('assets/Oswald-Regular.ttf')

    music.play()
    director.init(caption='Tower Defense')
    director.run(new_menu())
