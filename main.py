import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nuclear Reactor Control Room")

# Load images
reactor_image = pygame.image.load('reactor.png')
reactor_rect = reactor_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Define fonts
font = pygame.font.SysFont(None, 30)

# Define temperature variables
reactor_temperature = 50

# Define alarm thresholds
ALARM_THRESHOLD_HIGH = 80
ALARM_THRESHOLD_LOW = 20

# Define cooling system parameters
COOLING_RATE = 0.1  # Degrees per frame

# Variable to control alarm initiation
alarm_triggered = False

# Variable to control slider dragging
dragging_slider = False
slider_pos = 0

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if mouse is on the slider
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 50 <= mouse_x <= 750 and 500 <= mouse_y <= 520:
                    dragging_slider = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging_slider = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_slider:
                # Update slider position
                mouse_x, _ = pygame.mouse.get_pos()
                slider_pos = max(0, min(mouse_x - 50, 700))
                # Update reactor temperature based on slider position
                reactor_temperature = slider_pos / 700 * 100 + 50

    # Cooling system
    if not dragging_slider:
        if reactor_temperature > 50:
            reactor_temperature -= COOLING_RATE
        elif reactor_temperature < 50:
            reactor_temperature += COOLING_RATE

    # Check for alarms
    if not alarm_triggered and reactor_temperature >= ALARM_THRESHOLD_HIGH:
        alarm_triggered = True

    if reactor_temperature >= ALARM_THRESHOLD_HIGH:
        alarm_color = RED
    elif reactor_temperature <= ALARM_THRESHOLD_LOW:
        alarm_color = RED
    else:
        alarm_color = BLACK

    # Clear the screen
    screen.fill(WHITE)

    # Draw reactor image
    screen.blit(reactor_image, reactor_rect)

    # Draw temperature slider
    pygame.draw.rect(screen, BLACK, (50, 500, 700, 20))  # Slider base
    pygame.draw.rect(screen, RED, (slider_pos + 50, 495, 5, 30))  # Slider handle

    # Draw temperature text
    temperature_text = font.render(f"Reactor Temperature: {int(reactor_temperature)}°C", True, BLACK)
    screen.blit(temperature_text, (10, 10))

    # Draw alarm text
    if alarm_triggered:
        alarm_text = font.render("ALARM!", True, alarm_color)
        screen.blit(alarm_text, (10, 50))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
