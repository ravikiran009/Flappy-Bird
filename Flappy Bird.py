import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 40

screen_width = 500
screen_height = 400

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy Bird')

#Font
font = pygame.font.SysFont('Bauhaus 93', 40)

#Colour
white = (255,255,255)

#Defining Variables
flying = False
ground_scroll = 0
scroll_speed = 4
pipe_frequency = 1000 #milliseconds
last_pipe = pygame.time.get_ticks() 
score = 0
pass_pipe = False
game_over = False

#Images
bg = pygame.image.load('bg.png')
ground = pygame.image.load('ground.png')
restart = pygame.image.load('restart.png')

def draw_text(text,font,text_col,x,y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x,y))

def reset_game():
	pipe_group.empty()
	flappy.rect.x = 60
	flappy.rect.y = 200

class Bird(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		for num in range(1,4):
			img = pygame.image.load(f'bird{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.vel = 0		
		self.clicked = False

	def update(self):

		if self.rect.bottom < 300 and self.rect.top > 0:
			#For Jumping and Gravity
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and flying == True: 
				self.clicked = True
				self.vel = -5
			elif flying == True: 
				self.clicked = False
				self.vel += 0.5
			if self.rect.bottom < 300 and self.rect.top > 0:
				self.rect.y += int(self.vel)

			#Bird Animation
			self.counter += 1
			flap_cooldown = 15

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index =0
			self.image = self.images[self.index]
			self.image = pygame.transform.rotate(self.images[self.index], self.vel*-0.5)
		else :
			self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
	def __init__(self,x,y,position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('pipe.png')
		self.rect = self.image.get_rect()
		#position 1 is form top and position -1 is from bottom
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x,y-50]
		if position == -1:
			self.rect.topleft = [x,y+50]

	def update(self):

		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

class Restart():
	def __init__(self,x,y,image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
	def draw(self):
		action = False
		#Getting Mouse Position
		pos = pygame.mouse.get_pos()
		#Cursor is on Button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		screen.blit(self.image , (self.rect.x,self.rect.y))

		return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(60,200)

bird_group.add(flappy)

#Restart
button = Restart(250,200,restart)

run = True
while run:

	clock.tick(fps)

	#Background
	screen.blit(bg, (0,0))
	screen.blit(bg, (168,0))
	screen.blit(bg, (336,0))


	bird_group.draw(screen)
	bird_group.update()
	pipe_group.draw(screen)

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False

	draw_text(str(score), font, white, 250, 20)	

	#Checking for collision
	if pygame.sprite.groupcollide(bird_group,pipe_group,False,False):
		game_over = True

	if game_over == False:

		#For generating pipes
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency: 
			pipe_height = random.randint(-60,60)
			top_pipe = Pipe(500,200+pipe_height,1)
			btm_pipe = Pipe(500,200+pipe_height,-1)
			pipe_group.add(top_pipe)
			pipe_group.add(btm_pipe)
			last_pipe = time_now 

	    #Scrolling Ground
		screen.blit(ground, (ground_scroll,300))

		if flappy.rect.bottom < 300 and flappy.rect.top >0:
			if abs(ground_scroll) > 13:
				ground_scroll = 0
			ground_scroll -= scroll_speed
		else :
			game_over = True

		pipe_group.update()

	else:
		#For Restarting Game
		if button.draw() == True:
			game_over = False
			score = 0
			reset_game()
		
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == pygame.mouse.get_pressed()[0] == 1:
				flying = True
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False

	pygame.display.update()

pygame.quit()

# dude branch