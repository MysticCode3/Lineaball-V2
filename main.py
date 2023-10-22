# Imports
import sys
import pygame
from pygame import *
import time
import Line
import Dot
import Background_Animation
import sparks_game
import math
import random
import Red_Line
from kivy.core.audio import SoundLoader
from collections import deque

# Initialization
pygame.init()

# Screen Dimensions
info = pygame.display.Info()

# screen_width = info.current_w
# screen_height = info.current_h

screen_width = 450
screen_height = 800

# Colors
green = 150, 200, 20
blue = 67, 84, 255
orange = 255, 165, 0
red = 250, 0, 0
purple = 172, 79, 198
gray = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0

# Pause
pause = False
countdown = False
countdown_timer = 3
current_time = 0

# Mouse Variables
cx, cy = (0, 0)
mx, my = (0, 0)

# Lines Variables
x, y = screen_width / 2, screen_height
x2, y2 = 0, 0

# Ball Variables
bx, by = screen_width / 2, screen_height / 2

# Collision Variables
collide = False
red_collide = False

# Velocity For Ball
opp_rec_glob = 0
bx_vel = 0
by_vel = 0
gravity = 3
up = 0

# Game Event Variables
game_start = False
end = False

# Point Variables
points = 0
high_score = 0

# Lists
line_list = []
dot_list = []
animation_list = []
sparks = []
red_list = []

# Background Variables
b_animation_list = []
background_set = False
background_animation = True

bg_blue = (0, 4, 35)
bg_green = (6, 169, 55)
bg_gray = (65, 98, 108)
current_color = 0
bg_color = bg_blue

# Start Screen Variables
start_screen = True
tutorial_active = False
options_menu = False
achievements_menu = False
stats_menu = False

# Sound Variables
sound = True
sound_effects = True

# Death Animation Variables
max_size = 2000
size = 10
width = 1

# Delta Time
last_time = time.time()
dt = 0

# Sound Effects
MAX_CONCURRENT_SOUNDS = 3
active_sounds = deque(maxlen=MAX_CONCURRENT_SOUNDS)

ball_bounce = SoundLoader.load('sounds/ball_tap.ogg')
click = SoundLoader.load('sounds/click.ogg')
death_sound = SoundLoader.load('sounds/death_sound.ogg')
restart_sound = SoundLoader.load('sounds/restart.ogg')

# Background
# Colors (shades of blue)
"""DARK_BLUE = (0, 0, 100)
MEDIUM_BLUE = (0, 0, 150)
LIGHT_BLUE = (0, 0, 200)"""

# Initialize screen shake variables
shake_intensity = 0
shake_duration = 0
shake_timer = 0
shake_offset_x = 0
shake_offset_y = 0

# Stats
line_stats = 0
bounce_stats = 0
updated_stats = False

# Graphics
fancy_graphics = True

# Animations
# End screen text animation
end_screen_txt_loc = screen_height / 5 + 50
current_end_screen_txt_loc = -100

end_screen_high_score_loc = screen_height / 3
current_end_screen_high_score_loc = -100

# Pause animation
first_pause_box_pos = screen_width / 2 - (screen_width / 15) / 2 - 79
current_first_box_pos = -100

second_pause_box_pos = screen_width / 2 - (screen_width / 15) / 2 + 79
current_second_box_pos = screen_width + 100

# Start Screen animation
start_screen_pos = 0
start_screen_txt_offset = 0

# Optimizations
# Start Screen
font = pygame.font.SysFont("Bahnschrift", int(screen_width / 7))
font_small = pygame.font.SysFont("Bahnschrift", int(screen_width / 30))
font_back = pygame.font.SysFont("twcencondensedextra", int(screen_width / 11))
font_small_2 = pygame.font.SysFont("twcencondensedextra", int(screen_width / 19))

title_text = font.render("Lineaball", bool(1), (173, 216, 230))
name = font_small_2.render("Rohan Saxena", bool(1), (173, 216, 230))
how_to_play_button = font_back.render("How to Play", bool(1), (173, 216, 230))
options_button = font_back.render("Settings", bool(1), (173, 216, 230))
achievements_button = font_back.render("Achievements", bool(1), (173, 216, 230))
stats_button = font_back.render("Stats", bool(1), (173, 216, 230))
play_button = font.render("Play", bool(1), (173, 216, 230))
high_score_txt = font_small_2.render(f"High Score: {high_score}", bool(1), (173, 216, 230))

# Sound functions
def play_sound(type_sound):
    global active_sounds
    if type_sound:
        if len(active_sounds) < MAX_CONCURRENT_SOUNDS:
            if sound_effects:
                if len(line_list) < 20:
                    active_sounds.append(type_sound)
                    type_sound.play()


def update():
    global active_sounds

    if len(active_sounds) >= MAX_CONCURRENT_SOUNDS:
        active_sounds.remove(active_sounds[0])


# Ball Effect
def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


# Draw Background
def draw_background():
    global background_set
    global b_animation_list

    s_2 = pygame.Surface((screen_width, screen_height))

    if not background_set:
        background_set = True
        for i in range(0, 10):
            b_animation_list.append(Background_Animation.animation(screen_width, screen_height))
    for animation_obj in b_animation_list:
        animation_obj.draw(s_2)
        if not pause:
            animation_obj.update()

    s_2.set_alpha(128)
    screen.blit(s_2, (0, 0))


