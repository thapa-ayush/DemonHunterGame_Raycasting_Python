import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    """
    Main game class that handles initialization, game loop, and core game mechanics.
    This is a demon-hunting FPS game where the player must eliminate all demons to win.
    """
    def __init__(self):
        # Initialize Pygame and setup display
        pg.init()
        pg.mouse.set_visible(False)  # Hide mouse cursor for immersion
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        
        # Setup game events and state
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)  # 40ms timer for game events
        self.is_victory = False
        
        # Start a new game
        self.new_game()

    def new_game(self):
        """Initialize all game components for a new game session"""
        self.map = Map(self)  # Game map
        self.player = Player(self)  # Player character
        self.object_renderer = ObjectRenderer(self)  # Handles game rendering
        self.raycasting = RayCasting(self)  # 3D rendering engine
        self.object_handler = ObjectHandler(self)  # Manages game objects and NPCs
        self.weapon = Weapon(self)  # Player's weapon
        self.sound = Sound(self)  # Game audio
        self.pathfinding = PathFinding(self)  # Enemy AI pathfinding
        
        # Reset game state
        self.is_victory = False
        self.object_renderer.explored_areas.clear()

    def update(self):
        """Update game state for each frame"""
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.check_victory()
        
        # Update display
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'Demon Hunter - FPS: {self.clock.get_fps() :.1f}')

    def check_victory(self):
        """Check if all demons are eliminated for victory condition"""
        if len([npc for npc in self.object_handler.npc_list if npc.alive]) == 0:
            self.is_victory = True

    def draw(self):
        """Render game objects to the screen"""
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        """Handle game events and user input"""
        self.global_trigger = False
        for event in pg.event.get():
            # Handle quit events
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            # Handle global game events
            elif event.type == self.global_event:
                self.global_trigger = True
            # Handle player shooting
            self.player.single_fire_event(event)

        # Check for game restart
        keys = pg.key.get_pressed()
        if (not self.player.is_alive or self.is_victory) and keys[pg.K_r]:
            self.new_game()

    def run(self):
        """Main game loop"""
        while True:
            self.check_events()
            if not self.player.is_alive:
                self.object_renderer.game_over()
            elif self.is_victory:
                self.object_renderer.victory()
            else:
                self.update()
                self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()