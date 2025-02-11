import math

"""
Game Settings and Configuration
This file contains all the constant values and configurations used throughout the game.
"""

# Display Settings
RES = WIDTH, HEIGHT = 1600, 900  # Game resolution
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60  # Target frames per second

# Player Settings
PLAYER_POS = 1.5, 5  # Starting position (x, y)
PLAYER_ANGLE = 0  # Starting angle (radians)
PLAYER_SPEED = 0.005  # Movement speed
PLAYER_ROT_SPEED = 0.002  # Rotation speed
PLAYER_SIZE_SCALE = 60  # Player hitbox size
PLAYER_MAX_HEALTH = 100  # Maximum player health

# Mouse Control Settings
MOUSE_SENSITIVITY = 0.0003  # Mouse look sensitivity
MOUSE_MAX_REL = 40  # Maximum mouse movement per frame
MOUSE_BORDER_LEFT = 100  # Left screen border for mouse
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT  # Right screen border for mouse

# Visual Settings
FLOOR_COLOR = (30, 30, 30)  # Dark gray floor
SKY_COLOR = (15, 15, 40)  # Dark blue sky for atmosphere
BLOOD_COLOR = (145, 0, 0)  # Dark red for damage effects
HEALTH_COLOR = (0, 145, 0)  # Green for health display

# Weapon Settings
WEAPON_BASE_DAMAGE = 50  # Base weapon damage
WEAPON_SCALE = 0.4  # Weapon sprite scale
WEAPON_RECOIL = 50  # Maximum recoil amount
WEAPON_SWAY = 1.5  # Weapon sway amount
WEAPON_BOB = 0.06  # Weapon bob amount
WEAPON_SPREAD = 15  # Weapon spread in degrees
MAX_PELLETS = 8  # Number of pellets per shot
RELOAD_TIME = 1000  # Reload time in milliseconds
SHOT_DELAY = 500  # Delay between shots

# Movement Settings
ACCELERATION = 0.4  # Player acceleration rate
DECELERATION = 0.2  # Player deceleration rate
MAX_VELOCITY = 0.5  # Maximum player velocity
SPRINT_MULTIPLIER = 1.5  # Speed multiplier when sprinting
HEAD_BOB_SPEED = 0.9  # Speed of head bobbing
HEAD_BOB_AMOUNT = 0.06  # Amount of head bobbing

# Combat Settings
DAMAGE_FALLOFF_START = 5  # Distance at which damage starts falling off
MAX_DAMAGE_RANGE = 20  # Maximum range for full damage
CRITICAL_DISTANCE = 2  # Distance for critical hits
STAMINA_DRAIN_RATE = 1  # Rate at which sprinting drains stamina
STAMINA_REGEN_RATE = 0.5  # Rate of stamina regeneration
HEALTH_REGEN_DELAY = 700  # Delay before health starts regenerating
HEALTH_REGEN_RATE = 1  # Rate of health regeneration

# Raycasting Settings
FOV = math.pi / 3  # Field of view in radians (60 degrees)
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2  # Number of rays to cast
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS  # Angle between rays
MAX_DEPTH = 32  # Maximum ray distance

# Projection Settings
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)  # Distance to projection plane
SCALE = WIDTH // NUM_RAYS  # Scaling factor for walls

# Texture Settings
TEXTURE_SIZE = 256  # Size of wall textures
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# Sound Settings
MUSIC_VOLUME = 0.4  # Background music volume
SFX_VOLUME = 0.6  # Sound effects volume
FOOTSTEP_DELAY = 400  # Delay between footstep sounds
WEAPON_VOLUME = 0.7  # Weapon sound volume

# Enemy Settings
ENEMY_SPEED = 0.03  # Base enemy movement speed
ENEMY_ATTACK_DIST = 1.0  # Distance at which enemies can attack
ENEMY_DAMAGE = 10  # Base enemy damage
ENEMY_HEALTH = {
    'soldier': 100,
    'caco_demon': 150,
    'cyber_demon': 200
}

# Visual Effects
DAMAGE_FADE_SPEED = 5  # Speed of damage indicator fade
MUZZLE_FLASH_DURATION = 50  # Duration of muzzle flash in ms
SCREEN_SHAKE_AMOUNT = 20  # Amount of screen shake on damage
BLOOD_SCREEN_DURATION = 300  # Duration of blood screen effect

# Animation Settings
ANIMATION_SPEED = 10  # Frames per second for animations
WEAPON_ANIMATION_SPEED = 90  # Speed of weapon animations