# Death Animation Function
def death_animation():
    global max_size
    global size
    global width

    if fancy_graphics:
        pygame.draw.circle(screen, red, (bx, by), size, width)
        pygame.draw.circle(screen, red, (bx, by), size / 2, width)
    if size < max_size * screen_width:
        size += width
        width += 1
    if size < max_size / 2:
        sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(120, 360)), random.randint(3, 6), red, 1))
    if width < 3:
        try:
            play_sound(death_sound)
            apply_screenshake(2, 200, pygame.time.get_ticks())
        except:
            pass


# Title Screen
def draw_tutorial():
    global tutorial_active

    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill(bg_color)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 7)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 10, 1)

    how_to_play_txt = font.render("How to Play", bool(1), (173, 216, 230))
    s.blit(how_to_play_txt, (screen_width / 2 - how_to_play_txt.get_width() / 2, int(screen_height / 5.8)))

    first_line_txt = font_small_change.render("A simple endless game where you have to keep the ball", bool(1), (173, 216, 230))
    s.blit(first_line_txt, (screen_width / 2 - first_line_txt.get_width() / 2, int(screen_height / 3.5)))
    second_line_txt = font_small_change.render("from touching the bottom/sides of the screen", bool(1), (173, 216, 230))
    s.blit(second_line_txt, (screen_width / 2 - second_line_txt.get_width() / 2, int(screen_height / 3.2)))

    third_line_txt = font_small_change.render("There are also obstacles that will spawn from the top", bool(1), (173, 216, 230))
    s.blit(third_line_txt, (screen_width / 2 - third_line_txt.get_width() / 2, int(screen_height / 2.7)))
    fourth_line_txt = font_small_change.render("of the screen that you have to weave through", bool(1), (173, 216, 230))
    s.blit(fourth_line_txt, (screen_width / 2 - fourth_line_txt.get_width() / 2, int(screen_height / 2.53)))

    screen.blit(s, (0, 0))


def draw_options():
    global options_menu
    global cx, cy
    global sound_effects
    global background_animation
    global fancy_graphics
    is_sound = 0
    is_bg_anim = 0
    is_f_graphics = 0

    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill(bg_color)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 7)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 10, 1)

    settings_txt = font.render("Settings", bool(1), (173, 216, 230))
    s.blit(settings_txt, (screen_width / 2 - settings_txt.get_width() / 2, int(screen_height / 5.8)))

    # Sound Settings
    sound_txt = font_back.render("Sound Effects", bool(1), (173, 216, 230))
    s.blit(sound_txt, (screen_width / 2 - sound_txt.get_width() / 2, int(screen_height / 3.5)))

    if sound_effects:
        is_sound = 0
    else:
        is_sound = 1

    pygame.draw.rect(s, (173, 216, 230), ((screen_width / 2 - screen_width / 30, int(screen_height / 3.2) + screen_width / 15), (screen_width / 15, screen_width / 15)), is_sound, 5)
    if screen_width / 2 - screen_width / 30 < cx < screen_width / 2 - screen_width / 30 + screen_width / 15:
        if int(screen_height / 3.2) + screen_width / 15 < cy < int(screen_height / 3.2) + screen_width / 15 + screen_width / 15:
            cx, cy = -15, -15
            if sound_effects:
                sound_effects = False
            else:
                sound_effects = True

    # Background Settings
    background_txt = font_back.render("Background Animation", bool(1), (173, 216, 230))
    s.blit(background_txt, (screen_width / 2 - background_txt.get_width() / 2, int(screen_height / 2.4)))

    if background_animation:
        is_bg_anim = 0
    else:
        is_bg_anim = 1

    pygame.draw.rect(s, (173, 216, 230), ((screen_width / 2 - screen_width / 30, int(screen_height / 2.25) + screen_width / 15), (screen_width / 15, screen_width / 15)), is_bg_anim, 5)

    if screen_width / 2 - screen_width / 30 < cx < screen_width / 2 - screen_width / 30 + screen_width / 15:
        if int(screen_height / 2.25) + screen_width / 15 < cy < int(screen_height / 2.25) + screen_width / 15 + screen_width / 15:
            cx, cy = -15, -15
            if background_animation:
                background_animation = False
            else:
                background_animation = True

    # Graphics Settings
    background_txt = font_back.render("Fancy Graphics", bool(1), (173, 216, 230))
    s.blit(background_txt, (screen_width / 2 - background_txt.get_width() / 2, int(screen_height / 1.85)))

    if fancy_graphics:
        is_f_graphics = 0
    else:
        is_f_graphics = 1

    pygame.draw.rect(s, (173, 216, 230), ((screen_width / 2 - screen_width / 30, int(screen_height / 1.75) + screen_width / 15), (screen_width / 15, screen_width / 15)), is_f_graphics, 5)

    if screen_width / 2 - screen_width / 30 < cx < screen_width / 2 - screen_width / 30 + screen_width / 15:
        if int(screen_height / 1.75) + screen_width / 15 < cy < int(screen_height / 1.75) + screen_width / 15 + screen_width / 15:
            cx, cy = -15, -15
            if fancy_graphics:
                fancy_graphics = False
            else:
                fancy_graphics = True

    screen.blit(s, (0, 0))


