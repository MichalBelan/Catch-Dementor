import pygame
import random

# Inicializacia hry
pygame.init()

# Obrazovka
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Utok dementora")

# Nastavenie hry
fps = 60
clock = pygame.time.Clock()

# Parametre hry
player_start_lives = 5
dementor_start_speed = 2
dementor_speed_acceleration = 0.5
score = 0

player_lives = player_start_lives
dementor_speed = dementor_start_speed

dementor_x = random.choice([-1, 1])
dementor_y = random.choice([-1, 1])

# Obrazky
background_img = pygame.image.load("img/hogwarts-castle.jpg")
background_img_rect = background_img.get_rect()
background_img_rect.topleft = (0, 0)

dementor_img = pygame.image.load("img/mozkomor.png")
dementor_img_rect = dementor_img.get_rect()
dementor_img_rect.center = (width / 2, height / 2)

# Farby
dark_yellow = pygame.Color("#938f0c")

# Fonty
potter_font_big = pygame.font.Font("fonts/Harry.ttf", 50)
potter_font_middle = pygame.font.Font("fonts/Harry.ttf", 30)

# Text
game_over_text = potter_font_big.render("Game over", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width / 2, height / 2)

continue_text = potter_font_middle.render("Press any button to continue", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width / 2, height / 2 + 50)

# Zvuky
success_click = pygame.mixer.Sound("music/success_click.wav")
miss_click = pygame.mixer.Sound("music/miss_click.wav")
pygame.mixer.music.load("music/bg-music-hp.wav")
success_click.set_volume(0.1)
miss_click.set_volume(0.1)

# Hlavny cykklus
lets_continue = True
pygame.mixer.music.play(-1, 0.0)
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]

            # Bolo kliknute na dementora
            if dementor_img_rect.collidepoint(click_x, click_y):
                success_click.play()
                score += 1
                dementor_speed += dementor_speed_acceleration

                previous_x = dementor_x
                previous_y = dementor_y

                while previous_x == dementor_x and previous_y == dementor_y:
                    dementor_x = random.choice([-1, 1])
                    dementor_y = random.choice([-1, 1])


            else:
                miss_click.play()
                player_lives -= 1

    # Pohybujeme mozkomorem
    dementor_img_rect.x += dementor_x * dementor_speed
    dementor_img_rect.y += dementor_y * dementor_speed

    # Odraz mozkomora
    if dementor_img_rect.left < 0 or dementor_img_rect.right >= width:
        dementor_x = -1 * dementor_x
    elif dementor_img_rect.top < 0 or dementor_img_rect.bottom >= height:
        dementor_y = -1 * dementor_y

    # Upravil som tuto cast, aby dementor nevysiel mimo obrazovku
    if dementor_img_rect.left < 0:
        dementor_img_rect.left = 0
    if dementor_img_rect.right > width:
        dementor_img_rect.right = width
    if dementor_img_rect.top < 0:
        dementor_img_rect.top = 0
    if dementor_img_rect.bottom > height:
        dementor_img_rect.bottom = height

    # Texty
    score_text = potter_font_middle.render(f"Score: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.topright = (width - 30, 10)

    lives_text = potter_font_middle.render(f"Lives: {player_lives}", True, dark_yellow)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.topright = (width - 30, 50)

    # Obrazky
    screen.blit(background_img, background_img_rect)
    screen.blit(dementor_img, dementor_img_rect)

    # Texty
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)

    # Update obrazovky
    pygame.display.update()

    # Spomalenie cyklu
    clock.tick(fps)

    # Kontrola konca hry
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()

        # Pozastavenie hry do dalsieho kliknutia
        pygame.mixer.music.stop()
        paused = True
        while paused:
            # chces hrat znova
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = player_start_lives
                    dementor_speed = dementor_start_speed
                    dementor_img_rect.center = (width / 2, height / 2)
                    dementor_x = random.choice([-1, 1])
                    dementor_y = random.choice([-1, 1])
                    pygame.mixer.music.play(-1, 0.0)
                    paused = False
                elif event.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

# Ukoncenie hry
pygame.quit()
