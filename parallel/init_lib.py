# init_lib.py e' un modulo per consentire la visibilità delle routines scritte da me che stanno nella dir python/ in dropbox.

def add_path_to_lib(libraries):
	import os,sys
	directories = ( 'C:/Users/Massimiliano/Dropbox/miei-programmi/python/',			\
					'C:/Users/massimiliano.cosmell/Dropbox/miei-programmi/python/',	\
					'C:/Users/admin/Dropbox/miei-programmi/python/' )
	for directory in directories:
		if os.path.exists(directory):
			if len(libraries) == 1:
				print(f'\nLinking {len(libraries)} external library:')
				sys.path.append(directory + libraries[0])
				print(f'{directory+libraries[0]}')
			else:
				print(f'\nLinking {len(libraries)} external libraries:')
				for library in libraries:
					sys.path.append(directory + library)
					print(f'{directory+library}')