from sprite_object import *
import math
import random

class Weapon(AnimatedSprites):
    """
    Weapon class handling shooting mechanics, animations, and effects.
    Implements recoil, weapon sway, and dynamic animations.
    """
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        
        # Weapon images and positioning
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.weapon_base_pos = self.weapon_pos  # Store base position for weapon sway
        
        # Shooting mechanics
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50
        self.accuracy = 0.95  # Base accuracy (95%)
        
        # Recoil mechanics
        self.recoil_offset = 0
        self.max_recoil = 50
        self.recoil_recovery_speed = 2.5
        self.recoil_kick = 20
        
        # Weapon sway
        self.sway_offset = {'x': 0, 'y': 0}
        self.sway_phase = 0
        self.sway_amplitude = 1.5
        
        # Ammunition system
        self.max_ammo = 8
        self.current_ammo = self.max_ammo
        self.total_ammo = 32
        self.reload_time = 1000  # ms
        self.last_shot_time = 0
        self.shot_delay = 500  # ms between shots
        
        # Spread pattern
        self.spread_angles = [math.radians(i) for i in range(-15, 16, 5)]  # Shotgun spread pattern
        self.num_pellets = 8
        
        # Visual effects
        self.muzzle_flash_active = False
        self.muzzle_flash_duration = 50  # ms
        self.flash_start_time = 0
        self.shell_ejection_counter = 0

    def update(self):
        """Update weapon state each frame"""
        self.check_animation_time()
        self.animate_shot()
        self.update_weapon_position()
        self.check_reload_state()
        self.update_recoil()
        self.update_muzzle_flash()

    def update_weapon_position(self):
        """Update weapon position with sway and recoil"""
        # Update weapon sway
        self.sway_phase += 0.1
        self.sway_offset['x'] = math.sin(self.sway_phase) * self.sway_amplitude
        self.sway_offset['y'] = math.cos(self.sway_phase * 0.5) * self.sway_amplitude
        
        # Calculate movement-based offset
        movement_offset_x = -self.game.player.velocity_x * 5
        movement_offset_y = -abs(self.game.player.velocity_y * 3)
        
        # Apply head bobbing
        bob_offset = self.game.player.update_head_bob() * 30
        
        # Combine all offsets
        final_x = self.weapon_base_pos[0] + self.sway_offset['x'] + movement_offset_x
        final_y = self.weapon_base_pos[1] + self.sway_offset['y'] + movement_offset_y + bob_offset - self.recoil_offset
        
        self.weapon_pos = (final_x, final_y)

    def update_recoil(self):
        """Handle weapon recoil animation"""
        if self.recoil_offset > 0:
            self.recoil_offset = max(0, self.recoil_offset - self.recoil_recovery_speed)

    def update_muzzle_flash(self):
        """Handle muzzle flash effect"""
        if self.muzzle_flash_active:
            if pg.time.get_ticks() - self.flash_start_time > self.muzzle_flash_duration:
                self.muzzle_flash_active = False

    def check_reload_state(self):
        """Check and handle weapon reload state"""
        keys = pg.key.get_pressed()
        if keys[pg.K_r] and not self.reloading and self.current_ammo < self.max_ammo:
            self.start_reload()

    def start_reload(self):
        """Start the reload animation"""
        if self.total_ammo > 0 and not self.reloading:
            self.reloading = True
            self.frame_counter = 0
            # Play reload sound
            if hasattr(self.game.sound, 'reload'):
                self.game.sound.reload.play()

    def finish_reload(self):
        """Complete the reload process"""
        bullets_needed = self.max_ammo - self.current_ammo
        bullets_available = min(bullets_needed, self.total_ammo)
        self.current_ammo += bullets_available
        self.total_ammo -= bullets_available
        self.reloading = False

    def animate_shot(self):
        """Handle shooting animation with recoil"""
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.finish_reload()
                    self.frame_counter = 0

    def shoot(self):
        """Handle shooting mechanics"""
        current_time = pg.time.get_ticks()
        if (not self.reloading and self.current_ammo > 0 and 
            current_time - self.last_shot_time > self.shot_delay):
            
            self.current_ammo -= 1
            self.last_shot_time = current_time
            self.recoil_offset = min(self.max_recoil, self.recoil_offset + self.recoil_kick)
            self.muzzle_flash_active = True
            self.flash_start_time = current_time
            
            # Calculate spread for each pellet
            for _ in range(self.num_pellets):
                spread = random.uniform(-0.1, 0.1)
                # Apply damage with spread pattern
                # This would connect to your NPC damage system
            
            # Shell ejection effect
            self.shell_ejection_counter += 1
            
            return True
        return False

    def draw(self):
        """Render weapon and effects"""
        # Draw weapon
        self.game.screen.blit(self.images[0], self.weapon_pos)
        
        # Draw muzzle flash
        if self.muzzle_flash_active:
            flash_pos = (self.weapon_pos[0] + 30, self.weapon_pos[1] - 10)
            pg.draw.circle(self.game.screen, (255, 200, 50), flash_pos, 10)
        
        # Draw ammo counter
        self.draw_ammo_counter()

    def draw_ammo_counter(self):
        """Draw ammunition counter HUD"""
        ammo_text = f"{self.current_ammo}/{self.total_ammo}"
        font = pg.font.Font(None, 36)
        text_surface = font.render(ammo_text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (WIDTH - 100, HEIGHT - 50))

    def get_damage(self, distance):
        """Calculate damage based on distance"""
        # Damage falloff over distance
        damage_falloff = max(0.5, 1 - (distance / MAX_DEPTH))
        return int(self.damage * damage_falloff)
