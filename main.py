import pygame
from UI import UI
import save
import level

def main():

    screen = pygame.display.set_mode((save.SC_WIDTH, save.SC_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    paused = False
    pause_ran = False

    dt = 0


    savedData = save.loadGame()

    game = level.Level1()

    ui = UI(screen, savedData["highestScore"],)
    while running:
        # quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if(savedData["highestScore"]<game.player.score):
                    save.saveGame(game.player.score, game.player.kills)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    pause_ran = False
                    clock.tick(0)

        if not paused:

            # render components 
            screen.fill("purple")
            game.update(dt, paused)
        else:
            game.pauseTimer()
            paused, pause_ran = ui.paused(paused, pause_ran)

        pygame.display.flip()

        dt = clock.tick(save.frame_rate) / 1000



    pygame.quit()
if __name__ == '__main__':
    pygame.init()
    main()