def draw_achievements():
    global cx, cy
    global line_stats, bounce_stats
    global updated_stats

    if not updated_stats:
        draw_stats()
        updated_stats = True

    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill(bg_color)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 7)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 10, 1)

    achievements_list = []
    y_positions = [3.5, 2.8, 2.35, 2.03, 1.78, 1.58, 1.42, 1.29, 1.18]

    achievements_txt = font.render("Achievements", bool(1), (173, 216, 230))
    s.blit(achievements_txt, (screen_width / 2 - achievements_txt.get_width() / 2, int(screen_height / 5.8)))

    # Points
    if high_score >= 25:
        achievements_list.append("- Reach 25 points!")
    if high_score >= 50:
        achievements_list.append("- Reach 50 points!")
    if high_score >= 100:
        achievements_list.append("- Reach 100 points!")

    if line_stats == "":
        line_stats = 0

    # Lines created
    if int(line_stats) >= 100:
        achievements_list.append("- Create 100 lines!")
    if int(line_stats) >= 200:
        achievements_list.append("- Create 200 lines!")
    if int(line_stats) >= 500:
        achievements_list.append("- Create 500 lines!")

    if bounce_stats == "":
        bounce_stats = 0

    # Bounces
    if int(bounce_stats) >= 50:
        achievements_list.append("- Bounce 50 times!")
    if int(bounce_stats) >= 100:
        achievements_list.append("- Bounce 100 times!")
    if int(bounce_stats) >= 200:
        achievements_list.append("- Bounce 200 times!")

    # If no achievements
    if high_score < 25 and int(line_stats) < 100 and int(bounce_stats) < 50:
        nonetxt = font_back.render("You currently have no", bool(1), (173, 216, 230))
        s.blit(nonetxt, (screen_width / 2 - nonetxt.get_width() / 2, int(screen_height / 3.5)))
        nonetxt2 = font_back.render("achievements unlocked", bool(1), (173, 216, 230))
        s.blit(nonetxt2, (screen_width / 2 - nonetxt2.get_width() / 2, int(screen_height / 3)))

    for achievement in achievements_list:
        txt = font_back.render(achievement, bool(1), (173, 216, 230))
        s.blit(txt, (screen_width / 2 - txt.get_width() / 2, int(screen_height / y_positions[achievements_list.index(achievement)])))

    screen.blit(s, (0, 0))


def draw_stats():
    global cx, cy
    global line_stats, bounce_stats

    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    s.fill(bg_color)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 7)
    # pygame.draw.circle(s, (150, 150, 150), (mx, my), 10, 1)

    stats_txt = font.render("Stats", bool(1), (173, 216, 230))
    s.blit(stats_txt, (screen_width / 2 - stats_txt.get_width() / 2, int(screen_height / 5.8)))

    # Line Stats
    # Save files
    file_path = "lines_created.txt"

    # Open the file in read mode
    try:
        file_line_stats = open(file_path, "r")
    except:
        file_line_stats = open(file_path, "w")
        file_line_stats = open(file_path, "r")

    # Read the entire content of the file
    line_stats = file_line_stats.read()

    # Close the file
    file_line_stats.close()

    if line_stats != "":
        line_txt = font_back.render(f"Lines created: {line_stats}", bool(1), (173, 216, 230))
    else:
        line_txt = font_back.render(f"Lines created: 0", bool(1), (173, 216, 230))
    s.blit(line_txt, (screen_width / 2 - line_txt.get_width() / 2, int(screen_height / 3.5)))

    # Bounce Stats
    # Save files
    file_path_b = "total_bounces.txt"

    # Open the file in read mode
    try:
        file_bounce_stats = open(file_path_b, "r")
    except:
        file_bounce_stats = open(file_path_b, "w")
        file_bounce_stats = open(file_path_b, "r")

    # Read the entire content of the file
    bounce_stats = file_bounce_stats.read()

    # Close the file
    file_bounce_stats.close()

    if bounce_stats != "":
        bounce_txt = font_back.render(f"Total bounces: {bounce_stats}", bool(1), (173, 216, 230))
    else:
        bounce_txt = font_back.render(f"Total bounces: 0", bool(1), (173, 216, 230))
    s.blit(bounce_txt, (screen_width / 2 - bounce_txt.get_width() / 2, int(screen_height / 2.8)))

    screen.blit(s, (0, 0))


