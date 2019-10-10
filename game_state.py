
from enum import Enum

class GameState(Enum):
	NEED_ROLL = 0
	ROLLING = 1
	NO_MORE_ROLLS = 2
	GAME_OVER = 3
	
	def __str__(self):
		return ' '.join(self.name.lower().split('_'))
		
	
	
if __name__ == '__main__':
	for s in GameState:
		print(s)
