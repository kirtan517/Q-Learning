import pygame 
import random
import copy
import math

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


BLOCK_SIZE=100
LINE_WIDTH=9
FONT_SIZE = 50


class gridgame:

    def __init__(self,size,render=False):

        self.size = size
        self.setting_up_display(self.size)
        self.render=render
        self.player_cords,self.goal_cords,self.wall_cords,self.pit_cords= random.sample(self.centers.keys(),4)
        self.centers[self.player_cords]=1
        self.centers[self.wall_cords]=1
        self.centers[self.pit_cords]=1
        self.centers[self.goal_cords]=1
        self.action_set={"u":"Upper","l":"left","d":"down","r":"right"}
        self.action=["l","r","u","d"]
        if render:
            self.display()


    
    def setting_up_display(self,size):

        self.centers={}
        self.line_cords = [] 
        x=BLOCK_SIZE//2
        for i in range(size):
            y=BLOCK_SIZE//2
            for j in range(size):
                self.centers[(x,y)]=0
                if y not in self.line_cords:
                    self.line_cords.append(y)
                y +=LINE_WIDTH+BLOCK_SIZE
            x += LINE_WIDTH+BLOCK_SIZE
        self.WIDTH=BLOCK_SIZE * self.size + LINE_WIDTH * (self.size-1)
        self.font = pygame.font.SysFont("Sans", FONT_SIZE)

    def display(self):

        self.win= pygame.display.set_mode((self.WIDTH,self.WIDTH))
        self.line_cords.pop()
        self.starting_line_cords=[(i+BLOCK_SIZE//2+LINE_WIDTH//2+1,0) for i in self.line_cords]
        self.ending_line_cords=[(i+BLOCK_SIZE//2+LINE_WIDTH//2+1,self.WIDTH) for i in self.line_cords]
        self.left_line_cords=[(0,i+BLOCK_SIZE//2+LINE_WIDTH//2+1) for i in self.line_cords]
        self.right_line_cords=[(self.WIDTH,i+BLOCK_SIZE//2+LINE_WIDTH//2+1) for i in self.line_cords]
        for i in zip(self.starting_line_cords,self.ending_line_cords):
            pygame.draw.line(self.win, RED, i[0], i[1], LINE_WIDTH)
        for i in zip(self.left_line_cords,self.right_line_cords):
            pygame.draw.line(self.win, RED, i[0], i[1], LINE_WIDTH)

        self.player=self.font.render("P",True,WHITE)
        self.win.blit(self.player,(self.player_cords[0]-self.player.get_width()//2,self.player_cords[1]-self.player.get_height()//2))

        self.wall=self.font.render("W",True,WHITE)
        self.win.blit(self.wall,(self.wall_cords[0]-self.wall.get_width()//2,self.wall_cords[1]-self.wall.get_height()//2))

        self.goal=self.font.render("G",True,WHITE)
        self.win.blit(self.goal,(self.goal_cords[0]-self.goal.get_width()//2,self.goal_cords[1]-self.goal.get_height()//2))

        self.pit=self.font.render("L",True,WHITE)
        self.win.blit(self.pit,(self.pit_cords[0]-self.pit.get_width()//2,self.pit_cords[1]-self.pit.get_height()//2))

        pygame.display.update()

    def erase(self,cords):
        surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        surface.fill(BLACK)
        self.win.blit(surface,(cords[0]-BLOCK_SIZE//2,cords[1]-BLOCK_SIZE//2))
        pygame.display.update()

    def redraw(self):
        self.win.blit(self.player,(self.player_cords[0]-self.player.get_width()//2,self.player_cords[1]-self.player.get_height()//2))
        pygame.display.update()


    def get_cords(self,cords):
        
        distance = math.inf
        for i in self.centers:
            d=math.sqrt((cords[0]-i[0])**2+(cords[1]-i[1])**2)
            if d < distance:
                position= i 
                distance = d

        if position == self.wall_cords:
            return self.player_cords
        return position



    def take_action(self,action):
        if action=="u":
            if self.player_cords[1]-BLOCK_SIZE > 0:
                if self.render:
                    self.erase(self.player_cords)
                self.player_cords = self.get_cords((self.player_cords[0],self.player_cords[1]-BLOCK_SIZE))
                if self.render:
                    self.redraw()

        if action=="d":
            if self.player_cords[1]+BLOCK_SIZE < self.WIDTH:
                if self.render:
                    self.erase(self.player_cords)
                self.player_cords =  self.get_cords((self.player_cords[0],self.player_cords[1]+BLOCK_SIZE))
                if self.render:
                    self.redraw()

        if action=="l":
            if self.player_cords[0]-BLOCK_SIZE > 0:
                if self.render:
                    self.erase(self.player_cords)
                self.player_cords = self.get_cords((self.player_cords[0]-BLOCK_SIZE,self.player_cords[1]))
                if self.render:
                    self.redraw()

        if action=="r":
            if self.player_cords[0] + BLOCK_SIZE < (self.WIDTH):
                if self.render:
                    self.erase(self.player_cords)
                self.player_cords = self.get_cords((self.player_cords[0]+BLOCK_SIZE,self.player_cords[1]))
                if self.render:
                    self.redraw()
                
                

        


    


def main():
    run= True 
    game=gridgame(5,render=True)
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run= False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.take_action("l")
                
                if event.key == pygame.K_RIGHT:
                    game.take_action("r")

                if event.key == pygame.K_UP:
                    game.take_action("u")

                if event.key == pygame.K_DOWN:
                    game.take_action("d")


if __name__ == "__main__":
    main()