def draw_title():
    global sound
    global start_screen
    global tutorial_active
    global options_menu
    global achievements_menu
    global stats_menu
    global cx, cy
    global start_screen_pos
    global start_screen_txt_offset
    global title_text, name, how_to_play_button, options_button, achievements_button, stats_button, play_button, high_score

    width_1 = int(screen_width * 0.7)
    height_1 = int(screen_height / 12)

    width = int(screen_width * 0.7)
    height = int(screen_height / 12)

    width_2 = int(screen_width * 0.5)
    height_2 = int(screen_height / 15)

    offset_x = 0
    offset_y = 0

    if int(screen_width / 2) - int(width / 2) - offset_x + width > mx > int(screen_width / 2) - int(width / 2) - offset_x:
        if screen_height - offset_y - int(screen_height / 4.5) + height > my > screen_height - offset_y - int(screen_height / 4.5):
            width = int(screen_width * 0.75)
            height = int(screen_height / 11.5)
            offset_x = int(screen_width / 175)
            offset_y = 10

    if not tutorial_active and not options_menu and not achievements_menu and not stats_menu:
        # Play button
        if int(screen_width / 2) - int(width / 2) - offset_x + width > cx > int(screen_width / 2) - int(width / 2) - offset_x:
            if screen_height - offset_y - int(screen_height / 4.5) + height > cy > screen_height - offset_y - int(screen_height / 4.5):
                if start_screen_pos <= -screen_height:
                    start_screen = False
                    play_sound(click)
                else:
                    start_screen_txt_offset -= start_screen_pos
                    start_screen_pos -= abs((screen_height - start_screen_pos - 1)/8)

        # Tutorial button
        if int(screen_width / 2) - int(width_2 / 2) + width_2 > cx > int(screen_width / 2) - int(width_2 / 2):
            if screen_height - int(screen_height / 3) + height_2 > cy > screen_height - int(screen_height / 3):
                cx, cy = -15, -15
                tutorial_active = True
                play_sound(click)

        # Options button
        if int(screen_width / 2) - int(width_2 / 2) + width_2 > cx > int(screen_width / 2) - int(width_2 / 2):
            if screen_height - int(screen_height / 2.3) + height_2 > cy > screen_height - int(screen_height / 2.3):
                cx, cy = -15, -15
                options_menu = True
                play_sound(click)

        # Achievements button
        if int(screen_width / 2) - int(width_2 / 2) + width_2 > cx > int(screen_width / 2) - int(width_2 / 2):
            if screen_height - int(screen_height / 1.87) + height_2 > cy > screen_height - int(screen_height / 1.87):
                cx, cy = -15, -15
                achievements_menu = True
                play_sound(click)

        # Stats button
        if int(screen_width / 2) - int(width_2 / 2) + width_2 > cx > int(screen_width / 2) - int(width_2 / 2):
            if screen_height - int(screen_height / 1.58) + height_2 > cy > screen_height - int(screen_height / 1.58):
                cx, cy = -15, -15
                stats_menu = True
                play_sound(click)

    # Surface
    s = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    # Update highscore
    high_score_txt = font_small_2.render(f"High Score: {high_score}", bool(1), (173, 216, 230))

    # Title(Lineaball)
    pygame.draw.rect(s, (173, 216, 230), (int(screen_width / 2) - int(width_1 / 2), int(screen_height / 12), width_1, height_1), border_radius=40)

    # Play
    pygame.draw.rect(s, (129, 253, 129), (int(screen_width / 2) - int(width / 2) - offset_x, screen_height - offset_y - int(screen_height / 4.5), width, height), border_radius=40)

    # Tutorial
    pygame.draw.rect(s, (173, 216, 230), (int(screen_width / 2) - int(width_2 / 2), screen_height - int(screen_height / 3), width_2, height_2), border_radius=40)

    # Options
    pygame.draw.rect(s, (173, 216, 230), (int(screen_width / 2) - int(width_2 / 2), screen_height - int(screen_height / 2.3), width_2, height_2), border_radius=40)

    # Achievements
    pygame.draw.rect(s, (173, 216, 230), (int(screen_width / 2) - int(width_2 / 2), screen_height - int(screen_height / 1.87), width_2, height_2), border_radius=40)

    # Stats
    pygame.draw.rect(s, (173, 216, 230), (int(screen_width / 2) - int(width_2 / 2), screen_height - int(screen_height / 1.58), width_2, height_2), border_radius=40)

    # Screen
    s.set_alpha(128)
    screen.blit(s, (0, start_screen_pos))

    # Title
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, int(screen_height / 10) - start_screen_txt_offset))

    # Name
    screen.blit(name, (screen_width / 2 - name.get_width() / 2, int(screen_height / 1.1) - start_screen_txt_offset))

    # Tutorial button
    screen.blit(how_to_play_button, (screen_width / 2 - how_to_play_button.get_width() / 2, screen_height - int(screen_height / 3.2) - start_screen_txt_offset))

    # Settings button
    screen.blit(options_button, (screen_width / 2 - options_button.get_width() / 2, screen_height - int(screen_height / 2.42) - start_screen_txt_offset))

    # Achievements button
    screen.blit(achievements_button, (screen_width / 2 - achievements_button.get_width() / 2, screen_height - int(screen_height / 1.95) - start_screen_txt_offset))

    # Stats button
    screen.blit(stats_button, (screen_width / 2 - stats_button.get_width() / 2, screen_height - int(screen_height / 1.63) - start_screen_txt_offset))

    # Play button
    screen.blit(play_button, (screen_width / 2 - play_button.get_width() / 2, screen_height - int(screen_height / 5) - start_screen_txt_offset))

    # High score text
    screen.blit(high_score_txt, (screen_width / 2 - high_score_txt.get_width() / 2, int(screen_height / 1.07) - start_screen_txt_offset))

    # If statements to update states of different screens
    if tutorial_active:
        draw_tutorial()

    if options_menu:
        draw_options()

    if achievements_menu:
        draw_achievements()

    if stats_menu:
        draw_stats()

def score_animation():
    global font

    font = pygame.font.SysFont("twcencondensedextra", int(screen_width / 4))

# Screenshake
def apply_screenshake(si, sd, st):
    global shake_intensity, shake_duration, shake_timer
    if fancy_graphics:
        shake_intensity = si
        shake_duration = sd  # Duration of the shake in milliseconds
        shake_timer = st


