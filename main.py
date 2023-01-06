import pygame
import math
from pygame.locals import K_w, K_s, K_a, K_d, KEYDOWN, MOUSEBUTTONDOWN
from spider import Spider, SIZE
from projectile import Projectile
from node import Node
# 800x600 -> 50x50px sprites -> 10x10 board = 500x50a0px board
game_screen = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()

BG = pygame.image.load("gfx/background.png").convert()

game_spider = Spider()
nodes = pygame.sprite.Group()

# initial node grid 
nodes.add(Node(2,4))
nodes.add(Node(2,5))
nodes.add(Node(2,3))
nodes.add(Node(3,4))
nodes.add(Node(1,4))
nodes.add(Node(1,3))
nodes.add(Node(1,5))
nodes.add(Node(3,3))
nodes.add(Node(3,5))

for i in range(10):
    for j in range(10):
        node = Node(i,j)
        nodes.add(node)
        if (i,j) in ((2,4), (2,5), (2,3), (3,4), (1,4), 
        (1,3), (1,5), (3,3), (3,5)): # initial grid
            node.visible = True

bullets = pygame.sprite.Group()
if __name__ == "__main__":
    pygame.init()

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    game_spider.update("up", nodes)
                elif event.key == K_s:
                    game_spider.update("down", nodes)
                elif event.key == K_a:
                    game_spider.update("left", nodes)
                elif event.key == K_d:
                    game_spider.update("right", nodes)
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                vector_x, vector_y = mouse_x - game_spider.x, mouse_y - game_spider.y
                bullet_angle = math.degrees(math.atan2(-vector_y, +vector_x))
                
                # rotating the spider
                game_spider.rotate("-", bullet_angle)

                # creating the Projectile
                bullets.add(Projectile(game_spider.x + SIZE // 2,
                                        game_spider.y + SIZE // 2,
                                        vector_x, vector_y,
                                        bullet_angle))

        game_screen.blit(BG, (0,0))
        n: Node
        for n in nodes:
            if n.visible == True:
                n.show(game_screen)

        bullet: Projectile
        for bullet in bullets:
            if bullet.x > 800 or bullet.x < 0 or bullet.y > 600 or bullet.y < 0:
                bullets.remove(bullet)
            else:
                n: Node
                for n in nodes:
                    if bullet.rect.colliderect(n.rect):
                        n.visible = True
                bullet.update()
                bullet.show(game_screen)


        game_spider.show(game_screen)

        clock.tick(30)
        
        pygame.display.flip()
    