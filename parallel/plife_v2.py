
# plife_v2.py : parallel life game with pygame

# John Conway - Game of Life

# CopyRight 2020 by Lumachina Software - @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

# Le transizioni di stato dipendono unicamente dallo stato delle celle vicine in quella generazione:
#
# - Qualsiasi cella viva con meno di due celle vive adiacenti muore, come per effetto d'isolamento;
# - Qualsiasi cella viva con due o tre celle vive adiacenti sopravvive alla generazione successiva;
# - Qualsiasi cella viva con più di tre celle vive adiacenti muore, come per effetto di sovrappopolazione;
# - Qualsiasi cella morta con esattamente tre celle vive adiacenti diventa una cella viva, come per effetto di riproduzione.

# versione base, con possibilità di passare i parametri di densità di cellule vive iniziali e il ritardo di refresh

from mpi4py import MPI

from init_lib import *
add_path_to_lib('matrix')
from matrici import newMatrix,deepCopyMatrix

from random import random,randint,seed
import pygame, sys, time, traceback, itertools
from pygame.locals import *

from config_life import *

# the parallel world
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

ROWS = (DIM[0]+1)//size 	# how many rows per node

if rank == 0:
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
	
def drawCells(c,co):
	if rank == 0:
		try:
			for x,y in itertools.product(range(DIM[0]),range(DIM[1])):
				cc = co[x][y]*c[x][y]
				s.fill((RED*cc%256,GREEN*cc%256,BLUE*cc%256))
				r.x,r.y = x*RES,y*RES	# get an object rectangle from the object surface and place it at position x,y
				screen.blit(s,r)		# link the object rectangle to the object surface
			pygame.display.flip()		# update the entire pygame display
		except IndexError:
			print(f'drawCells::IndexError: x:{x},y:{y}')
			print(f'drawCells:: len(c):{len(c)},len(co):{len(co)}')
			print(f'drawCells:: len(c[0]):{len(c[0])},len(co[0]):{len(co[0])}')
			print(f'drawCells:: len(c[0][0]):{len(c[0][0])},len(co[0][0]):{len(co[0][0])}')
			quit()

def rndCells(a,c,s):
	# creates an rnd grid
	if rank == 0:
		for i,j in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
			if random() < s:
				a[i][j] = ALIVE
				c[i][j] += 1
			else: 
				a[i][j] = DEAD
		return a,c

def setCell(c,x,y):
	if rank == 0:
		c[x//RES][y//RES] = ALIVE
		return c
	
def clearCell(c,x,y):
	if rank == 0:
		c[x//RES][y//RES] = DEAD
		return c

#def updateCells(c,cc,co):
	# updates the cells status considering the Moore's neighborhoods
#	try:
#		for i,j in itertools.product(range(1,len(c)-1),range(1,len(c[0])-1)):
			# sum of the neighborhoods's status
#			S = c[i-1][j+1] + c[i][j+1] + c[i+1][j+1] + \
#				c[i-1][j]	     +		  c[i+1][j]   + \
#				c[i-1][j-1] + c[i][j-1] + c[i+1][j-1]
			# update cell applying rules		
#			if c[i][j] == ALIVE:
#				if S < S2:	cc[i][j] = DEAD	# muore di solitudine
#				elif S == S2 or S == S3:
#					cc[i][j] = ALIVE		# rimane invariato
#					co[i][j] += 1
#				else:
#					 cc[i][j] = DEAD		# muore per sovrappopolazione (caso S > S3)
#			elif S == S3:
#				cc[i][j] = ALIVE			# resuscita miracolosamente
#				co[i][j] += 1
#			else: 
#				cc[i][j] = DEAD				# sterile (caso S != S3)
#	except IndexError:
#		print(f'updateCells::IndexError: x:{x},y:{y}')
#		print(f'drawCells:: len(c):{len(c)},len(cc):{len(cc)},len(co):{len(co)}')
#		print(f'drawCells:: len(c[0]):{len(c[0])},len(cc[0]):{len(cc[0])},len(co[0]):{len(co[0])}')
#		quit()

#	return (cc,co)

def main():

	randomize()
	
	if rank == 0:	# on master node creates data

		MCELLS,MCOLORS = rndCells(newMatrix(DIM[0]+1,DIM[1]+1),newMatrix(DIM[0]+1,DIM[1]+1),PERC)

		#print(f'create data: {MCELLS}')
		print(f'DIMX:{len(MCELLS)} DIMY:{len(MCELLS[0])}')

		CELLS,COLORS = [],[]

		for i in range(size):
			CELLS.append(MCELLS[i*ROWS:(i+1)*ROWS])
			COLORS.append(MCOLORS[i*ROWS:(i+1)*ROWS])
	else:
		CELLS,COLORS = None,None

	NG,T = 0,time.time()	# initializing iterations number and execution time
	
	while True:

		NG += 1

		# on every node scatter data
		CELLS, COLORS = comm.scatter(CELLS, root=0), comm.scatter(COLORS, root=0)

		# on every node now performing some sort of operations on data
		#CELLS,COLORS = updateCells(CELLS,deepCopyMatrix(CELLS),COLORS)

		# *********** UPDATE CELLS  *************

		CCELLS = deepCopyMatrix(CELLS)

		# updates the cells status considering the Moore's neighborhoods
		try:
			for i,j in itertools.product(range(1,len(CELLS)-1),range(1,len(CELLS[0])-1)):
				# sum of the neighborhoods's status
				S = CELLS[i-1][j+1] + CELLS[i][j+1] + 	CELLS[i+1][j+1] + \
					CELLS[i-1][j]	     +		  		CELLS[i+1][j]   + \
					CELLS[i-1][j-1] + CELLS[i][j-1] + 	CELLS[i+1][j-1]
				# update cell applying rules		
				if CELLS[i][j] == ALIVE:
					if S < S2:	CCELLS[i][j] = DEAD	# muore di solitudine
					elif S == S2 or S == S3:
						CCELLS[i][j] = ALIVE		# rimane invariato
						COLORS[i][j] += 1
					else:
						 CCELLS[i][j] = DEAD		# muore per sovrappopolazione (caso S > S3)
				elif S == S3:
					CCELLS[i][j] = ALIVE			# resuscita miracolosamente
					COLORS[i][j] += 1
				else: 
					CCELLS[i][j] = DEAD				# sterile (caso S != S3)

			#CELLS = deepCopyMatrix(CCELLS)

		except IndexError:
			print(f'updateCells::IndexError: x:{x},y:{y}')
			print(f'drawCells:: len(c):{len(c)},len(cc):{len(cc)},len(co):{len(co)}')
			print(f'drawCells:: len(c[0]):{len(c[0])},len(cc[0]):{len(cc[0])},len(co[0]):{len(co[0])}')
			quit()

		# *************************************

		# from every node gather data
		CELLS, COLORS = comm.gather(CCELLS, root=0), comm.gather(COLORS, root=0)		

		if rank == 0:

			#print(f'gather data : {CELLS}')

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

			# rimette insieme la matrice:

			#print('\n\n Reconstruct Matrix:')
			#print(MCELLS)
			#print(f'DIMX:{len(MCELLS)} DIMY:{len(MCELLS[0])}')

			n = 0
			for ss in range(size):
				for rr in range(ROWS):
					MCELLS[n],MCOLORS[n] = CELLS[ss][rr],COLORS[ss][rr]
					n += 1

			drawCells(MCELLS,MCOLORS)	
			pygame.display.set_caption(f'Parallel Life v.1 (c)2020 by Lumachina Software - @_°°    GEN:{NG}')		

	terminate(T,NG)
			
main()
