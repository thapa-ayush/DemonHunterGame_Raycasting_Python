from settings import *
import pygame as pg
import math


class Player:
    """
    Player class handling movement, combat, health, and player state.
    Implements smooth movement, head bobbing, and various gameplay mechanics.
    """
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.rel = 0
        self.health = PLAYER_MAX_HEALTH
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()
        self.is_alive = True
        
        # Movement variables
        self.velocity_x = 0  # For smooth acceleration
        self.velocity_y = 0
        self.acceleration = 0.4
        self.deceleration = 0.2
        self.max_velocity = 0.5
        
        # Head bobbing effect
        self.bob_phase = 0
        self.bob_amplitude = 0.06
        self.bob_freq = 0.9
        
        # Combat variables
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_recovery_rate = 0.5
        self.sprint_drain_rate = 1
        self.is_sprinting = False
        
        # Footstep sounds
        self.footstep_delay = 400  # ms
        self.last_footstep = 0
        
        # Combat stats
        self.kills = 0
        self.accuracy = 0
        self.shots_fired = 0
        self.shots_hit = 0

    def update(self):
        """Update player state each frame"""
        if self.is_alive:
            self.movement()
            self.mouse_control()
            self.recovery_health()
            self.recover_stamina()
            self.update_head_bob()
            self.play_footstep_sounds()

    def movement(self):
        """Handle player movement with smooth acceleration/deceleration"""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        # Get keyboard input
        keys = pg.key.get_pressed()
        
        # Handle sprinting
        self.is_sprinting = keys[pg.K_LSHIFT] and self.stamina > 0
        if self.is_sprinting:
            speed *= 1.5
            self.stamina = max(0, self.stamina - self.sprint_drain_rate)
        
        # Calculate movement direction
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        # Apply smooth acceleration
        target_vel_x = dx
        target_vel_y = dy
        
        # Accelerate or decelerate towards target velocity
        if abs(target_vel_x) > 0:
            self.velocity_x += (target_vel_x - self.velocity_x) * self.acceleration
        else:
            self.velocity_x *= (1 - self.deceleration)
            
        if abs(target_vel_y) > 0:
            self.velocity_y += (target_vel_y - self.velocity_y) * self.acceleration
        else:
            self.velocity_y *= (1 - self.deceleration)

        # Clamp velocities
        self.velocity_x = max(min(self.velocity_x, self.max_velocity), -self.max_velocity)
        self.velocity_y = max(min(self.velocity_y, self.max_velocity), -self.max_velocity)

        # Apply movement with collision detection
        self.check_wall_collision(self.velocity_x, self.velocity_y)

    def update_head_bob(self):
        """Update head bobbing effect based on movement"""
        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        if speed > 0.01:
            self.bob_phase += self.bob_freq * speed
            return math.sin(self.bob_phase) * self.bob_amplitude
        return 0

    def play_footstep_sounds(self):
        """Play footstep sounds based on movement"""
        speed = math.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)
        current_time = pg.time.get_ticks()
        
        if speed > 0.1 and current_time - self.last_footstep > self.footstep_delay:
            self.last_footstep = current_time
            # Adjust delay based on sprint
            self.footstep_delay = 300 if self.is_sprinting else 400
            # Play footstep sound (assuming sound is implemented in game.sound)
            if hasattr(self.game.sound, 'footstep'):
                self.game.sound.footstep.play()

    def recover_stamina(self):
        """Handle stamina recovery"""
        if not self.is_sprinting:
            self.stamina = min(self.max_stamina, 
                             self.stamina + self.stamina_recovery_rate)

    def recovery_health(self):
        """Handle health recovery over time"""
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        """Check if enough time has passed for health recovery"""
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
        return False

    def get_damage(self, damage):
        """Handle player taking damage with screen effects"""
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        
        # Screen shake effect
        self.game.object_renderer.screen_shake = 20
        
        if self.health < 1:
            self.is_alive = False
            self.check_game_over()

    def is_targeting_enemy(self):
        """Check if player is aiming at an enemy"""
        return any(npc.ray_cast_value and npc.alive 
                  for npc in self.game.object_handler.npc_list)

    def single_fire_event(self, event):
        """Handle shooting events with recoil and effects"""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.shot = True
                self.game.weapon.reloading = True
                self.game.sound.shotgun.play()
                self.game.object_renderer.weapon_shot_flash()
                self.shots_fired += 1
                
                # Check for hits and update accuracy
                if self.is_targeting_enemy():
                    self.shots_hit += 1
                self.accuracy = (self.shots_hit / self.shots_fired) * 100 if self.shots_fired > 0 else 0

    def check_wall_collision(self, dx, dy):
        """Handle collision detection with walls"""
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def check_wall(self, x, y):
        """Check if position is walkable"""
        return (x, y) not in self.game.map.world_map

    def mouse_control(self):
        """Handle mouse look with smooth movement"""
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def check_game_over(self):
        """Handle game over state"""
        if not self.is_alive:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    @property
    def pos(self):
        """Get player position"""
        return self.x, self.y

    @property
    def map_pos(self):
        """Get player position on map grid"""
        return int(self.x), int(self.y)