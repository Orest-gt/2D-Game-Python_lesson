import cv2
import pygame as py
import sys
import time
import random

print("\nFollow chris.mrg in instagram")
print("Shoutout to 'Big_Smoke' in youtube (everyone subscribe)\n")
nametag = input("Enter name: ")

__author__ = "Orestis Gatos"
__year__ = "2025"
__version__ = "1.1"

py.init()

standard_loop_delay = 0.016
FPS = 60

cap = cv2.VideoCapture(r"assets\moonside-lake-bloodborne-moewalls-com.mp4")
fullscreen_mode = False

screen_width = 1280
screen_height = 720
screen_centre_width = screen_width // 2
screen_centre_height = screen_height // 2

ground_y_size = 15
general_platforms_x_size = 200
general_platforms_y_size = 10

platforms = []
objects = []

bias = screen_width // 2 - 100

num_repeats = 120

beginning_wall_size_x = screen_width // 4

beginning_wall = py.Rect(1, 0, beginning_wall_size_x, screen_height)

finish_line_pos_x, finish_line_pos_y = 1960 + bias, screen_height - 1220

finish_line = py.Rect(finish_line_pos_x, finish_line_pos_y + 10, 80, 80)

player_size = 50
player_speed = 10

go_up = False

additional_velocity_y = 0
gravity = 1
jump_strength = -15
on_ground = False
is_jumping = False
is_up = False
is_more_up = False
can_move = True

transitioning = False
transitioning_speed = 2
trans_counter = 0
last_move = 0
delay_per_step = 0
direction = "up"
trans_done = False

player = py.Rect(bias - 50, screen_height - 100, player_size, player_size) # idk i just found 3.5 the perfect number not something else

start_check_point = py.Rect(0, 0, 1, screen_height)
start_point = py.Rect(0, 0, 1, screen_height)
end_check_point = py.Rect(screen_width - 1 + 2000, 0, 1, screen_height)
end_point = py.Rect(screen_width - 1, 0, 1, screen_height)

global_speed = player_speed

can_move_left = True
can_move_right = True

is_looking_left = False
is_looking_right = False

screen = py.display.set_mode((screen_width, screen_height))
py.display.set_caption("The best 2D game from Orestis so far!")
py.event.set_grab(True)
py.mouse.set_visible(False)

shooting_radius = 35
angle = 0

bullet_shooter_center = py.math.Vector2(shooting_radius, 0).rotate(-angle)
bullet_shooter_obj = player.center + bullet_shooter_center
bullet_object_direction = py.Rect(int(bullet_shooter_obj.x), int(bullet_shooter_obj.y), 3, 3)

pistoli = py.image.load(r"pistoli_paixnidi.jpg").convert()
marios = py.image.load(r"assets\super-mario-bros-mario-kart-8-toad-mario-bros-f4a8715ee6bddde717ed2b891c123d6e.png").convert_alpha()
jumping_mario = py.image.load(r"assets\new-super-mario-bros-u-super-mario-64-8-bit-thumbnail.png").convert()
#jumping_mario = jumping_mario.set_colorkey((255, 255, 255), py.RLEACCEL)
background_img = py.image.load(r"assets\1920-x-1080-collection-of-my-fav-wallpapers-part-1-v0-rie6s4t6yza81.png").convert()
finish_line_img = py.image.load(r"assets\finish_line_img2.png").convert_alpha()
finish_line_img =  py.transform.smoothscale(finish_line_img, (80, 80))
marios = py.transform.smoothscale(marios, (player_size, player_size))
jumping_mario = py.transform.smoothscale(jumping_mario, (player_size, player_size))
pistoli = py.transform.smoothscale(pistoli, (20, 8))

finish_line_rect = finish_line_img.get_rect()
finish_line_rect.topleft = (finish_line_pos_x, finish_line_pos_y)

marios_rect = marios.get_rect()
marios_rect.topleft = (player.x, player.y)

jumping_mario_rect = jumping_mario.get_rect()
jumping_mario_rect.topleft = (player.x, player.y)

pistoli_rect = pistoli.get_rect()
pistoli_rect.topleft = (bullet_object_direction.x, bullet_object_direction.y)


