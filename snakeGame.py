import pygame
import random

def show_game_over_menu(screen, game_over_sound):
    game_over_sound.play()
    font = pygame.font.SysFont(None, 48)
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(restart_text, (220, 220))
        screen.blit(quit_text, (250, 300))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    return "quit"

def show_main_menu(screen):
    font = pygame.font.SysFont(None, 72)
    title_text = font.render("Snake Game", True, (0, 255, 0))
    font_small = pygame.font.SysFont(None, 48)
    start_text = font_small.render("Press S to Start", True, (255, 255, 255))
    quit_text = font_small.render("Press Q to Quit", True, (255, 255, 255))
    while True:
        screen.fill((34, 139, 34))  # Jungle green background
        screen.blit(title_text, (220, 120))
        screen.blit(start_text, (250, 250))
        screen.blit(quit_text, (250, 320))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return "start"
                elif event.key == pygame.K_q:
                    return "quit"

def show_pause_menu(screen):
    font = pygame.font.SysFont(None, 72)
    pause_text = font.render("Paused", True, (255, 255, 0))
    font_small = pygame.font.SysFont(None, 48)
    resume_text = font_small.render("Press P to Resume", True, (255, 255, 255))
    quit_text = font_small.render("Press Q to Quit", True, (255, 255, 255))
    while True:
        screen.fill((34, 139, 34))
        screen.blit(pause_text, (300, 180))
        screen.blit(resume_text, (220, 280))
        screen.blit(quit_text, (250, 350))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"
                elif event.key == pygame.K_q:
                    return "quit"

def random_food_position(snake):
    while True:
        x = random.randint(0, 79) * 10
        y = random.randint(0, 59) * 10
        if (x, y) not in snake:
            return (x, y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Load background image
    bg_image = pygame.image.load("jungle_bg.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, (800, 600))

    # Load sounds
    eat_sound = pygame.mixer.Sound("eat.mp3")
    game_over_sound = pygame.mixer.Sound("game_over.mp3")

    # Show main menu first
    menu_choice = show_main_menu(screen)
    if menu_choice == "quit":
        pygame.quit()
        return

    while True:  # This loop allows restarting
        snake = [(100, 100), (90, 100), (80, 100)]
        snake_dir = (10, 0)
        food = random_food_position(snake)
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
                    if event.key == pygame.K_p:
                        paused = True
            if paused:
                pause_choice = show_pause_menu(screen)
                if pause_choice == "resume":
                    paused = False
                elif pause_choice == "quit":
                    pygame.quit()
                    return
                continue

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and snake_dir != (0, 10):
                snake_dir = (0, -10)
            elif keys[pygame.K_DOWN] and snake_dir != (0, -10):
                snake_dir = (0, 10)
            elif keys[pygame.K_LEFT] and snake_dir != (10, 0):
                snake_dir = (-10, 0)
            elif keys[pygame.K_RIGHT] and snake_dir != (-10, 0):
                snake_dir = (10, 0)
            new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

            # Wall wrap-around logic
            new_x = new_head[0]
            new_y = new_head[1]
            if new_x < 0:
                new_x = 790
            elif new_x >= 800:
                new_x = 0
            if new_y < 0:
                new_y = 590
            elif new_y >= 600:
                new_y = 0
            new_head = (new_x, new_y)

            # Self collision check
            if new_head in snake:
                choice = show_game_over_menu(screen, game_over_sound)
                if choice == "restart":
                    running = False
                else:
                    pygame.quit()
                    return

            snake.insert(0, new_head)

            # Food collision check
            if new_head == food:
                eat_sound.play()
                food = random_food_position(snake)
            else:
                snake.pop()

            # Draw background
            screen.blit(bg_image, (0, 0))
            # Draw food
            pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], 10, 10))
            # Draw snake
            for segment in snake:
                pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], 10, 10))
            pygame.display.flip()
            clock.tick(15)

if __name__ == "__main__":
    main()