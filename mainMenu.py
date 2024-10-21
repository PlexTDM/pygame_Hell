import pygame, sys
from Button import Button
from main import main


pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Backgrounds/Main Menu/Background.png")
hover_SFX = pygame.mixer.Sound("./assets/FX/menu/menu.mp3")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("./assets/Backgrounds/Main Menu/font.ttf", size)

def play():
    main()
def options():
        pygame.display.update()

def main_menu():
    pygame.init()
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("./assets/Backgrounds/Main Menu/Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("./assets/Backgrounds/Main Menu/Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("./assets/Backgrounds/Main Menu/Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    hover_SFX.play()
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    hover_SFX.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    hover_SFX.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == '__main__':
    main_menu()