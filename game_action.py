from enum import Enum

class GameAction(Enum):
	HOLD=0
	ROLL=1
	SCORE=2
	RESTART=3
	
	def __str__(self):
		return self.name.lower()
		


if __name__ == '__main__':
	for a in GameAction:
		print(a)
