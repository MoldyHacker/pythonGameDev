## Q1: Fix the bug that sticks the player cannon to the screen edges.
Describe what modifications you made and the outcome.

### My Solution

- created a new variable to calculate the x position of the cannon
- improved the logic so that when the cannon reaches the edge the position is updated. 
  - If position exceeds screen boundaries, set position to the boundary

## Q2: Create a MysteryShip class that extends Alien
- A mystery ship may be worth 10, 50, 100, or 200 points (chosen at random when created)
- It always uses "img/alien4.png" as its sprite image
- It has a horizontal speed of 150 pixels per second
- Its update() method performs its movement

- The GameLayer has a small random chance to spawn a MysteryShip every frame
- It spawns the ship 50 pixels from the top left corner of the screen
- When a MysteryShip spawns, play the sound effect "sfx/ufo_lowpitch.wav"
 

Describe what modifications you made and the outcome.

### My Solution
- Created a MsyteryShip class
  - Randomly assigns points to itself using random.choice()
  - Instead of calling super I call the Actor constructor.
    - I was going to add a 4th type of alien, but this was easier for some reason.
  - passed the on_exit function
  - Added and modified functions:
    - side_reached
    - should_turn
    - update
- Added the ufo_lowpitch.mp3 to the audio load list
- Created a function spawn_mystery_ship in GameLayer to spawn the MystryShip
  - This creates the object, adds it to the field, and plays the mp3 file if a ship has not already been active.
- In the game loop I added a function that after a small random chance.

## Q3: In the Challenges, you made two functions named increase_difficulty() -- one in AlienColumn and one in Swarm. Every time the player earns an additional 150 points, call both increase_difficulty() functions. In other words, aliens will move and fire faster at 150 points, 300 points, 450 points, etc.

Hint: GameLayer contains the swarm and the score. The swarm contains the list of columns.

Describe what modifications you made and the outcome.

## Q4: If the player destroys all aliens in the swarm, end the game with a 'You Win' message.

Describe what modifications you made and the outcome.

### My Solution

- I added a on_win function to the GamyLayer that unschedules the game loop and displays the 'You Win!' text
- To the constructor in the GameLayer I added a remaining_aliens variable that checks for the number of remaining aliens
  - self.remaining_aliens = len(self.swarm.columns) * len(self.swarm.columns[0].aliens)
- And to the collide function in the GameLayer I i checked if the instance of other i was colliding with was an alien, then it would subtract one from total.

## Q5: Add the ability to toggle a "cheat mode" on and off. When cheat mode is on, the player does not lose a life when the cannon is destroyed.

Pick two keyboard keys that are not already in use and designate one as "cheat on", the other as "cheat off". You may optionally include a visual indicator (like a label) for when cheat mode is enabled.

Hint: In which class is the life deducted? This would be a good place for a boolean flag variable.

Describe what modifications you made and the outcome. Be sure to include which keys you chose!