ground = py.Rect(screen_centre_width - screen_width // 2, screen_height - ground_y_size, screen_width + 1500, ground_y_size)

platform_1 = py.Rect(200 + bias,screen_height - 80, general_platforms_x_size, general_platforms_y_size)
platform_2 = py.Rect(400 + bias ,screen_height - 160, general_platforms_x_size, general_platforms_y_size)
platform_3 = py.Rect(600 + bias ,screen_height - 240, general_platforms_x_size, general_platforms_y_size)
platform_4 = py.Rect(800 + bias ,screen_height - 320, general_platforms_x_size, general_platforms_y_size)
platform_5 = py.Rect(1000 + bias, screen_height - 400, general_platforms_x_size - 50, general_platforms_y_size)
platform_6 = py.Rect(1200 + bias, screen_height - 480, general_platforms_x_size - 10, general_platforms_y_size)
#platform_7 = py.Rect(1200 + bias, screen_height - 580, general_platforms_x_size + random.randint(-40, 40), general_platforms_y_size + random.randint(-10, 20))
platform_8 = py.Rect(1300 + bias, screen_height - 580, general_platforms_x_size - random.randint(0, 30), general_platforms_y_size - random.randint(0, 10))
platform_9 = py.Rect(1400 + bias, screen_height - 660, general_platforms_x_size + random.randint(-20, 50), general_platforms_y_size + random.randint(-10, 15))
platform_10 = py.Rect(1500 + bias, screen_height - 740, general_platforms_x_size - random.randint(20, 40), general_platforms_y_size + random.randint(0, 10))
platform_11 = py.Rect(1600 + bias, screen_height - 820, general_platforms_x_size + random.randint(-10, 20), general_platforms_y_size - random.randint(5, 10))
platform_12 = py.Rect(1700 + bias, screen_height - 900, general_platforms_x_size - random.randint(15, 30), general_platforms_y_size + random.randint(-5, 15))
platform_13 = py.Rect(1800 + bias, screen_height - 940, general_platforms_x_size + random.randint(0, 40), general_platforms_y_size + random.randint(-10, 20))
platform_14 = py.Rect(1900 + bias, screen_height - 1030, general_platforms_x_size - random.randint(10, 40), general_platforms_y_size - random.randint(5, 10))

platforms.extend([platform_1, platform_2, platform_3, platform_4, platform_5, platform_6, platform_8, platform_9, platform_10, platform_11, platform_12, platform_13, platform_14])

objects.append(start_check_point)
objects.append(end_check_point)
for p in platforms:
    objects.append(p)
#objects.append(ground)
objects.append(beginning_wall)
objects.append(finish_line)
objects.append(finish_line_rect)
objects.append(ground)

fps_clock = py.time.Clock()

running = True

start_time = time.time()

bullet_speed = 10

last_shot = 0

bullets = []
can_shoot = True
cooldown_for_shoot = 300

player_last_y = 0

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    now_time = py.time.get_ticks()

    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    frame = cv2.resize(frame, (screen_width, screen_height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)
    video_play_surface = py.surfarray.make_surface(frame)

    screen.blit(background_img, (0, 0))
    screen.blit(finish_line_img, finish_line_rect.topleft)
    if not is_jumping:
        screen.blit(marios, marios_rect.topleft)
    else:
        screen.blit(jumping_mario, jumping_mario_rect.topleft)
    screen.blit(pistoli, pistoli_rect.topleft)

    dx, dy = py.mouse.get_rel()
    bullet_shooter_center = py.math.Vector2(shooting_radius, 0).rotate(-angle)
    bullet_shooter_obj = player.center + bullet_shooter_center
    bullet_object_direction = py.Rect(int(bullet_shooter_obj.x), int(bullet_shooter_obj.y), 3, 3)
    #py.draw.rect(screen, (70, 30, 40), bullet_object_direction)

    keys = py.key.get_pressed()
    mouse = py.mouse.get_pressed()
    global_speed = 13 if keys[py.K_LCTRL] else 10
    if mouse[0] and now_time - last_shot >= cooldown_for_shoot:
        bullet_velocity = py.math.Vector2(1, 0).rotate(-angle) * bullet_speed
        bullet_pos = player.center + py.math.Vector2(shooting_radius, 0).rotate(-angle)
        bullet_rect = py.Rect(int(bullet_pos.x), int(bullet_pos.y), 5, 5)
        bullet = {
            "pos": bullet_pos,
            "velocity": bullet_velocity,
            "rect": bullet_rect
        }
        bullets.append(bullet)

        last_shot = now_time
    if keys[py.K_a] and can_move_left and can_move:
        for object_ in objects:
            object_.x += global_speed
        is_looking_left = True
        is_looking_right = False
    if keys[py.K_d] and can_move_right and can_move:
        for object_ in objects:
            object_.x -= global_speed
        is_looking_left = False
        is_looking_right = True
    if keys[py.K_SPACE] and on_ground and can_move:
        additional_velocity_y = jump_strength
        on_ground = False
        is_jumping = True
    if keys[py.K_f] and not fullscreen_mode:
        screen = py.display.set_mode((screen_width, screen_height), py.FULLSCREEN)
        fullscreen_mode = True
    if keys[py.K_f] and fullscreen_mode:
        screen = py.display.set_mode((screen_width, screen_height))
        fullscreen_mode = False

    for b in bullets:
        b["pos"] += b["velocity"]
        b["rect"].topleft = b["pos"]
        py.draw.rect(screen, (255, 0, 0), b["rect"])

    angle -= dx
    additional_velocity_y += gravity

    ''''''
    steps = abs(int(additional_velocity_y))
    step_dir = 1 if additional_velocity_y > 0 else -1

    for _ in range(steps):
        player.y += step_dir
        hit_platform = False
        for platforma in platforms:
            if player.colliderect(platforma) and step_dir > 0 and player.bottom <= platforma.top + 5:   # CHATGPT PART (sorry)
                player.bottom = platforma.top
                additional_velocity_y = 0
                on_ground = True
                hit_platform = True
                is_jumping = False
                break
        if hit_platform:
            break
    ''''''

    if player.colliderect(ground) and additional_velocity_y >= 0:
        player.bottom = ground.top
        additional_velocity_y = 0
        on_ground = True
        is_jumping = False

    for bullet in bullets[:]: # antigrafoume tin lista gia na min epireasume tin kanoniki
        for platform in platforms:
            if bullet["rect"].colliderect(platform) or bullet["rect"].colliderect(ground):
                bullets.remove(bullet)
                break
    for bullet in bullets:
        if bullet["rect"].x >= screen_width or bullet["rect"].x <= 0 or bullet["rect"].y <= 0 or bullet["rect"].y >= screen_height:
            bullets.remove(bullet)

    py.draw.rect(screen, (139, 69, 19), ground)

    for platforma in platforms:
        if player.colliderect(platforma):
            if additional_velocity_y < 0 and player.top <= platforma.bottom < player.bottom:
                # Ο παίκτης ανεβαίνει και χτύπησε κάτω από πλατφόρμα
                player.top = platforma.bottom  # Ακριβής επαναφορά
                additional_velocity_y = -additional_velocity_y # bounce!
            elif player.right > platforma.left > player.left:
                player.right = platforma.left
            elif player.left < platforma.right < player.right:
                player.left = platforma.right


        py.draw.rect(screen, (30, 0, 0), platforma)

    if start_check_point.colliderect(start_point):
        can_move_left = False
    else:
        can_move_left = True

    if end_check_point.colliderect(end_point):
        can_move_right = False
        unlocked_right = True
    else:
        can_move_right = True

    if transitioning:
        if now_time - last_move >= delay_per_step:
            if trans_counter < num_repeats:
                for obj in objects:
                    if direction == "up":
                        obj.y += transitioning_speed
                    else:
                        obj.y += -transitioning_speed * 7
                        if not player.y >= screen_height + 35:
                            transitioning = True
                        else:
                            transitioning = False
                if direction == "up":
                    player.y += transitioning_speed
                    if not player.y >= screen_height + 35:
                        transitioning = True
                    else:
                        transitioning = False
                trans_counter += 1
                last_move = now_time
                trans_done = True
            else:
                transitioning = False
                trans_counter = 0
                trans_done = False

    if player.y <= screen_height // 2 and is_up:
        go_up = True

    if player.y > screen_height // 2 and go_up:
        go_down = True
        go_up = False




    if not transitioning and player.y <= screen_height // 2 and not is_up:# and not is_more_up:
        transitioning = True
        direction = "up"
        if trans_done:
            is_up = True

    if not transitioning and player.y <= 0 and is_up:
        transitioning = True
        direction = "up"
        if trans_done:
            is_up = False

    if not transitioning and player.top <= screen_height and is_up:
        transitioning = True
        direction = "up"
        if trans_done:
            is_up = False

    if transitioning and player.y >= screen_height // 2:
        is_up = False
        transitioning = False

    if player.y >= screen_height:
        direction = "down"
        transitioning = True
        if trans_done:
            is_up = False


    if player.left <= beginning_wall.right < player.right:
        player.left = beginning_wall.right

    current_time = time.time()

    elapsed_time = current_time - start_time - standard_loop_delay

    for bullet in bullets:
        if bullet["rect"].colliderect(finish_line):
            print(f"You won!\nTime:\n{elapsed_time:.1f} seconds")
            running = False

    if player.colliderect(finish_line):
        print(f"You won!\nTime:\n{elapsed_time:.1f} seconds")
        running = False

    py.draw.rect(screen, (139, 69, 19), beginning_wall)

    fps_clock.tick(FPS)

    marios_rect.topleft = (player.x, player.y)
    jumping_mario_rect.topleft = (player.x, player.y)
    pistoli_rect.topleft = (bullet_object_direction.x, bullet_object_direction.y)

    player_last_y = player.y

    py.display.update()

print(f"\nThanks for playing the game {nametag}!\nWe hope we'll see you again!\n"
      f"Author: {__author__}\nYear: {__year__}\nVersion: {__version__}")

cap.release()
py.quit()
sys.exit()

# 400 GRAMMES NAIIIII
