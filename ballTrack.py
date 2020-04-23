import pygame, time
from pygame.locals import *
import random

pygame.font.init() # you have to call this at the start, 
                # if you want to use this module.

textSize = 130
comicSans = pygame.font.SysFont('Comic Sans MS', textSize )   
clock = pygame.time.Clock()
def main():


    surface = create_window()
    game = Game(surface) #call a function that has the same name as the class
    game.play() #call play method on game
    pygame.quit()

 
def create_window():
    # Open a window on the display and rseturn its Surface
    title = 'Ball Track'
    size =(1920, 1080)
    pygame.init()
    surface = pygame.display.set_mode(size, 0, 0)
    pygame.display.set_caption(title)
    return surface




class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image,(1920, 1080))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Game:

    def __init__(self, surface):

        
        self.BackGround = Background('bball.jpg', [0,0])
        self.bg_color = pygame.Color('black')
        self.fg_color = pygame.Color('white')
        self.pause_time = 0.00 # smaller is faster game
        self.surface = surface
        self.close_clicked = False
        self.continue_game = True
        ball_location = [self.surface.get_width()//2, self.surface.get_height()//2]
        ball_size = 150
        ball_velocity = [10,10]
        self.updateBallFreq = 3
        self.ball = Ball(self.surface, ball_location, ball_size , self.fg_color, ball_velocity )

        
        self.startTime = time.perf_counter()

    def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.
 
        self.draw()
        self.surface.blit(self.BackGround.image, self.BackGround.rect)
        while not self.close_clicked: # until player clicks close box
            self.update()
            self.handle_event()
            self.draw()
            clock.tick(60)
            #time.sleep(self.pause_time) # set game velocity by pausing

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        #self.surface.fill(self.bg_color)
        #self.surface.fill([255, 255, 255])
       # 
        self.surface.blit(self.BackGround.image, [self.ball.center[0]-50, self.ball.center[1]-50], pygame.Rect(self.ball.center[0]-50, self.ball.center[1]-50, 300, 300))
        self.ball.draw()
        pygame.display.update() #do not erase

    def update(self):
        if time.perf_counter() -  self.startTime > self.updateBallFreq:
            self.ball.changeNumber()
            self.startTime = time.perf_counter()

        self.ball.move()


    def handle_event(self):
        # Handle each user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled
        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True


class Ball:
   # An object in this class represents a colored circle.
   def __init__(self, surface, location, size, color, velocity):
      self.surface = surface
      self.center = location
      self.radius = size
      self.color = color
      self.velocity = velocity
      self.image = pygame.image.load("ball.png")

      self.image_size = (150, 150)
      self.image = pygame.transform.scale(self.image, self.image_size)
      self.number = random.randint(0,10)


   def changeNumber(self):
       self.number = random.randint(0,9)
   
   def draw(self):
      #draws ball
    
      #pygame.draw.circle(self.surface,self.color,self.center,self.radius)
      #self.surface.blit(self.image, (self.center[0] - self.image_size[0]//2, self.center[1] -  self.image_size[1]//2))
      self.surface.blit(self.image, (self.center[0], self.center[1]))
      textsurface = comicSans.render(str(self.number), False, (255, 255, 255))
      self.surface.blit(textsurface, (self.center[0] + 50, self.center[1] + 30) )
   
   def move(self):
      #moves ball
      size = self.surface.get_size()
      for coord in range(0,2):#number 0 and 1
         self.center[coord] = (self.center[coord] + self.velocity[coord])
         if self.center[coord] < self.radius:
            self.velocity[coord] = -self.velocity[coord]
         if self.center[coord] + self.radius > size[coord]:
            self.velocity[coord] = -self.velocity[coord]            
    



main()