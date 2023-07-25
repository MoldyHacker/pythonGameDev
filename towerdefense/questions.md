## Q1: Add sound effects and background music to the game. You'll need to search for and download audio files:

.WAV files for effects
.OGG or .MP3 files for music
Describe what modifications you made and the outcome.

## Q2: Using a tile map editor, create a new TMX file containing a custom map. You can reuse the desert tileset ("assets/desert.png") or search for a new image.

Modify scenario.py to make your map playable.

See this tutorial page for more information: Create Your Own Tower Defense Map

Describe what modifications you made and the outcome.

## Q3: Add a label to the top-middle of the screen that displays the player bunker's current health.

Describe what modifications you made and the outcome.

## Q4: Create a HealthBar class that extends Sprite
It is initialized with the image "health_bar.png", a color overlay of red, and a position of (-20, 0)
Its constructor adds a second sprite as a child of itself, also using "health_bar.png", a green color overlay, and position (0, 0)
The HealthBar class contains a method that accepts the percent "full" the bar should be and updates the scale_y property of the green bar
 

Modify the Enemy class to contain a HealthBar object
When an Enemy object is hit, update the health bar
 

Describe what modifications you made and the outcome.