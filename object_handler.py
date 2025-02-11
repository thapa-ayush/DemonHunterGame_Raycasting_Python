from sprite_object import *
from npc import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # Light placement in key areas
        add_sprite(AnimatedSprites(game, pos=(2.5, 2.5)))  # Starting area
        add_sprite(AnimatedSprites(game, pos=(8.5, 5.5)))  # First corridor
        add_sprite(AnimatedSprites(game, pos=(15.5, 7.5)))  # Central area
        add_sprite(AnimatedSprites(game, pos=(20.5, 4.5)))  # Right upper area
        add_sprite(AnimatedSprites(game, pos=(25.5, 2.5)))  # Far right corner
        add_sprite(AnimatedSprites(game, pos=(3.5, 15.5)))  # Lower left section
        add_sprite(AnimatedSprites(game, pos=(14.5, 15.5)))  # Lower middle
        add_sprite(AnimatedSprites(game, pos=(22.5, 16.5)))  # Lower right arena

        # Red lights in dangerous areas
        add_sprite(AnimatedSprites(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(28.5, 10.5)))
        add_sprite(AnimatedSprites(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(24.5, 20.5)))
        add_sprite(AnimatedSprites(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 18.5)))

        # NPC placement in strategic locations
        add_npc(SoldierNPC(game, pos=(3.5, 2.5)))  # First encounter
        add_npc(SoldierNPC(game, pos=(14.5, 8.5)))  # Middle area patrol
        add_npc(SoldierNPC(game, pos=(20.5, 3.5)))  # Upper right guard

        # Stronger enemies in later areas
        add_npc(CacoDemonNPC(game, pos=(25.5, 5.5)))  # Right side ambush
        add_npc(CacoDemonNPC(game, pos=(18.5, 15.5)))  # Lower section patrol

        # Final boss in a strategic location
        add_npc(CyberDemonNPC(game, pos=(27.5, 18.5)))  # Final area boss

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)