# Collision Detection Between The Ball and The Red Line
def check_red(a, b, c):
    global game_start
    global end

    slope_1 = 0
    slope_2 = 0

    if (b[0] - a[0]) != 0:
        try:
            slope_1 = (b[1] - a[1]) / (b[0] - a[0])
            slope_2 = (b[1] - c[1]) / (b[0] - c[0])
        except:
            pass

    if (b[0] - a[0]) == 0:
        return False

    if abs(slope_2 - slope_1) <= 0.1:
        if a[0] < b[0]:
            if c[0] > a[0]:
                if c[0] < b[0]:
                    game_start = False
                    end = True
                    return True
                else:
                    return False
            else:
                return False
        elif b[0] < a[0]:
            if c[0] > b[0]:
                if c[0] < a[0]:
                    game_start = False
                    end = True
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False


# Collision Detection Between The Ball and The Lines
def check_collision(a, b, c):
    global points
    global shake_intensity, shake_duration, shake_timer

    slope_1 = 0
    slope_2 = 0

    if (b[0] - a[0]) != 0:
        try:
            slope_1 = (b[1] - a[1]) / (b[0] - a[0])
            slope_2 = (b[1] - c[1]) / (b[0] - c[0])
        except:
            pass

    if (b[0] - a[0]) == 0:
        return False, opp_rec_glob

    if abs(slope_2 - slope_1) <= 0.1:
        if a[0] < b[0]:
            if c[0] > a[0]:
                if c[0] < b[0]:
                    points += 1
                    score_animation()
                    add_ball_bounce_count()
                    apply_screenshake(2, 200, pygame.time.get_ticks())
                    try:
                        play_sound(ball_bounce)
                        if fancy_graphics:
                            for i in range(15):
                                # animation_list.append(Line_Animation.dot_anim(bx, by, (67, 84, 255), 0.01, 14))
                                sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(3, 6), blue, 2))
                                sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(3, 5), (175, 215, 215), 1))
                    except:
                        sparks.clear()
                    return True, opp_rec_glob + (slope_1 * 6)
        elif b[0] < a[0]:
            if c[0] > b[0]:
                if c[0] < a[0]:
                    try:
                        play_sound(ball_bounce)
                        apply_screenshake(2, 200, pygame.time.get_ticks())
                        if fancy_graphics:
                            for i in range(15):
                                # animation_list.append(Line_Animation.dot_anim(bx, by, (67, 84, 255), 0.01, 14))
                                sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(3, 6), blue, 2))
                                sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(3, 5), (175, 215, 215), 1))
                    except:
                        sparks.clear()
                    points += 1
                    score_animation()
                    add_ball_bounce_count()
                    return True, opp_rec_glob + (slope_1 * 6)


# Restart Function
def restart_game():
    global layer_offsets, b_animation_list, background_set, points, x, y, x2, y2, bx, by, bx_vel, by_vel, end, opp_rec_glob, game_start, max_size, size, width, red_collide
    layer_offsets = [0, 0, 0]
    b_animation_list = []
    background_set = False
    play_sound(restart_sound)
    for line_obj in line_list:
        line_obj.restart()
    line_list.clear()
    dot_list.clear()
    animation_list.clear()
    sparks.clear()
    points = 0
    x, y = screen_width / 2, screen_height
    x2, y2 = 0, 0
    bx, by = screen_width / 2, screen_height / 2
    bx_vel = 0
    by_vel = 0
    end = False
    opp_rec_glob = 0
    game_start = False
    max_size = 2000
    size = 10
    width = 1
    for red_line_obj in red_list:
        red_line_obj.reset()
    red_collide = False


# Usual Pygame Stuff
pygame.display.set_caption('LineaBall')
# pygame.display.set_icon(Logo)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE, pygame.HWSURFACE)
clock = pygame.time.Clock()

# Initial positions for parallax effect
layer_offsets = [0, 0, 0]
layer_speeds = [0.05, 0.05, 0.05]  # Adjust these speeds for different layers

# Cursor
pygame.mouse.set_visible(False)

# Red Line
for i in range(0, 3):
    red_list.append(Red_Line.RED_LINE(screen_width, -2000))

