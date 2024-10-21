import pygame
from save import UPGRADES1
from Button import Button
def get_font(size):
        return pygame.font.Font("./assets/Backgrounds/Main Menu/font.ttf", size)

class UI:
    def __init__(self, screen, highestScore):
        self.screen = screen
        self.color = (255, 255, 255)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.font = pygame.font.SysFont(None, 30)
        self.highestScore = highestScore
        self.frameCount = 0
        self.gameOver = False

        self.width = screen.get_width()
        self.height = screen.get_height()
    
    # FPS
    def render(self, player, time):
        self.clock.tick()
        screen = self.screen
        fps_text = self.font.render(f'FPS: {self.clock.get_fps():.0f}', True, 'white')
        score_text = self.font.render(f'Score: {player.score}', True, self.color)
        highest_score = self.font.render(f'Highest Score: {self.highestScore}', True, self.color)
        level_text = self.font.render(f'Lvl: {str(player.level)}', True, self.color)
        timer = self.font.render(time, True, self.color)
        screen.blit(fps_text, (10, 10))
        screen.blit(fps_text, (10, 10))
        screen.blit(score_text, (10,30))
        screen.blit(highest_score, (self.screen.get_width()-200,10))
        screen.blit(timer,(self.screen.get_width()/2-15,10))
        screen.blit(level_text, (10,50))

        if player.leveling_up:
            # if self.levelupMenu(player):
            if self.levelUpOptions(player):
                player.leveling_up = False
    
    def deathScreen(self):
        font = pygame.font.SysFont(None, 75)
        text = font.render('You Died', True, (255, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))


    def paused(self, paused, pause_ran):
        screen = self.screen
        if not pause_ran:
            surface = screen
            rect = pygame.Rect(0,0,screen.get_width(),screen.get_height())
            color = (0,0,0,126)
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
            surface.blit(shape_surf, rect)
            pause_ran = True

            TITLE_TEXT = get_font(45).render("Paused", True, "white")
            TITLE_RECT = TITLE_TEXT.get_rect(center=(screen.get_width()//2, 150))
            screen.blit(TITLE_TEXT,TITLE_RECT)
        resume = Button(image=None, pos=(screen.get_width()//2, 500),text_input="Resume", 
                        font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        mouse_pos = pygame.mouse.get_pos()
        resume.changeColor(mouse_pos)
        resume.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume.checkForInput(mouse_pos):
                    paused = False
        return paused, pause_ran
    def levelUpOptions(self, player):

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen = self.screen
        width = self.width
        height = self.height

        bg_width = width - 800
        bg_height = height - 100
        bg_x = (width - bg_width) / 2
        bg_y = (height - bg_height) / 2
        pygame.draw.rect(screen, 'aqua', (bg_x, bg_y, bg_width, bg_height))

        options_x = width//2
        options_y = (height-100)//2/2+100

        TITLE_TEXT = get_font(45).render("Level UP!", True, "#b68f40")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(options_x, 100))

        option1 = Button(image=pygame.image.load("./assets/Backgrounds/Main Menu/Rect.png"), pos=(options_x, options_y),
                            text_input="Attack UP", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        option2 = Button(image=pygame.image.load("./assets/Backgrounds/Main Menu/Rect.png"), pos=(options_x, 400),
                            text_input="Attack speed UP", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        option3 = Button(image=pygame.image.load("./assets/Backgrounds/Main Menu/Rect.png"), pos=(options_x, 550),
                            text_input="Move speed up", font=get_font(25), base_color="#d7fcd4", hovering_color="White")

        screen.blit(TITLE_TEXT,TITLE_RECT)
        
        for button in [option1,option2,option3]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if option1.checkForInput(MENU_MOUSE_POS):
                    player.dmg += 1
                    return True
                if option2.checkForInput(MENU_MOUSE_POS):
                    player.default_attack_speed -= 10
                    return True
                if option3.checkForInput(MENU_MOUSE_POS):
                    player.speed += 10
                    return True
    def levelupMenu(self, player):
        screen = self.screen
        width = self.width
        height = self.height
        
        title_font = pygame.font.SysFont(None, 60, True)
        text_font = pygame.font.SysFont(None, 30)
        # bg

        bg_width = width - 800
        bg_height = height - 100
        bg_x = (width - bg_width) / 2
        bg_y = (height - bg_height) / 2
        pygame.draw.rect(screen, 'aqua', (bg_x, bg_y, bg_width, bg_height))

        options_x = bg_x + 10
        options_y = bg_y + 10
        options_w = width - options_x * 2
        options_h = round((height - 20 - options_y * 2) / 4)

        # bg
        options = []
        options.append(pygame.draw.rect(screen, 'white', (options_x, options_y, options_w, options_h)))
        options.append(pygame.draw.rect(screen, 'red', (options_x, options_y+options_h+10, options_w, options_h)))
        options.append(pygame.draw.rect(screen, 'white', (options_x, options_y+options_h*2+20, options_w, options_h)))

        # player
        text1 = text_font.render(UPGRADES1["penetration"]["name"], True, 'black')
        screen.blit(text1, (options_x + 50, options_y+options_h / 4))
        text1desc = text_font.render(UPGRADES1["penetration"]["description"], True, 'black')
        screen.blit(text1desc, (options_x + 50, options_y+options_h * 0.5))


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in options:
                    if i.collidepoint(pygame.mouse.get_pos()):
                        return True


    def renderHP(self, user):
        hp_width = 80
        hp_height = 10
        bar_x = self.screen.get_width() // 2 - 40
        bar_y = self.screen.get_height() // 2 - 60
        hp = user.hp
        maxHp = user.maxHp
        # background
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, hp_width, hp_height))
        # foreground bar (green)
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, hp_width * (hp / maxHp), hp_height))
