
import sharedlibs
sharedlibs.add_path_for('dice')
from dice import Dice

from scorecard import Scorecard
from game_state import GameState as GS
from game_action import GameAction as GA
from score_category import ScoreCategory as SC
from decorators import StateBoundAction
from illegal_action import IllegalAction


class Yahtzee (object):
	
	def __init__(self):
		self._dice = Dice(5,6)
		self._scorecard = Scorecard()
		self._cur_rolls = 0
		self._game_state = GS.NEED_ROLL
		
		self._state_action_map = {
			GS.NEED_ROLL:[GA.ROLL, GA.RESTART],
			GS.ROLLING:[GA.ROLL, GA.HOLD, GA.SCORE, GA.RESTART],
			GS.NO_MORE_ROLLS:[GA.SCORE, GA.HOLD, GA.RESTART],
			GS.GAME_OVER:[GA.RESTART]
		}
	
	## Properties
	@property
	def dice(self):
		return self._dice
		
	@property
	def score(self):
		return self._scorecard.score
		
	@property
	def scorecard(self):
		return self._scorecard
		
	@property
	def cur_rolls(self):
		return self._cur_rolls
		
	@property
	def open_categories(self):
		return self._scorecard.get_open_categories()
		
	@property
	def available_actions(self):
		return self._state_action_map[self._game_state]
		
		
	## Game actions
	@StateBoundAction(GA.RESTART)
	def restart(self):
		self._scorecard.reset()
		self._dice.release_all()
		self._cur_rolls = 0
		self._game_state = GS.NEED_ROLL
		
	@StateBoundAction(GA.ROLL)
	def roll(self):
		self._dice.roll()
		self._cur_rolls += 1
		if self._cur_rolls >= 3:
			self._game_state = GS.NO_MORE_ROLLS
		else:
			self._game_state = GS.ROLLING
		return self._dice
		
	@StateBoundAction(GA.HOLD)
	def toggle_hold(self, *idxs):
		for idx in idxs:
			self._dice.toggle_hold(idx)
			
	@StateBoundAction(GA.HOLD)
	def hold(self, *idxs):
		for idx in idxs:
			self._dice.hold(idx)
			
	@StateBoundAction(GA.HOLD)
	def release(self, *idxs):
		for idx in idxs:
			self._dice.release(idx)
		
	@StateBoundAction(GA.SCORE)
	def score_dice_as(self, category):
		if self._scorecard.is_category_open(category):
			score = self._scorecard.score_as(self._dice, category)
			o = self._scorecard.get_num_open_categories()
			if o == 0:
				self._game_state = GS.GAME_OVER
			else:
				self._cur_rolls = 0
				self._dice.release_all()
				self._game_state = GS.NEED_ROLL
			return score
		else:
			raise IllegalAction('The "%s" category is already filled' % category)
			
	def get_potential_score_for(self, category):
		return self._scorecard.score_as(self._dice, category, False)
			
	## public
	def is_game_over(self):
		return self._game_state == GS.GAME_OVER
	

if __name__ == '__main__':
	y = Yahtzee()
	print(y.roll().values)
	print(y.roll().values)
	print(y.roll().values)
	try:
		y.roll()
	except Exception as ex:
		print(ex)
	try:
		y.hold(0)
	except Exception as ex:
		print(ex)
