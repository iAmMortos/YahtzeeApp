
import sharedlibs
sharedlibs.add_path_for('dice')
from dice import Dice

from score_category import ScoreCategory as SC

class Scorecard (object):
	
	def __init__(self):
		self.reset()
		
		
	## properties
		
	@property
	def ones(self):
		return self._score[SC.ONES]
		
	@property
	def twos(self):
		return self._score[SC.TWOS]
		
	@property
	def threes(self):
		return self._score[SC.THREES]
		
	@property
	def fours(self):
		return self._score[SC.FOURS]
		
	@property
	def fives(self):
		return self._score[SC.FIVES]
		
	@property
	def sixes(self):
		return self._score[SC.SIXES]
		
	@property							
	def top_singles(self):
		s = 0
		if self.ones: s += self.ones
		if self.twos: s += self.twos
		if self.threes: s += self.threes
		if self.fours: s += self.fours
		if self.fives: s += self.fives
		if self.sixes: s += self.sixes
		return s
					 
	@property
	def top_bonus(self):
		return 35 if (self.top_singles >= 63) else 0
	
	@property
	def top_score(self):
		return self.top_bonus + self.top_singles
		
	@property
	def sm_straight(self):
		return self._score[SC.SM_STRAIGHT]
		
	@property
	def lg_straight(self):
		return self._score[SC.LG_STRAIGHT]
		
	@property
	def full_house(self):
		return self._score[SC.FULL_HOUSE]
		
	@property
	def three_of_a_kind(self):
		return self._score[SC.THREE_OF_A_KIND]
		
	@property
	def four_of_a_kind(self):
		return self._score[SC.FOUR_OF_A_KIND]
		
	@property
	def chance(self):
		return self._score[SC.CHANCE]
		
	@property
	def yahtzee(self):
		return self._score[SC.YAHTZEE]
		
	@property
	def bonus_yahtzees(self):
		return 100 * self._bonus_yahtzees
		
	@property
	def num_bonus_yahtzees(self):
		return self._bonus_yahtzees
		
	@property
	def bottom_score(self):
		s = 0
		if self.full_house: s += self.full_house
		if self.sm_straight: s += self.sm_straight
		if self.lg_straight: s += self.lg_straight
		if self.three_of_a_kind: s += self.three_of_a_kind
		if self.four_of_a_kind: s += self.four_of_a_kind
		if self.chance: s += self.chance
		if self.yahtzee: s += self.yahtzee
		s += self.bonus_yahtzees
		return s
		
	@property
	def score(self):
		return self.top_score + self.bottom_score
		
		
	## private
		
	def _get_value_counts(self, dice):
		counts = {}
		for v in dice.values:
			counts[v] = counts.get(v, 0) + 1
		return counts
		
	def _get_unique_values(self, dice):
		unique_vals = []
		for v in dice.values:
			if v not in unique_vals:
				unique_vals += [v]
		return unique_vals
		
	def _is_yahtzee(self, dice):
		return len(self._get_unique_values(dice)) == 1
		
	def _score_bonus_yahtzee(self, dice, commit):
		possible_score = 100
		if self._is_yahtzee(dice) and self.yahtzee:
			if commit:
				self._bonus_yahtzees += 1
			return possible_score
		return 0
		
	def _score_single(self, num, dice, commit=True):
		bonus = self._score_bonus_yahtzee(dice, commit)
		score = 0
		old_top_score = self.top_singles
		for die in dice:
			if die.value == num:
				score += num
		if old_top_score < 63 and old_top_score + score >= 63:
			bonus += 35
		if commit:
			if num == 1 and self.ones == None:
				self._score[SC.ONES] = score
			elif num == 2 and self.twos == None:
				self._score[SC.TWOS] = score
			elif num == 3 and self.threes == None:
				self._score[SC.THREES] = score
			elif num == 4 and self.fours == None:
				self._score[SC.FOURS] = score
			elif num == 5 and self.fives == None:
				self._score[SC.FIVES] = score
			elif num == 6 and self.sixes == None:
				self._score[SC.SIXES] = score
		return score + bonus
		
	def _score_full_house(self, dice, commit=True):
		possible_score = 25
		bonus = self._score_bonus_yahtzee(dice, commit)
		if bonus:
			if commit and self.full_house == None:
				self._score[SC.FULL_HOUSE] = possible_score
			return possible_score + bonus
			
		counts = self._get_value_counts(dice)
		score = possible_score if (len(counts) == 2 and list(counts.values())[0] in [2,3]) else 0
		
		if commit and self.full_house == None:
			self._score[SC.FULL_HOUSE] = score
		return score
			
	def _score_straight(self, is_large, dice, commit=True):
		req_seq = 5 if is_large else 4
		possible_score = 40 if is_large else 30
		bonus = self._score_bonus_yahtzee(dice, commit)
		if bonus:
			if commit:
				if is_large and self.lg_straight == None:
					self._score[SC.LG_STRAIGHT] = possible_score
				elif not is_large and self.sm_straight == None:
					self._score[SC.SM_STRAIGHT] = possible_score
			return possible_score + bonus
				
		unique_vals = self._get_unique_values(dice)
		last_val = None
		cur_seq = 0
		longest_seq = 1
		for v in sorted(unique_vals):
			if last_val and v == last_val + 1:
				seq += 1
				if seq > longest_seq:
					longest_seq = seq
			else:
				seq = 1
			last_val = v
					
		score = possible_score if longest_seq >= req_seq else 0
		if commit:
			if is_large and self.lg_straight == None:
				self._score[SC.LG_STRAIGHT] = score
			elif not is_large and self.sm_straight == None:
				self._score[SC.SM_STRAIGHT] = score
		return score
		
	def _score_kinds(self, is4, dice, commit=True):
		bonus = self._score_bonus_yahtzee(dice, commit)
		req_kind = 4 if is4 else 3
		counts = self._get_value_counts(dice)
		score = dice.value if max(counts.values()) >= req_kind else 0
		if commit:
			if is4 and self.four_of_a_kind == None:
				self._score[SC.FOUR_OF_A_KIND] = score
			elif not is4 and self.three_of_a_kind == None:
				self._score[SC.THREE_OF_A_KIND] = score
		return score + bonus
		
	def _score_chance(self, dice, commit=True):
		bonus = self._score_bonus_yahtzee(dice, commit)
		score = dice.value
		if commit and self.chance == None:
			self._score[SC.CHANCE] = score
		return score + bonus
		
	def _score_yahtzee(self, dice, commit=True):
		score = 50 if self._is_yahtzee(dice) else 0
		if commit and self.yahtzee == None:
			self._score[SC.YAHTZEE] = score
		return score
		
		
	## public
	
	def reset(self):
		self._score = {
			SC.ONES: None,
			SC.TWOS: None,
			SC.THREES: None,
			SC.FOURS: None,
			SC.FIVES: None,
			SC.SIXES: None,
			SC.SM_STRAIGHT: None,
			SC.LG_STRAIGHT: None,
			SC.FULL_HOUSE: None,
			SC.THREE_OF_A_KIND: None,
			SC.FOUR_OF_A_KIND: None,
			SC.CHANCE: None,
			SC.YAHTZEE: None
		}
		self._bonus_yahtzees = 0
		
	def get_all_scores(self):
		return self._score
		
	def get_score_for(self, category):
		if category in SC:
			return self._score[category]
		else:
			raise ValueError('No such score category: %s' % c)
		
	def score_as(self, dice, category, commit=True):
		c = category
		singles = [SC.ONES, SC.TWOS, SC.THREES, SC.FOURS, SC.FIVES, SC.SIXES]
		
		if c in singles:
			return self._score_single(singles.index(c) + 1, dice, commit)
		elif c is SC.FULL_HOUSE:
			return self._score_full_house(dice, commit)
		elif c is SC.SM_STRAIGHT:
			return self._score_straight(False, dice, commit)
		elif c is SC.LG_STRAIGHT:
			return self._score_straight(True, dice, commit)
		elif c is SC.THREE_OF_A_KIND:
			return self._score_kinds(False, dice, commit)
		elif c is SC.FOUR_OF_A_KIND:
			return self._score_kinds(True, dice, commit)
		elif c is SC.CHANCE:
			return self._score_chance(dice, commit)
		elif c is SC.YAHTZEE:
			return self._score_yahtzee(dice, commit)
		else:
			raise ValueError('Not a valid score category: %s' % c)
			
	def get_potential_score_for(self, dice, category):
		return self.score_as(dice, category, False)
			
	def is_category_open(self, category):
		return self.get_score_for(category) == None
			
	def get_open_categories(self):
		cs = []
		for c in SC:
			if self.is_category_open(c):
				cs += [c]
		return cs
		
	def get_num_open_categories(self):
		return len(self.get_open_categories())
		
	def get_filled_categories(self):
		cs = []
		for c in SC:
			if not self.is_category_open(c):
				cs += [c]
		return cs
		
	def get_num_filled_categories(self):
		return len(self.get_filled_categories())
		
		
		
if __name__ == '__main__':
	sc = Scorecard()
	print(sc.get_all_scores())
