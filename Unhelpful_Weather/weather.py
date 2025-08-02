

import pygame
import sys
import random
import urllib.request
import io

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Unhelpful Weather")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DROPDOWN_COLOR = (50, 50, 50)
DROPDOWN_HOVER = (80, 80, 80)
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.SysFont(None, 32)
large_font = pygame.font.SysFont(None, 48)

# Mapping of destinations to bizarre weather and direct image URLs
destinations = {
    "Paris": [
        ("Lava Rain", "https://i.imgur.com/3ZQ3ZQ3.jpg"),
        ("Snail Blizzard", "https://i.imgur.com/4ZQ4ZQ4.jpg"),
        ("Croissant Tornado", "https://i.imgur.com/5ZQ5ZQ5.jpg")
    ],
    "New York": [
        ("Frog Storm", "https://i.imgur.com/6ZQ6ZQ6.jpg"),
        ("Upside-down Snow", "https://i.imgur.com/7ZQ7ZQ7.jpg"),
        ("Taxi Hurricane", "https://i.imgur.com/8ZQ8ZQ8.jpg")
    ],
    "Tokyo": [
        ("Anime Lightning", "https://i.imgur.com/9ZQ9ZQ9.jpg"),
        ("Sushi Hail", "https://i.imgur.com/0ZQ0ZQ0.jpg"),
        ("Robot Fog", "https://i.imgur.com/1ZQ1ZQ1.jpg")
    ],
    "Cairo": [
        ("Sand Tsunami", "https://i.imgur.com/2ZQ2ZQ2.jpg"),
        ("Camel Cyclone", "https://i.imgur.com/3ZQ3ZQ3.jpg"),
        ("Pyramid Lightning", "https://i.imgur.com/4ZQ4ZQ4.jpg")
    ],
    "Sydney": [
        ("Koala Thunder", "https://i.imgur.com/5ZQ5ZQ5.jpg"),
        ("Boomerang Wind", "https://i.imgur.com/6ZQ6ZQ6.jpg"),
        ("Vegemite Mist", "https://i.imgur.com/7ZQ7ZQ7.jpg")
    ]
}

destination_list = list(destinations.keys())
selected_destination = None
selected_weather = None
background_image = None

# Dropdown settings
dropdown_rect = pygame.Rect(50, 50, 200, 40)
dropdown_open = False

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dropdown_rect.collidepoint(event.pos):
                dropdown_open = not dropdown_open
            elif dropdown_open:
                for i, dest in enumerate(destination_list):
                    item_rect = pygame.Rect(50, 90 + i * 40, 200, 40)
                    if item_rect.collidepoint(event.pos):
                        selected_destination = dest
                        selected_weather, image_url = random.choice(destinations[dest])
                        try:
                            with urllib.request.urlopen(image_url) as url:
                                image_data = url.read()
                                image_file = io.BytesIO(image_data)
                                loaded_image = pygame.image.load(image_file)
                                background_image = pygame.transform.scale(loaded_image, (WIDTH, HEIGHT))
                        except Exception as e:
                            print(f"Failed to load image: {e}")
                            background_image = None
                        dropdown_open = False

    # Draw dropdown
    pygame.draw.rect(screen, DROPDOWN_COLOR, dropdown_rect)
    dropdown_text = font.render("Select Destination", True, TEXT_COLOR)
    screen.blit(dropdown_text, (dropdown_rect.x + 10, dropdown_rect.y + 5))

    if dropdown_open:
        for i, dest in enumerate(destination_list):
            item_rect = pygame.Rect(50, 90 + i * 40, 200, 40)
            mouse_pos = pygame.mouse.get_pos()
            color = DROPDOWN_HOVER if item_rect.collidepoint(mouse_pos) else DROPDOWN_COLOR
            pygame.draw.rect(screen, color, item_rect)
            item_text = font.render(dest, True, TEXT_COLOR)
            screen.blit(item_text, (item_rect.x + 10, item_rect.y + 5))

    # Display selected destination and weather
    if selected_destination and selected_weather:
        dest_text = large_font.render(f"{selected_destination} Weather:", True, WHITE)
        weather_text = font.render(f"{selected_weather}", True, WHITE)
        screen.blit(dest_text, (300, 200))
        screen.blit(weather_text, (300, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
