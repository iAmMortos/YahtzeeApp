import ui
import highscore
import dialogs
import console
from yahtzee import Yahtzee
from yahtzee_dice_view import YahtzeeDiceView
from game_action import GameAction as GA
from score_category import ScoreCategory as SC
from PIL import Image

class YahtzeeView (ui.View):
	
	def __init__(self):
		self._yahtzee = Yahtzee()
	
	def did_load(self):
		self.right_button_items = [ui.ButtonItem(image=ui.Image('iob:ios7_reload_32'), action=lambda s: self.restart(prompt=True))]
		self._highscore = highscore.get()
		self._update_title()
		
		self._dice_view = self['dice']
		self._dice_view.onrollfinished = self._handle_roll_finished
		self._dice_view.onholdchange = self._handle_hold_changed
		self._rolling = False
		
		self._roll_btn = self['roll_btn']
		self._roll_btn.action = lambda s: self._roll()	
		self._score_lbl = self['score']
		
		self._sv = self['categories']
		self._top_bonus_lbl = self._sv['top_bonus_slbl']
		self._top_total_lbl = self._sv['top_total_slbl']
		self._bonus_yahtzee_lbl = self._sv['bonus_yahtzee_slbl']
		self._bonus_yahtzee_ticks = self._sv['bonus_yahtzee_ticks']
		self._bot_total_lbl = self._sv['bot_total_slbl']
		
		self._category_buttons = {}
		self._init_score_buttons()
		self._update_views()
		
	def layout(self):
		x,y,w,h = self.frame
		dx,dy,dw,dh = self._dice_view.frame
		bx,by,bw,bh = self._roll_btn.frame
		sx,sy,sw,sh = self._sv.frame
		lx,ly,lw,lh = self._score_lbl.frame
		
		nby = dy + dh + 8
		self._roll_btn.frame = (bx,nby,bw,bh)
		self._score_lbl.frame = (lx,nby,lw,lh)
		
		nsy = nby + bh + 8
		nsh = h - 6 - dh - 8 - bh - 8
		self._sv.frame = (sx,nsy,sw,nsh)
		
	def _update_title(self):
		hs = self._highscore
		msg = ''
		if hs['score']:
			if hs['name'] != '':
				msg = ' (High Score: %s - %s)' % (hs['name'][:4], hs['score'])
			else:
				msg = ' (High Score: %s)' % hs['score']
		self.name = 'Yahtzee!%s' % msg
		
	def _make_category_dict(self, lst):
		d = {}
		for cat in lst:
			n,c = cat
			d[c] = self._make_category_btn(n, c)
		return d
		
	def _make_category_btn(self, name, category):
		btn = self._sv[name]
		btn.background_color = '#64c800'
		btn.tint_color = '#000'
		def press_action(sender):
			self._dice_view.release_all()
			score = self._yahtzee.score_dice_as(category)
			self._update_views()
			
			if self._yahtzee.is_game_over():
				self._game_over()
		btn.action = press_action
		
		return btn
		
	def _init_score_buttons(self):
		self._category_buttons = self._make_category_dict([
			('ones_sbtn', SC.ONES),
			('twos_sbtn', SC.TWOS),
			('threes_sbtn', SC.THREES),
			('fours_sbtn', SC.FOURS),
			('fives_sbtn', SC.FIVES),
			('sixes_sbtn', SC.SIXES),
			('toak_sbtn', SC.THREE_OF_A_KIND),
			('foak_sbtn', SC.FOUR_OF_A_KIND),
			('full_house_sbtn', SC.FULL_HOUSE),
			('smstr_sbtn', SC.SM_STRAIGHT),
			('lgstr_sbtn', SC.LG_STRAIGHT),
			('chance_sbtn', SC.CHANCE),
			('yahtzee_sbtn', SC.YAHTZEE)])
		
	def _update_views(self):
		actions = self._yahtzee.available_actions
		
		self._dice_view.enabled = GA.HOLD in actions
		
		self._roll_btn.enabled = not self._rolling and GA.ROLL in actions
		self._roll_btn.title = 'Roll (%s left)' % str(3 - self._yahtzee.cur_rolls)
		
		scorecard = self._yahtzee.scorecard
		self._score_lbl.text = 'Score\n%s' % scorecard.score
		
		self._top_bonus_lbl.text = str(scorecard.top_bonus)
		self._top_total_lbl.text = str(scorecard.top_score)
		self._bonus_yahtzee_ticks.text = '/'*scorecard.num_bonus_yahtzees
		self._bonus_yahtzee_lbl.text = str(scorecard.bonus_yahtzees)
		self._bot_total_lbl.text = str(scorecard.bottom_score)
		
		for cat in SC:
			btn = self._category_buttons[cat]
			score = self._yahtzee.scorecard.get_score_for(cat)
			btn.enabled = False
			if score is not None:
				btn.enabled = True
				btn.action = lambda s: None
				btn.title = str(score)
				btn.background_color = '#fff'
				btn.tint_color = '#000'
			else:
				if GA.SCORE in actions and not self._rolling:
					btn.enabled = True
					btn.title = '(%s)' % self._yahtzee.get_potential_score_for(cat)
				else:
					btn.title = ''
		
	def _roll(self):
		self._rolling = True
		self._yahtzee.roll()
		self._dice_view.roll_to(self._yahtzee.dice)
		self._update_views()
		
	@ui.in_background
	def _game_over(self):
		score = self._yahtzee.score
		msg = 'Your score is: %s' % score
		if score > self._highscore['score']:
			name = console.input_alert('High Score! Enter your name:')
			highscore.set(name, score)
			self._highscore = highscore.get()
			msg += '\nNew High Score!'
			self._update_title()
		result = dialogs.alert('GAME OVER!', msg, 'Restart', 'Quit', hide_cancel_button=True)
		if result == 1:
			self.restart()
			
	@ui.in_background
	def restart(self, prompt=False):
		result = 1
		if not self._yahtzee.is_game_over() and prompt:
			result = dialogs.alert('Start Over?', 'Progress will be lost.', 'Restart', 'Nevermind', hide_cancel_button=True)
			
		if result == 1:
			self._dice_view.reset()
			self._yahtzee.restart()
			self._init_score_buttons()
			self._update_views()
		
	def _handle_roll_finished(self):
		self._rolling = False
		self._update_views()
		
	def _handle_hold_changed(self, idx, val):
		if val:
			self._yahtzee.hold(idx)
		else:
			self._yahtzee.release(idx)
	

v = ui.load_view()
v.present('sheet')
