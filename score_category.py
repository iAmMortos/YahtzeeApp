from enum import Enum

class ScoreCategory (Enum):
	ONES = 1
	TWOS = 2
	THREES = 3
	FOURS = 4
	FIVES = 5
	SIXES = 6
	THREE_OF_A_KIND = 7
	FOUR_OF_A_KIND = 8
	FULL_HOUSE = 25
	SM_STRAIGHT = 30
	LG_STRAIGHT = 40
	CHANCE = 9
	YAHTZEE = 50
	
	def __str__(self):
		if self is ScoreCategory.SM_STRAIGHT:
			return 'small straight'
		elif self is ScoreCategory.LG_STRAIGHT:
			return 'large straight'
		else:
			return ' '.join(self.name.lower().split('_'))
	
	@staticmethod
	def top_categories():
		return [ScoreCategory.ONES, ScoreCategory.TWOS, ScoreCategory.THREES, ScoreCategory.FOURS, ScoreCategory.FIVES, ScoreCategory.SIXES]
		
	@staticmethod
	def bottom_categories():
		return [ScoreCategory.THREE_OF_A_KIND, ScoreCategory.FOUR_OF_A_KIND, ScoreCategory.FULL_HOUSE, ScoreCategory.SM_STRAIGHT, ScoreCategory.LG_STRAIGHT, ScoreCategory.CHANCE, ScoreCategory.YAHTZEE]
			
			
			
if __name__ == '__main__':
	for c in ScoreCategory:
		print(c)
