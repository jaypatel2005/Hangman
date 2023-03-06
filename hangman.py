import pygame
import random
import sys
from colors import *
from Button import Button

WIDTH, HEIGHT = 800, 600

letters = [chr(ascii) for ascii in range(65, 91)]
letter_button = []

GAP = 20
RADIUS = 20
    
startX = (WIDTH - (GAP + RADIUS*2)*13)/2 + GAP/2 
startY = HEIGHT - ((GAP)*2 + RADIUS*4)

for i in range(len(letters)):
    x = startX + (i % 13)*(GAP + RADIUS*2)
    y = startY + (i//13)*(GAP + RADIUS*2)

    letter_button.append([Button(x, y, RADIUS*2, RADIUS*2, color=WHITE, text=letters[i], fColor=BLACK, fSize=25, fStyle='lucidasans', padx=12, pady=1), letters[i]])
    
images = []
for i in range(7):
    images.append(pygame.image.load(f'hangman{i}.png'))

global hangman_status
hangman_status = 0

with open('words.txt', 'r') as f:
    allText = f.read()
    words = list(map(str, allText.split()))

word = random.choice(words).upper()
guessed = []

word_font = pygame.font.SysFont('lucidasans', 40)
title_font = pygame.font.SysFont('lucidasans', 50)

def redrawWindow(win, text):
    win.fill(WHITE)

    title_text = title_font.render("Guess the word", 1, BLACK)
    win.blit(title_text, ((WIDTH - title_text.get_width())//2, 20))

    render_text = word_font.render(text, 1, BLACK)
    win.blit(render_text, ((1150 - render_text.get_width())//2, 250))

    for button in letter_button:
        pygame.draw.circle(win, ORANGE, (button[0].x + RADIUS, button[0].y + RADIUS), RADIUS + 5)
        button[0].draw(win, radius=RADIUS, hoverColor=ORANGE)

    win.blit(images[hangman_status], (120, 170))
    
    pygame.display.update()

def endScreen(win, text):
    win.fill(BLACK)
    font = pygame.font.SysFont('lucidasans', 50)
    render_text1 = font.render(text, 1, WHITE)
    render_text2 = font.render(f"The word is {word}", 1, WHITE)
    restart_button = Button(WIDTH/2 - 70, (HEIGHT + render_text1.get_height() + render_text2.get_height())//2, 140, 40, text="Play again"
    , fColor=BLACK, color=GREEN, fStyle='lucidasans', fSize=25)

    exit_button = Button(WIDTH/2 - 32, (HEIGHT + render_text1.get_height() + render_text2.get_height())//2 + 60, 64, 40, text="Exit"
    , fColor=BLACK, color=DARK_RED, fStyle='lucidasans', fSize=25)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.isOver():
                    return True
                elif restart_button.isOver():
                    restart()
                    return False

        win.blit(render_text1, ((WIDTH - render_text1.get_width())//2, (HEIGHT - render_text1.get_height() - render_text2.get_height())//2 - 10))
        win.blit(render_text2, ((WIDTH - render_text2.get_width())//2, (HEIGHT - render_text2.get_height())//2 + 10))
        restart_button.draw(win, hoverColor=LIME, radius=3)
        exit_button.draw(win, hoverColor=RED, radius=3)

        pygame.display.update()

def restart():
    global word, hangman_status, letters, letter_button, guessed
    word = random.choice(words).upper()
    hangman_status = 0

    letters = [chr(ascii) for ascii in range(65, 91)]
    letter_button = []

    for i in range(len(letters)):
        x = startX + (i % 13)*(GAP + RADIUS*2)
        y = startY + (i//13)*(GAP + RADIUS*2)

        letter_button.append([Button(x, y, RADIUS*2, RADIUS*2, color=WHITE, text=letters[i], fColor=BLACK, fSize=25, fStyle='lucidasans', padx=12, pady=1), letters[i]])
    
    guessed = []
       
def main(FPS=60, WIDTH=WIDTH, HEIGHT=HEIGHT):
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hangman Game!')
    running  = True
    clock = pygame.time.Clock()
    global hangman_status
    global word

    while running:
        clock.tick(FPS)
        
        text = ''
        for letter in word:
            if letter in guessed:
                text += letter + ' '
            else:
                text += '_ '
        redrawWindow(win, text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in letter_button:
                    if button[0].isOver():
                        if button[1] in word:
                            guessed.append(button[1])
                        else:
                            hangman_status += 1

                        letter_button.remove(button)
                        
        if hangman_status == 6:
            redrawWindow(win, text)
            pygame.time.delay(700)
            if endScreen(win, "You Lost!"):
                running = False
            hangman_status = 0

        if '_' not in text:
            redrawWindow(win, text)
            pygame.time.delay(700)
            if endScreen(win, "You Won!"):
                running = False
            hangman_status = 0
            
    # pygame.quit()

if __name__ == "__main__":
    main()