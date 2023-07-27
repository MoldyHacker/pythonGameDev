## Q1: Add sound effects and background music to the game. You'll need to search for and download audio files:

.WAV files for effects
.OGG or .MP3 files for music
Describe what modifications you made and the outcome.

### My Solution
    After a quick google search I found https://pixabay.com/sound-effects/ for sound effects.
    I had to alter some of the files to make them play at a resonable volume.
    But I started with the actor file.
    
    I assigned sound files to turret placements, turret shots, tanks exploding, and the bunker exploding.
    
    I added the tank explosion sound in the explode class of the Enemy
    I added the bunker explosion in the Bunker class under the collide function.    
    I added the turret shot sound in the Shoot class so that it would only make a sound when fired.
    I added the turret placement sound to the turret constructor so it would only be played once.

    I also added background music. I was going to add one for the main menu and one for the game. but i couldn't get the music to stop playing.
    

## Q2: Using a tile map editor, create a new TMX file containing a custom map. You can reuse the desert tileset ("assets/desert.png") or search for a new image.

Modify scenario.py to make your map playable.

See this tutorial page for more information: Create Your Own Tower Defense Map

Describe what modifications you made and the outcome.

## Q3: Add a label to the top-middle of the screen that displays the player bunker's current health.

Describe what modifications you made and the outcome.

### My Solution:
    I made all my ajustments in the gamelayer
    First to the GameLayer class I added a bunker_health variable and set that to the health of the bunker obj
    Then I created a @property and a @setter for the bunker that performs the same actions as the score and setters
    In the HUD class I created the text variable bunker_health_text and set it's position to the center of the screen
    Also in the HUD class I defined a function update_bunker_health that updates the bunker text element with the passed in value.
    Finally in the game_loop I used this update_bunker_health func passing in the current bunker health at every collision with the bunker.

## Q4: Create a HealthBar class that extends Sprite
It is initialized with the image "health_bar.png", a color overlay of red, and a position of (-20, 0)
Its constructor adds a second sprite as a child of itself, also using "health_bar.png", a green color overlay, and position (0, 0)
The HealthBar class contains a method that accepts the percent "full" the bar should be and updates the scale_y property of the green bar
 

Modify the Enemy class to contain a HealthBar object
When an Enemy object is hit, update the health bar
 

Describe what modifications you made and the outcome.

### My Solution
    