
# config_life.py : configuration file for life game

NG = 0											# number of generations

TICKS = 10										# clock ticks	

MAXTIME = 100									# tempo massimo di esecuzione in sec

XRES,YRES,RES = 640,480,4						# screen resolution and dot dimension

DIM = (XRES//RES,YRES//RES)						# dimensione delle matrici di calcolo

RED,GREEN,BLUE = 3,2,4							# rgb components

C_DEAD,C_ALIVE = (0,0,0),(255,255,255)			# con quali colori vengono rappresentate a video le cellule vive o morte

DEAD,ALIVE = 0,1								# valori assunti dalla cellula morta e da quella viva

S0,S1,S2,S3,S4,S5,S6,S7,S8 = 0,1,2,3,4,5,6,7,8	# valori possibili per la somma dei vicini	

PERC = 0.6										# percentuale di cellule inizialmente vive