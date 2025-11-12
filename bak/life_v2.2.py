
# life_v2.2.py : life game with pygame and arrays

# John Conway - Game of Life

# CopyRight 2020 by Lumachina Software - @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

# Le transizioni di stato dipendono unicamente dallo stato delle celle vicine in quella generazione:
#
# - Qualsiasi cella viva con meno di due celle vive adiacenti muore, come per effetto d'isolamento;
# - Qualsiasi cella viva con due o tre celle vive adiacenti sopravvive alla generazione successiva;
# - Qualsiasi cella viva con più di tre celle vive adiacenti muore, come per effetto di sovrappopolazione;
# - Qualsiasi cella morta con esattamente tre celle vive adiacenti diventa una cella viva, come per effetto di riproduzione.

# versione base, con possibilità di passare i parametri di densità di cellule vive iniziali e il ritardo di refresh

# in questa versione implemento le matrici utilizzando le liste.

import time
from random import random,randint,seed
import pygame, sys, traceback
from pygame.locals import *
import itertools

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

def get(a,x,y): return a[x+DIM[0]*y]
def set(a,x,y):
	a[x+DIM[0]*y] = ALIVE
	return a
def unset(a,x,y):
	a[x+DIM[0]*y] = DEAD
	return a
def getcolor(a,c,x,y): return a[x+DIM[0]*y]*c[x+DIM[0]*y]
def inccolor(a,x,y):a[x+DIM[0]*y] += 1

def drawCells(c,co):
	for x,y in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
		cc = getcolor(c,co,x,y)
		s.fill((RED*cc%256,GREEN*cc%256,BLUE*cc%256))
		r.x,r.y = x*RES,y*RES	# get an object rectangle from the object surface and place it at position x,y
		screen.blit(s,r)		# link the object rectangle to the object surface
	pygame.display.flip()		# update the entire pygame display
	
def rndCells(a,c,s):
	# creates an rnd grid
	for i,j in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
		if random() < s:
			set(a,i,j)
			inccolor(c,i,j)
		else: unset(a,i,j)
	return a,c

def setCell(c,x,y):return set(c,x//RES,y//RES)
def killCell(c,x,y):return unset(c,x//RES,y//RES)

def updateCells(c,cc,co):
	# updates the cells status considering the Moore's neighborhoods
	for i,j in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
		# sum of the neighborhoods's status
		S = get(c,i-1,j+1) + get(c,i,j+1) + get(c,i+1,j+1) + \
			get(c,i-1,j)   + get(c,i+1,j) + \
			get(c,i-1,j-1) + get(c,i,j-1) + get(c,i+1,j-1)
		# update cell applying rules		
		if get(c,i,j) == ALIVE:
			if S < S2:unset(cc,i,j)	# muore di solitudine
			elif S == S2 or S == S3:
				set(cc,i,j)			# rimane invariato
				inccolor(co,i,j)
			else: unset(cc,i,j)		# muore per sovrappopolazione (caso S > S3)
		elif S == S3:
			set(cc,i,j)				# resuscita miracolosamente
			inccolor(co,i,j)
		else: unset(cc,i,j)			# sterile (caso S != S3)
	return (cc,co)

def main():

	randomize()

	D = (DIM[0]+1)*(DIM[1]+1)	# dimensione della 'matrice' ..ex newMatrix(DIM[0]+1,DIM[1]+1)
	CELLS,COLORS = rndCells([0]*D,[0]*D,PERC) #rndCells(array.array('B',[0]*D),array.array('B',[0]*D),PERC)
	EMPTY = [0]*D #array.array('B',[0]*D)
	
	T = time.time()
	NG = 0
		
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
					CELLS = killCell(CELLS,event.pos[0],event.pos[1])	# ammazza una cellula
				
		drawCells(CELLS,COLORS)
		CELLS,COLORS = updateCells(CELLS,CELLS.copy(),COLORS) #updateCells(CELLS,CELLS[:],COLORS)
		
		NG += 1
		pygame.display.set_caption(f'Life v.2.2 (c)2020 by Lumachina Software - @_°°           GEN:{NG}')
		
	terminate(T,NG)
			
main()
