
# life_v5.0.py : life game with PyGame, Numpy and Numba !!

# John Conway - Game of Life

# Mit License 2019-2022 by Lumachina Software - @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

# Le transizioni di stato dipendono unicamente dallo stato delle celle vicine in quella generazione:
#
# - Qualsiasi cella viva con meno di due celle vive adiacenti muore, come per effetto d'isolamento;
# - Qualsiasi cella viva con due o tre celle vive adiacenti sopravvive alla generazione successiva;
# - Qualsiasi cella viva con più di tre celle vive adiacenti muore, come per effetto di sovrappopolazione;
# - Qualsiasi cella morta con esattamente tre celle vive adiacenti diventa una cella viva, come per effetto di riproduzione.

import time
import numpy as np
from random import random,randint,seed
import pygame, sys, traceback
from pygame.locals import *

from numba import jit

from config_life import *

pygame.init()
screen = pygame.display.set_mode((XRES,YRES))
s = pygame.Surface((RES,RES))	# the object surface of a dimension of RES x RES
r = s.get_rect()				# the 'pixel' at x,y

def randomize():	seed(time.time())

def terminate(t,ng):
	dt = time.time()-t
	print(f'Velocità :  {ng/dt} generazioni al secondo')			# stampa a console il numero di generazioni
	print(f'Terminato dopo {int(dt)} secondi')
	pygame.quit()
	sys.exit()
	
def drawCells(c,co,rr,gg,bb):
	for x in range(1,DIM[0]-1):
		for y in range(1,DIM[1]-1):		
			cc = co[x][y]*c[x][y]
			s.fill((rr*cc%256,gg*cc%256,bb*cc%256))
			r.x,r.y = x*RES,y*RES	# get an object rectangle from the object surface and place it at position x,y
			screen.blit(s,r)		# link the object rectangle to the object surface
	pygame.display.flip()		# update the entire pygame display

def resetCells(a,v=None):
	# reset the grid to ZERO or at value v
	if v == None:
		for i in range(1,DIM[0]-1):
			for j in range(1,DIM[1]-1):		
				a[i][j] = 0
	else:
		for i in range(1,DIM[0]-1):
			for j in range(1,DIM[1]-1):		
				a[i][j] = v
	return a
	
@jit(nopython=True,nogil=True)
def rndCells(s):
	# creates an rnd grid
	a = np.arange((DIM[0]+1)*(DIM[1]+1))
	a = a.reshape((DIM[0]+1,DIM[1]+1))
	a = np.zeros_like(a)
	c = np.arange((DIM[0]+1)*(DIM[1]+1))
	c = c.reshape((DIM[0]+1,DIM[1]+1))
	c = np.zeros_like(c)
	for i in range(1,DIM[0]-1):
		for j in range(1,DIM[1]-1):
			if random() < s:
				a[i][j] = ALIVE
				c[i][j] += 1
			else: a[i][j] = DEAD
	return a,c
		
def setCell(c,x,y):
	c[x//RES][y//RES] = ALIVE
	return c
	
def clearCell(c,x,y):
	c[x//RES][y//RES] = DEAD
	return c

@jit(nopython=True,nogil=True)
def updateCells(c,cc,co):
	# updates the cells status considering the Moore's neighborhoods
	for i in range(1,DIM[0]-1):
		for j in range(1,DIM[1]-1):		
			# sum of the neighborhoods's status
			S = c[i-1][j+1] + c[i][j+1] + c[i+1][j+1] + \
				c[i-1][j]	     +		  c[i+1][j]   + \
				c[i-1][j-1] + c[i][j-1] + c[i+1][j-1]
			# update cell applying rules		
			if c[i][j] == ALIVE:
				if S < S2:	cc[i][j] = DEAD	# muore di solitudine
				elif S == S2 or S == S3:
					cc[i][j] = ALIVE		# rimane invariato
					co[i][j] += 1
				else: cc[i][j] = DEAD		# muore per sovrappopolazione (caso S > S3)
			elif S == S3:
				cc[i][j] = ALIVE			# resuscita miracolosamente
				co[i][j] += 1
			else: cc[i][j] = DEAD			# sterile (caso S != S3)
	return (cc,co)

def main(a):

	# eg.:    py life_v5.0.py .6 3 5 2
	try:
		PERC,RED,GREEN,BLUE = float(a[0]),int(a[1]),int(a[2]),int(a[3])
	except:
		RED,GREEN,BLUE = 3,2,4						# rgb components
		PERC = 0.6									# percentuale di cellule inizialmente contagiate
	finally:
		print(f'Life Game Parameters %:{PERC} RED,GREEN,BLUE:{RED},{GREEN},{BLUE}')
	
	randomize()
	
	CELLS,COLORS = rndCells(PERC)
	
	NG,T = 0,time.time()
		
	while True:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate(T,NG)
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE: 
					terminate(T,NG)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					CELLS = setCell(CELLS,event.pos[0],event.pos[1])	# aggiunge una cellula viva
				elif event.button == 3:
					CELLS = clearCell(CELLS,event.pos[0],event.pos[1])	# ammazza una cellula
				
		drawCells(CELLS,COLORS,RED,GREEN,BLUE)
		CELLS,COLORS = updateCells(CELLS,np.copy(CELLS),COLORS)
		
		NG += 1
		pygame.display.set_caption(f'Life v.5 (c)2022 by Lumachina Software - @_°°           GEN:{NG}')
		
	terminate(T,NG)
			
main(sys.argv[1:])
