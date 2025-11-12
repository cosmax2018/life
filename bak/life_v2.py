
# life_v2.0.py : life game with pygame

# John Conway - Game of Life

# CopyRight 2019 by Lumachina Software - @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

# Le transizioni di stato dipendono unicamente dallo stato delle celle vicine in quella generazione:
#
# - Qualsiasi cella viva con meno di due celle vive adiacenti muore, come per effetto d'isolamento;
# - Qualsiasi cella viva con due o tre celle vive adiacenti sopravvive alla generazione successiva;
# - Qualsiasi cella viva con più di tre celle vive adiacenti muore, come per effetto di sovrappopolazione;
# - Qualsiasi cella morta con esattamente tre celle vive adiacenti diventa una cella viva, come per effetto di riproduzione.

# versione base, con possibilità di passare i parametri di densità di cellule vive iniziali e il ritardo di refresh

from init_lib import *
add_path_to_lib(('matrici',))

import time
from random import random,randint,seed
import pygame, sys, traceback
from pygame.locals import *

from copy import deepcopy
from matrici import *

from config_life import *

pygame.init()
screen = pygame.display.set_mode((XRES,YRES))

def randomize():	seed(time.time())

def terminate(t,ng):
	dt = time.time()-t
	print(f'Velocità :  {ng/dt} generazioni al secondo')			# stampa a console il numero di generazioni
	print(f'Terminato dopo {int(dt)} secondi')
	pygame.quit()
	sys.exit()	
	
def drawCells():
	for x in range(1,DIM[0]):
		for y in range(1,DIM[1]):
			s = pygame.Surface((RES,RES))	# the object surface of a dimension of RES x RES
			c = CELLS[x][y]
			s.fill((255*c,255*c,255*c))
			r,r.x,r.y = s.get_rect(),x*RES,y*RES	# get an object rectangle from the object surface and place it at position x,y
			screen.blit(s,r)						# link the object rectangle to the object surface
	
	pygame.display.update()
	
def rndCells(a,s):
	# creates an rnd grid
	for i in range(1,DIM[0]):
		for j in range(1,DIM[1]):
			if random() < s:
				a[i][j] = ALIVE
			else:
				a[i][j] = DEAD
	return a

def setCell(x,y):	CELLS[x//RES][y//RES] = ALIVE
	
def clearCell(x,y):	CELLS[x//RES][y//RES] = DEAD

def updateCells():
	# updates the cells status considering the Moore's neighborhoods
	b = deepcopy(CELLS)
	for i in range(1,DIM[0]):
		for j in range(1,DIM[1]):
			# sum of the neighborhoods's status
			S = b[i-1][j+1] + b[i][j+1] + b[i+1][j+1] + \
				b[i-1][j]	     +		  b[i+1][j]   + \
				b[i-1][j-1] + b[i][j-1] + b[i+1][j-1]
			# update cell applying rules
			if b[i][j] == ALIVE:
				if S < S2:					CELLS[i][j] = DEAD	# muore di solitudine
				elif S == S2 or S == S3:	CELLS[i][j] = ALIVE	# rimane invariato
				else:						CELLS[i][j] = DEAD	# muore per sovrappopolazione (caso S > S3)
			elif S == S3:					CELLS[i][j] = ALIVE	# resuscita miracolosamente
			else:							CELLS[i][j] = DEAD	# sterile (caso S != S3)

def main():

	randomize()
	clock = pygame.time.Clock()
	
	global CELLS
	CELLS = rndCells(newMatrix(DIM[0]+1,DIM[1]+1),PERC)
		
	NG = 0
	T = time.time()
		
	while True:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate(T,NG)
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE: 
					terminate(T,NG)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					setCell(event.pos[0],event.pos[1])		# aggiunge una cellula viva
				elif event.button == 3:
					clearCell(event.pos[0],event.pos[1])	# ammazza una cellula
		drawCells()
		
		updateCells()
		
		NG += 1
		pygame.display.set_caption(f'Life v.2 (c)2019 by Lumachina Software - @_°°           GEN:{NG}')
		
		clock.tick(60)
		
	terminate(T,NG)
			
main()

