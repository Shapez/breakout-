import pygame
import random
import math
from pygame.locals import * 

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

h = 700
w = 800

screen = pygame.display.set_mode([w,h])
barsize = [20,50]
lmargin = [barsize[0],h]
puk = [screen, red,(w/2 - 43,h - 13,80,10)]

circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(255,255,255),(15/2,15/2),15/2)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))

circle_x = 300.5
circle_y = 300.5
pps = (10,20)
pygame.display.set_caption('breakout')
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()

class Block():
	def __init__(self, x, y):
		self.color =  (random.choice(range(255)),
						random.choice(range(255)),
						random.choice(range(255))
						)
		self.shape = pygame.Rect(x,y,78,38)
		self.dead = False

	@property
	def colliderect(self):
		return self.shape.inflate(20,20)

	def update(self):
		self.shape.move(random.choice([-0.01,0,0.01]),random.choice([-0.01,0,0.01]))

	def hitby(self, obj):
		self.dead = True
		if hasattr(obj, 'hitother'):
			obj.hitother(self)

	def draw(self):
		pygame.draw.rect(screen, self.color, self.shape)
		pygame.draw.rect(screen, self.color, self.colliderect, 1)

class Ball():
	def __init__(self, color=(255,255,255), origin=(300, 300), vel=(1,-1), speed=0.2, shape=circle):
		self.color = color
		self.origin = (float(origin[0]), float(origin[1]))
		self.vel = (float(vel[0]), float(vel[1]))
		self.speed = float(speed)
		self.shape = shape
		self.size = 8
		self.constrainw = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		
	@property
	def atboundx(self):
		if self.origin[0] < 2 or self.origin[0] >= self.constrainw[0] - 10:
			return True

		return False

	@property
	def atboundy(self):
		if self.origin[1] < 2 or self.origin[1] > self.constrainw[1] - 10:
			return True
		return False

	@property
	def next_position(self):
		curpos = self.origin
		speedmod = clock.get_time() * self.speed
		if self.atboundx:
			self.vel = (self.vel[0] * -1, self.vel[1])
		if self.atboundy:
			self.vel = (self.vel[0], self.vel[1] * -1)

		nextx = (self.origin[0] + self.vel[0] * speedmod)
		nexty = (self.origin[1] + self.vel[1] * speedmod)
		return (nextx, nexty)

	def bouncey(self):
		self.vel = (self.vel[0], self.vel[1] * -1)

	def bouncex(self):
		self.vel = (self.vel[0] * -1, self.vel[1])

	def update(self):
		self.origin = self.next_position

	def hitother(self, other):
		if angle(self.origin, other.shape.center) > 0.08:
			self.bouncey()
		else:
			self.bouncex()

	def draw(self):
		pygame.draw.circle(screen, self.color, (int(self.origin[0]), int(self.origin[1])), self.size, 1)

	def broke(self):
		pass
#class Bouncer():
#	def __init__(self, x, y):
#		self.origin = (puk[2][0], puk[2][1])

#
#	def update(self):
#		self.origin = ()


pattern = [Block(x, random.randint(20,80)) for x in range(0,w,80)]
balls = [Ball(origin=(300,300))]
while True:
	clock.tick(360)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()


	screen.fill((black))
	pygame.draw.rect(puk[0],red,puk[2],5)

	pattern = [block for block in pattern if not block.dead]

	for block in pattern:
		block.update()
		block.draw()
		for ball in balls:
			if block.colliderect.collidepoint(ball.origin):
				block.hitby(ball)

	for ball in balls:

		ball.update()
		ball.draw()



	#screen.blit(circle,(circle_x,circle_y))
	#ball.update()
	#print(circle_x, circle_y, seconds)
	pygame.display.update()
	
		
