import console
from yahtzee import Yahtzee
from game_state import GameState as GS
from game_action import GameAction as GA
from score_category import ScoreCategory as SC
from text_utils import title_caps

class TextYahtzee (object):
	
	def __init__(self):
		self._yahtzee = Yahtzee()
		self._running = False
		self._pristine = True
		
	
	## properies
	
	@property
	def dice_str(self):
		s = ''
		for d in self._yahtzee.dice:
			s += ('{%s}' if d.held else '[%s]') % d.value
		return s
		
	
	## private
	
	def _main_game_loop(self):
		print()
		rolls = self._yahtzee.cur_rolls
		if rolls > 0:
			print(self.dice_str)
		if self._yahtzee.is_game_over():
			print('GAME OVER!')
		else:
			print('%s rolls remain.' % (3 - rolls))
		print('Score: %s' % self._yahtzee.score)
		actions = self._yahtzee.available_actions
		print('What would you like to do?')
		for i,a in enumerate(actions):
			print('  %s: %s' % (i+1, title_caps(a)))
		print('  ---')
		print('  9: Show Scorecard')
		print('  0: Quit')
		print()
		user_in = input()
		int_in = None
		# validate input is int
		try:
			int_in = int(user_in)
		except Exception:
			print('"%s" is not a valid option.' % user_in)
			return
		
		if int_in == 0:
			self.quit()
		elif int_in == 9:
			self._print_score()
		elif (int_in - 1) in range(len(actions)):
			self._do_action(actions[int_in - 1])
		else:
			print('"%s" is not one of the options.' % int_in)
			
	def _do_action(self, action):
		if action is GA.ROLL:
			self._roll()
		elif action is GA.HOLD:
			self._hold()
		elif action is GA.SCORE:
			self._score()
		elif action is GA.RESTART:
			self._restart()
		else:
			raise('Error: no such action')
			
	def _roll(self):
		self._pristine = False
		self._yahtzee.roll()
			
	def _hold(self):
		didxs = input('Which dice should hold? (ex. 145): ')
		dice = []
		for c in didxs.strip():
			if c in '12345' and c not in dice:
				dice += [int(c)]
		self._yahtzee.toggle_hold(*[i-1 for i in dice])
		
	def _score(self):
		sc = self._yahtzee.scorecard
		open_cats = sc.get_open_categories()
		dice = self._yahtzee.dice
		idx = 0
		cats = []
		print('- Top Categories')
		for cat in SC.top_categories():
			if cat in open_cats:
				potential = sc.get_potential_score_for(dice ,cat)
				print(' %s: %s (%s)' % (idx+1, title_caps(cat), potential))
				cats += [cat]
				idx += 1
		print('- Bottom Categories')
		for cat in SC.bottom_categories():
			if cat in open_cats:
				potential = sc.get_potential_score_for(dice, cat)
				print(' %s: %s (%s)' % (idx+1, title_caps(cat), potential))
				cats += [cat]
				idx += 1
		print('\n 0: Cancel')
		while True:
			i = input('\nScore your dice in which category?: ')
			try:
				cidx = int(i)
				if cidx == 0: # cancel
					break
				elif (cidx - 1) in range(len(cats)):
					c = cats[cidx - 1]
					p = self._yahtzee.score_dice_as(c)
					print('Scored %s points as %s!' % (p, title_caps(c)))
					break
				else:
					raise Exception()
			except Exception:
				print('"%s" is not one of the options' % i)
				
				
		
	def _restart(self):
		if self._yahtzee.is_game_over() or self._pristine:
			self._yahtzee.restart()
		else:
			yn = input('Are you sure you want to restart? Your score will not be saved. (y/N): ')
			if yn.lower() == 'y':
				print('Restarted!')
				self._yahtzee.restart()
		
	def _print_score(self):
		sc = self._yahtzee.scorecard
		print('=== Yahtzee Scorecard ===')
		print(' -- Top Categories --')
		for cat in SC.top_categories():
			s = sc.get_score_for(cat)
			print(' %s: %s' % (title_caps(cat), self._get_score_string(s)))
		print(' Top Bonus: %s' % sc.top_bonus)
		print(' - Top Total: %s' % sc.top_score)
		print(' -- Bottom Categories --')
		for cat in SC.bottom_categories():
			s = sc.get_score_for(cat)
			print(' %s: %s' % (title_caps(cat), self._get_score_string(s)))
		print(' - Bottom Total: %s' % sc.bottom_score)
		print('== Total: %s' % sc.score)
		
	def _get_score_string(self, score):
		return '-' if score is None else str(score)
		
	
	## public
	
	def start(self):
		console.clear()
		self._running = True
		print('Welcome to Yahtzee!')
		while (self._running):
			self._main_game_loop()
			
	def quit(self):
		q = False
		if self._pristine:
			q = True
		else:
			ans = input('Are you sure you want to quit? (y/N): ')
			if ans.lower() == 'y':
				q = True
		if q:
			self._running = False
			print('Seeya!')
		
		

if __name__ == '__main__':
	ty = TextYahtzee()
	ty.start()
