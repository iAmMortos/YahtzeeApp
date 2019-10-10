import os


filename = '.highscore'

def clear():
	with open(filename, 'w') as f:
		f.write('\n0')
		
def get():
	if not os.path.exists(filename):
		clear()
		return {'name':None, 'score':0}
	else:
		name = None
		score = None
		with open(filename) as f:
			parts = f.read().split('\n')
			name = parts[0] if parts[0] != '' else None
			score = int(parts[1])
		return {'name':name, 'score':score}
	
def set(name, score):
	with open(filename, 'w') as f:
		f.write('%s\n%s' % (name, score))
