import pygame as pg
import math
from settings import *

class ObjectRenderer:
    """
    Handles all game rendering including walls, sprites, UI elements, and special effects.
    Manages the game's visual presentation and special effects.
    """
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Load textures and images
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/wide_sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        
        # Load UI elements
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                           for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.victory_image = self.get_texture('resources/textures/victory.png', RES)
        
        # Initialize fonts and UI settings
        self.font = pg.font.Font(None, 72)
        self.small_font = pg.font.Font(None, 36)
        self.explored_areas = set()  # Track explored areas for fog of war
        
        # Visual effect settings
        self.damage_alpha = 0
        self.damage_fade_speed = DAMAGE_FADE_SPEED
        self.flash_alpha = 0
        self.flash_fade_speed = 10

    def draw(self):
        """Main drawing method that renders all game elements"""
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_minimap()
        self.draw_crosshair()
        self.draw_damage_effect()
        self.draw_weapon_flash()

    def draw_background(self):
        """Renders the sky and floor"""
        # Parallax sky effect
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        
        # Floor with gradient
        floor_surface = pg.Surface((WIDTH, HALF_HEIGHT))
        for y in range(HALF_HEIGHT):
            darkness = 1 - (y / HALF_HEIGHT) * 0.5
            color = tuple(int(c * darkness) for c in FLOOR_COLOR)
            pg.draw.line(floor_surface, color, (0, y), (WIDTH, y))
        self.screen.blit(floor_surface, (0, HALF_HEIGHT))

    def draw_crosshair(self):
        """Draws an animated crosshair"""
        cross_size = 20
        center_x, center_y = HALF_WIDTH, HALF_HEIGHT
        
        # Dynamic crosshair color based on whether player is aiming at an enemy
        color = (255, 0, 0) if self.game.player.is_targeting_enemy() else (255, 255, 255)
        
        # Draw crosshair lines with slight animation
        offset = math.sin(pg.time.get_ticks() * 0.005) * 2
        pg.draw.line(self.screen, color, (center_x - cross_size - offset, center_y),
                    (center_x + cross_size + offset, center_y), 2)
        pg.draw.line(self.screen, color, (center_x, center_y - cross_size - offset),
                    (center_x, center_y + cross_size + offset), 2)

    def draw_player_health(self):
        """Renders player health bar with dynamic colors and effects"""
        # Health bar background
        health_bar_width = 200
        health_bar_height = 30
        health_bar_x = 20
        health_bar_y = HEIGHT - 50
        
        # Draw background
        pg.draw.rect(self.screen, (40, 40, 40), 
                    (health_bar_x - 2, health_bar_y - 2, 
                     health_bar_width + 4, health_bar_height + 4))
        
        # Calculate health ratio and color
        health_ratio = self.game.player.health / PLAYER_MAX_HEALTH
        current_width = health_ratio * health_bar_width
        
        # Dynamic health bar color
        if health_ratio > 0.7:
            health_color = (0, 255, 0)  # Green
        elif health_ratio > 0.3:
            health_color = (255, 255, 0)  # Yellow
        else:
            health_color = (255, 0, 0)  # Red
            
        # Pulse effect when health is low
        if health_ratio < 0.3:
            pulse = abs(math.sin(pg.time.get_ticks() * 0.005))
            health_color = tuple(int(c * (0.7 + 0.3 * pulse)) for c in health_color)
        
        # Draw health bar
        pg.draw.rect(self.screen, health_color, 
                    (health_bar_x, health_bar_y, current_width, health_bar_height))
        
        # Draw health text
        health_text = f"{self.game.player.health}/{PLAYER_MAX_HEALTH}"
        for i, char in enumerate(health_text):
            if char == '/':
                char = '10'
            self.screen.blit(self.digits[char], (health_bar_x + i * 25, health_bar_y - 30))

    def draw_damage_effect(self):
        """Renders blood screen effect when player takes damage"""
        if self.damage_alpha > 0:
            damage_surface = self.blood_screen.copy()
            damage_surface.set_alpha(self.damage_alpha)
            self.screen.blit(damage_surface, (0, 0))
            self.damage_alpha = max(0, self.damage_alpha - self.damage_fade_speed)

    def draw_weapon_flash(self):
        """Renders muzzle flash effect when weapon is fired"""
        if self.flash_alpha > 0:
            flash_surface = pg.Surface(RES, pg.SRCALPHA)
            radius = 100
            center = (HALF_WIDTH, HEIGHT - 200)
            pg.draw.circle(flash_surface, (255, 200, 50, self.flash_alpha), center, radius)
            self.screen.blit(flash_surface, (0, 0))
            self.flash_alpha = max(0, self.flash_alpha - self.flash_fade_speed)

    def draw_minimap(self):
        """Renders an enhanced minimap with fog of war and enemy indicators"""
        map_size = 200
        tile_size = 10
        map_pos = (WIDTH - map_size - 20, 20)
        radius = 10

        # Create minimap surface with transparency
        minimap_surf = pg.Surface((map_size, map_size), pg.SRCALPHA)
        
        # Draw background
        pg.draw.rect(minimap_surf, (0, 0, 0, 180), (0, 0, map_size, map_size))
        pg.draw.rect(minimap_surf, (100, 100, 100, 255), (0, 0, map_size, map_size), 2)

        px, py = self.game.player.x, self.game.player.y

        # Update explored areas
        for y, row in enumerate(self.game.map.mini_map):
            for x, col in enumerate(row):
                if (x - px) ** 2 + (y - py) ** 2 <= radius ** 2:
                    self.explored_areas.add((x, y))

        # Draw explored areas with fog of war effect
        for x, y in self.explored_areas:
            map_x = x * tile_size
            map_y = y * tile_size
            if (x, y) in self.game.map.world_map:
                color = (80, 80, 80, 150)
            else:
                color = (40, 40, 40, 150)
            pg.draw.rect(minimap_surf, color, (map_x, map_y, tile_size - 1, tile_size - 1))

        # Draw visible areas
        for y, row in enumerate(self.game.map.mini_map):
            for x, col in enumerate(row):
                if (x - px) ** 2 + (y - py) ** 2 <= radius ** 2:
                    map_x = x * tile_size
                    map_y = y * tile_size
                    if col:
                        color = (200, 200, 200, 255)
                    else:
                        color = (60, 60, 60, 255)
                    pg.draw.rect(minimap_surf, color, (map_x, map_y, tile_size - 1, tile_size - 1))

        # Draw NPCs with threat indicators
        for npc in self.game.object_handler.npc_list:
            if npc.alive and (npc.x - px) ** 2 + (npc.y - py) ** 2 <= radius ** 2:
                map_x = int(npc.x * tile_size)
                map_y = int(npc.y * tile_size)
                # Pulsing effect for enemies
                pulse = abs(math.sin(pg.time.get_ticks() * 0.005))
                enemy_color = (255, 0, 0, 255)
                pg.draw.circle(minimap_surf, enemy_color, (map_x, map_y), 3)
                # Threat radius
                pg.draw.circle(minimap_surf, (255, 0, 0, 50), (map_x, map_y), 
                             int(5 + 2 * pulse))

        # Draw player with direction indicator
        map_x = int(px * tile_size)
        map_y = int(py * tile_size)
        pg.draw.circle(minimap_surf, (0, 255, 0, 255), (map_x, map_y), 4)
        
        # Draw player direction
        direction_x = map_x + 8 * math.cos(self.game.player.angle)
        direction_y = map_y + 8 * math.sin(self.game.player.angle)
        pg.draw.line(minimap_surf, (0, 255, 0, 255), (map_x, map_y), 
                    (direction_x, direction_y), 2)

        # Draw the minimap
        self.screen.blit(minimap_surf, map_pos)

    def game_over(self):
        """Displays game over screen with stats"""
        self.screen.blit(self.game_over_image, (0, 0))
        restart_text = self.font.render('Press R to Restart', True, (255, 255, 255))
        text_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT - 100))
        self.screen.blit(restart_text, text_rect)

    def victory(self):
        """Displays victory screen with stats"""
        self.screen.blit(self.victory_image, (0, 0))
        restart_text = self.font.render('Press R to Play Again', True, (255, 255, 255))
        text_rect = restart_text.get_rect(center=(WIDTH / 2, HEIGHT - 100))
        self.screen.blit(restart_text, text_rect)

    def player_damage(self):
        """Triggers damage effect when player is hit"""
        self.damage_alpha = 255

    def weapon_shot_flash(self):
        """Triggers muzzle flash effect when weapon is fired"""
        self.flash_alpha = 255

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Loads and scales a texture from file"""
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """Loads wall textures with variations"""
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/1.png'),
            3: self.get_texture('resources/textures/1.png'),
            4: self.get_texture('resources/textures/1.png'),
            5: self.get_texture('resources/textures/1.png'),
        }

    def render_game_objects(self):
        """Renders all game objects with depth sorting"""
        list_objects = sorted(self.game.raycasting.objects_to_render, 
                            key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)