# Event Loop
while True:
    screen_width, screen_height = screen.get_width(), screen.get_height()
    # Delta Time
    dt = time.time() - last_time
    dt *= 130
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cx, cy = pygame.mouse.get_pos()
            if start_screen == False:
                if end == False:
                    game_start = True
                    if (x, y) == (0, 0):
                        (x, y) = (cx, cy)
                    else:
                        if not pause:
                            if screen_width - screen_width / 60 + 1 - 45 < cx < screen_width - screen_width / 60 + 1 - 45 + screen_width / 30 + 15 and 15 < cy < 15 + screen_width / 15:
                                pass
                            elif 4 < cx < back_button.get_width() + 1 and 2 < cy < back_button.get_height():
                                pass
                            else:
                                try:
                                    play_sound(click)
                                except:
                                    pass
                                add_line_count()
                                (x2, y2) = (cx, cy)
                                line_list.append(Line.LINE((x, y), (x2, y2)))
                                (x, y) = (x2, y2)
                                if fancy_graphics:
                                    for i in range(15):
                                        sparks.append(sparks_game.Spark([x2, y2], math.radians(random.randint(0, 360)), random.randint(3, 5), (175, 215, 215), 1))
                if end:
                    restart_game()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                # pygame.display.iconify()
                pass

        mx, my = pygame.mouse.get_pos()

    keys = pygame.key.get_pressed()

    # Background
    screen.fill(bg_color)

    # Update screen shake
    if shake_intensity > 0:
        current_time_shake = pygame.time.get_ticks()
        if current_time_shake - shake_timer < shake_duration:
            shake_offset_x = random.randint(-shake_intensity, shake_intensity)
            shake_offset_y = random.randint(-shake_intensity, shake_intensity)
        else:
            shake_intensity = 0
            shake_offset_x = 0
            shake_offset_y = 0

    # Fonts
    font = pygame.font.SysFont("twcencondensedextra", int(screen_width / 7))
    font_big = pygame.font.SysFont("twcencondensedextra", int(screen_width / 4))
    font_small = pygame.font.SysFont("twcencondensedextra", 20)
    font_back = pygame.font.SysFont("twcencondensedextra", int(screen_width / 11))
    font_small_change = pygame.font.SysFont("twcencondensedextra", int(screen_width / 25))

    # Main Game Calculations
    if game_start:
        if background_animation:
            draw_background()
        if not pause:
            y += (Line.vel * dt)
            by += (gravity * dt)
            bx += (bx_vel * dt)
            by += (by_vel * dt)

            if collide:
                up = 7 * dt
                collide = False

            if up > 0:
                up -= 0.1 * dt

            by -= up

        try:
            dot_list.append(Dot.PATH(bx, by))
            # sparks.append(sparks_game.Spark([bx, by], math.radians(random.randint(0, 360)), random.randint(6, 10), blue, 2))
        except:
            dot_list.clear()
            # sparks.clear()

        for dot in dot_list:
            dot.draw(screen)
            dot.update()
            if dot.width < 1:
                dot_list.remove(dot)

        for line_obj in line_list:
            line_obj.draw(screen, pause)
            if not pause:
                line_obj.update(screen, dt)
            if fancy_graphics:
                for i in range(7):
                    screen.blit(circle_surf(12 + 3 * i, (20, 20, 20)), (line_obj.second_x - 12 - 3 * i, line_obj.second_y - 12 - 3 * i), special_flags=BLEND_RGB_ADD)

            if not pause:
                try:
                    collide, opp_rec_glob = check_collision((line_obj.first_x, line_obj.first_y), (line_obj.second_x, line_obj.second_y), (bx, by))
                except:
                    pass
            if int(line_obj.first_y) > screen_height:
                if int(line_obj.second_y) > screen_height:
                    line_list.remove(line_obj)
            if not pause:
                bx_vel = opp_rec_glob

            # Draw Red Line As Enemy
        for red_line_obj in red_list:
            red_line_obj.draw(screen)
            if not pause:
                red_line_obj.update(screen_height, dt)
            if not red_collide:
                red_collide = check_red((red_line_obj.x, red_line_obj.y), (red_line_obj.x + 100, red_line_obj.y + 100), (bx, by))

        if not pause:
            for animation in animation_list:
                animation.draw(screen)
                animation.update()
                if animation.width < 1:
                    animation_list.remove(animation)

            for i, spark in sorted(enumerate(sparks), reverse=True):
                spark.move(1)
                spark.draw(screen)
                if spark.color == gray:
                    screen.blit(circle_surf(10, (20, 20, 20)), (spark.loc[0] - 10, spark.loc[1] - 10), special_flags=BLEND_RGB_ADD)
                if not spark.alive:
                    sparks.pop(i)

    # Draw Main Circle
    pygame.draw.circle(screen, blue, (bx, by), 10)
    for i in range(4):
        screen.blit(circle_surf(12 + 3 * i, (20, 20, 20)), (bx - 12 - 3 * i, by - 12 - 3 * i), special_flags=BLEND_RGB_ADD)
    """for i in range(4):
        screen.blit(circle_surf(12 + i ** 2, (20, 20, 20)), (bx - 12 - i ** 2, by - 12 - i ** 2), special_flags=BLEND_RGB_ADD)"""

    # If Death Occurs
    score_shader = font.render(str(points), True, (173, 216, 230))
    screen.blit(score_shader, (screen_width / 2 - (score_shader.get_width() / 2) + 1, screen_height / 10))

    score = font.render(str(points), True, (67, 84, 255))
    screen.blit(score, (screen_width / 2 - (score.get_width() / 2) - 1, screen_height / 10))

    restart = font.render("Click to restart", True, (67, 84, 255))
    final_score = font.render(f"High Score: {high_score}", True, (67, 84, 255))

    restart_shader = font.render("Click to restart", True, (173, 216, 230))
    final_score_shader = font.render(f"High Score: {high_score}", True, (173, 216, 230))

    if end:
        if current_end_screen_txt_loc < end_screen_txt_loc:
            current_end_screen_txt_loc += (-100 + end_screen_txt_loc) / 10
        if current_end_screen_high_score_loc < end_screen_high_score_loc:
            current_end_screen_high_score_loc += (-100 + end_screen_high_score_loc) / 10
    else:
        """end_screen_txt_loc = screen_height / 5 + 50
        current_end_screen_txt_loc = -100

        end_screen_high_score_loc = screen_height / 3
        current_end_screen_high_score_loc = -100"""
        if current_end_screen_txt_loc > -100:
            current_end_screen_txt_loc -= (100 + current_end_screen_txt_loc) / 10
        if current_end_screen_high_score_loc > -100:
            current_end_screen_high_score_loc += (100 + end_screen_high_score_loc) / 10
        if current_end_screen_high_score_loc > screen_height:
            current_end_screen_high_score_loc = -100
    if current_end_screen_txt_loc > 0:
        screen.blit(restart_shader, (screen_width / 2 - (restart.get_width() / 2) + 1, current_end_screen_txt_loc))
        screen.blit(final_score_shader, (screen_width / 2 - (final_score.get_width() / 2) + 1, current_end_screen_high_score_loc))

        screen.blit(restart, (screen_width / 2 - (restart.get_width() / 2) - 1, current_end_screen_txt_loc))
        screen.blit(final_score, (screen_width / 2 - (final_score.get_width() / 2) - 1, current_end_screen_high_score_loc))

    # Check Death
    if bx < 0:
        game_start = False
        end = True
        death_animation()
    elif bx > screen_width:
        game_start = False
        end = True
        death_animation()
    elif by > screen_height:
        game_start = False
        end = True
        death_animation()
    elif red_collide:
        death_animation()

    # Points
    if points > high_score:
        high_score = points

    # Cursor Hover
    # pygame.draw.line(screen, (150, 150, 150), (x, y), (mx, my), 2)
    pygame.draw.circle(screen, (150, 150, 150), (mx, my), 10)
    pygame.draw.circle(screen, (150, 150, 150), (mx, my), 20, 1)

    # Start Screen
    if start_screen:
        b_animation_list = []
        background_set = False
        screen.fill(bg_color)
        # pygame.draw.circle(screen, (150, 150, 150), (mx, my), 7)
        # pygame.draw.circle(screen, (150, 150, 150), (mx, my), 10, 1)
        draw_title()
        clock.tick(130)

    # Back Button
    if not start_screen:
        back_button = font_back.render("Back", True, (67, 84, 255))
        back_button_shader = font_back.render("Back", True, (173, 216, 230))

        screen.blit(back_button, (10 + 1, 7))
        screen.blit(back_button_shader, (10 - 1, 7))

        if 4 < cx < back_button.get_width() + 1:
            if 2 < cy < back_button.get_height():
                cx, cy = 0, 0
                play_sound(click)
                start_screen = True
                start_screen_pos = 0
                start_screen_txt_offset = 0
                restart_game()
    else:
        if tutorial_active or options_menu or achievements_menu or stats_menu:
            back_button = font_back.render("Back", True, (67, 84, 255))
            back_button_shader = font_back.render("Back", True, (173, 216, 230))

            screen.blit(back_button, (10 + 1, 7))
            screen.blit(back_button_shader, (10 - 1, 7))

            if 4 < cx < back_button.get_width() + 1:
                if 2 < cy < back_button.get_height():
                    cx, cy = 0, 0
                    play_sound(click)
                    tutorial_active = False
                    options_menu = False
                    achievements_menu = False
                    stats_menu = False
        else:
            exit_button = font_back.render("Exit", True, (67, 84, 255))
            exit_button_shader = font_back.render("Exit", True, (173, 216, 230))

            screen.blit(exit_button, (10 + 1, 7))
            screen.blit(exit_button_shader, (10 - 1, 7))

            if 4 < cx < exit_button.get_width() + 1:
                if 2 < cy < exit_button.get_height():
                    cx, cy = 0, 0
                    play_sound(click)
                    sys.exit()

    # Pause
    if not start_screen:
        pygame.draw.rect(screen, (67, 84, 255), ((screen_width - screen_width / 60 + 1 - 45, 15), (screen_width / 60, screen_width / 15)))
        pygame.draw.rect(screen, (173, 216, 230), ((screen_width - screen_width / 60 - 1 - 45, 15), (screen_width / 60, screen_width / 15)))
        pygame.draw.rect(screen, (67, 84, 255), ((screen_width - (screen_width / 60) - 10 + 1, 15), (screen_width / 60, screen_width / 15)))
        pygame.draw.rect(screen, (173, 216, 230), ((screen_width - (screen_width / 60) - 10 - 1, 15), (screen_width / 60, screen_width / 15)))

        if screen_width - screen_width / 60 + 1 - 45 < cx < screen_width - screen_width / 60 + 1 - 45 + screen_width / 30 + 15:
            if 15 < cy < 15 + screen_width / 15:
                if pause:
                    countdown = True
                    cx, cy = 0, 0
                else:
                    pause = True
                    cx, cy = 0, 0

        if countdown:
            if current_first_box_pos > -100:
                current_first_box_pos -= (-100 + first_pause_box_pos) / 2
            if current_second_box_pos < screen_width + 100:
                current_second_box_pos += (-100 + first_pause_box_pos) / 2
            countdown_txt = font_big.render(str(countdown_timer), True, (173, 216, 230))
            countdown_txt_shader = font_big.render(str(countdown_timer), True, (67, 84, 255))

            screen.blit(countdown_txt, (screen_width - screen_width / 2 - countdown_txt.get_width() / 2 + 1, screen_height / 2 - countdown_txt.get_height() / 2))
            screen.blit(countdown_txt_shader, (screen_width - screen_width / 2 - countdown_txt.get_width() / 2 - 1, screen_height / 2 - countdown_txt.get_height() / 2))

            if current_time == 0:
                current_time = time.time()

            if int(time.time() - current_time) == 1:
                countdown_timer = 2
            if int(time.time() - current_time) == 2:
                countdown_timer = 1
            if int(time.time() - current_time) == 3:
                countdown_timer = 0

            if countdown_timer <= 0:
                countdown = False
                pause = False
                countdown_timer = 3
                current_time = 0

        if not countdown:
            if pause:
                if current_first_box_pos < first_pause_box_pos:
                    current_first_box_pos += (-100 + first_pause_box_pos) / 4
                current_second_box_pos = screen_width - current_first_box_pos - (screen_width / 15) / 1.4
                if current_first_box_pos > first_pause_box_pos:
                    current_first_box_pos = first_pause_box_pos
        if current_first_box_pos > 0:
            pygame.draw.rect(screen, (67, 84, 255),
                             ((current_first_box_pos, screen_height / 2 - 2 * (screen_width / 15)), ((screen_width / 15), 4 * (screen_width / 15))))
            pygame.draw.rect(screen, (173, 216, 230),
                             ((current_first_box_pos - 2, screen_height / 2 - 2 * (screen_width / 15)), ((screen_width / 15), 4 * (screen_width / 15))))
            pygame.draw.rect(screen, (67, 84, 255),
                             ((current_second_box_pos + 2, screen_height / 2 - 2 * (screen_width / 15)), ((screen_width / 15), 4 * (screen_width / 15))))
            pygame.draw.rect(screen, (173, 216, 230),
                             ((current_second_box_pos, screen_height / 2 - 2 * (screen_width / 15)), ((screen_width / 15), 4 * (screen_width / 15))))


    # Save files
    # High Score
    def write_high():
        # Save files
        file_path = "data.txt"

        # Open the file in write mode
        file = open(file_path, "w")

        # Write content to the file
        file.write(str(high_score))

        # Close the file
        file.close()


    # Open the file in read mode
    try:
        file = open("data.txt", "r")
    except:
        file = open("data.txt", "w")
        file = open("data.txt", "r")

    # Read the entire content of the file
    content = file.read()

    # Close the file
    file.close()

    if content != "":
        if int(content) > int(high_score):
            high_score = int(content)
        else:
            write_high()
    else:
        write_high()


    # Creating/Editing text file with stats for amount of lines created
    def add_line_count():
        # Save files
        file_path = "lines_created.txt"

        # Open the file in read mode
        try:
            file_l = open(file_path, "r")
        except:
            file_l = open(file_path, "w")
            file_l = open(file_path, "r")

        # Read the entire content of the file
        content_l = file_l.read()

        # Close the file
        file_l.close()

        # Open in write mode
        file_lw = open(file_path, "w")

        # Write content to the file
        if content_l == "":
            file_lw.write(str(1))
        else:
            file_lw.write(str(int(content_l) + 1))


    def add_ball_bounce_count():
        # Save files
        file_path = "total_bounces.txt"

        # Open the file in read mode
        try:
            file_b = open(file_path, "r")
        except:
            file_b = open(file_path, "w")
            file_b = open(file_path, "r")

        # Read the entire content of the file
        content_b = file_b.read()

        # Close the file
        file_b.close()

        # Open in write mode
        file_bw = open(file_path, "w")

        # Write content to the file
        if content_b == "":
            file_bw.write(str(1))
        else:
            file_bw.write(str(int(content_b) + 1))


    # Update Sound
    update()

    # Apply screen shake offset
    if shake_intensity > 0:
        screen.blit(screen, (shake_offset_x, shake_offset_y))

    # Sine wave properties
    amplitude = 50  # Amplitude of the sine wave
    frequency = 0.01  # Frequency of the sine wave
    speed_sin = 0.01  # Speed of the wave movement

    if not start_screen:
        # Draw the sine wave border
        for x_sin in range(screen_width):
            y_sin = screen_height // 2 + amplitude * math.sin(frequency * x_sin + speed_sin * pygame.time.get_ticks())
            pygame.draw.circle(screen, (255, 140, 0), (x_sin, int(y_sin) + screen_height / 2), 50)
        for x_sin in range(screen_width):
            y_sin = screen_height // 2 + (amplitude-30) * math.sin(frequency * x_sin + speed_sin * pygame.time.get_ticks())
            pygame.draw.circle(screen, (255, 213, 0), (x_sin+30, int(y_sin) + screen_height / 2 + 20), 50)
        """for y_sin in range(screen_width):
            x_sin = screen_height // 2 + amplitude * math.sin(frequency * y_sin + speed_sin * pygame.time.get_ticks())
            pygame.draw.circle(screen, (20, 20, 20), (int(x_sin) - screen_width/1.2, y_sin + 100), 50)"""

    # FPS and DT
    fps = font_small.render(f"FPS: {round(clock.get_fps())}", True, (173, 216, 230))
    # dt = font_small.render(f"DT: {round(dt, 4)}", True, (173, 216, 230))
    screen.blit(fps, (3, 40))
    # screen.blit(dt, (3, 60))
    # soundAMNT = font_small.render(f"Sound: {len(active_sounds)}", True, (173, 216, 230))
    # screen.blit(soundAMNT, (3, 0))

    pygame.display.flip()
    clock.tick(120)
