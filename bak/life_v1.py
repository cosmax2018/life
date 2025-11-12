
# life_v1.0.py : life game with pygame

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
add_path_to_lib(('graphics',))

import time
import random
from copy import deepcopy
from graphics import *
from matrici import *

from config_life import *

# con quale colore viene rappresentata a video una cella viva o morta
DEAD,ALIVE	= 0,1

# valori possibili per la somma di tutti i vicini
S0,S1,S2,S3,S4,S5,S6,S7,S8 = 0,1,2,3,4,5,6,7,8
	
def rndCells(a,s):
	# creates an rnd grid
	for i in range(1,DIM[0]-1):
		for j in range(1,DIM[1]-1):
			if random.random() < s:	a[i][j] = ALIVE
			else:					a[i][j] = DEAD
	return a

def initGraphicsObjs(resX,resY,d):
	# inizializza la griglia di n x m rettangoli (crea gli oggetti grafici necessari)
	sx = resX//d[0]
	sy = resY//d[1]
	g = []
	for x in range(0,resX-1,sx):
		row = []
		for y in range(0,resY-1,sy):
			row.append(Rectangle(Point(x,y),Point(x+sx,y+sy)))
		g.append(row)
	return g
	
def drawGraphicObjs(g,f):
	# accende gli oggetti grafici a video
	for i in range(DIM[0]):
		for j in range(DIM[1]):
			g[i][j].draw(f)
	return g
	
def sumStatusOfNeighborhoods(a, i, j):
	# sum of the neighborhoods's integer
	return 	a[i-1][j+1] + a[i][j+1] + a[i+1][j+1] + \
			a[i-1][j]	     +		  a[i+1][j]   + \
			a[i-1][j-1] + a[i][j-1] + a[i+1][j-1]
	
def updateCells(a):
	# updates the cells status considering the Moore's neighborhoods
	b = deepcopy(a)
	for i in range(1,DIM[0]):
		for j in range(1,DIM[1]):
			S = sumStatusOfNeighborhoods(b,i,j)	# the neighborhoods status sum
			# update cell applying rules
			if b[i][j] == ALIVE:
				if S < S2:					a[i][j] = DEAD	# muore di solitudine
				elif S == S2 or S == S3:	a[i][j] = ALIVE	# rimane invariato
				else:						a[i][j] = DEAD	# muore per sovrappopolazione (caso S > S3)
			elif S == S3:					a[i][j] = ALIVE	# resuscita miracolosamente
			else:							a[i][j] = DEAD	# sterile (caso S != S3)
			
def updateGraphicObjs(g,c):
	# aggiorna gli oggetti grafici g in base ai valori delle celle c
	for i in range(DIM[0]):
		for j in range(DIM[1]):
			if c[i][j] == ALIVE:	g[i][j].setFill('white')
			else:					g[i][j].setFill('black')

def main():

	random.seed(time.time()) # randomize timer
	
	CELLS = rndCells(newMatrix(DIM[0]+1,DIM[1]+1),PERC)
	
	NG = 0
	
	window = GraphWin('life v1.0 (c)2019 by Lumachina Software - @_°°',640,480+20)
	window.setBackground('black')
	window.autoflush = False		# to speed up simulation
	
	GRID = drawGraphicObjs(initGraphicsObjs(640,480,DIM),window)
	
	mess = Text(Point(320,490),f'Life v.1 (c)2019 by Lumachina Software - @_°° GEN:{NG}')
	mess.setSize(18)
	mess.setTextColor('red')
	mess.draw(window)
	
	t = time.time()
		
	while time.time() - t < MAXTIME:
		if window.checkKey() == 'Escape':
			window.close()
		
		updateGraphicObjs(GRID,CELLS)

		updateCells(CELLS)

		NG += 1		
		mess.setText(f'Life v.1 (c)2019 by Lumachina Software - @_°° GEN:{NG}')
	
	print(f'Generazioni al sec {NG/MAXTIME}/sec')			# stampa a console il numero di generazioni
	sys.exit()

main()
