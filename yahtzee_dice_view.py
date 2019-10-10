
import ui

import sharedlibs
sharedlibs.add_path_for('die_view')
from die_view import DieView


class YahtzeeDiceView (ui.View):
	
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		self.flex = 'WB'
		self._dvs = [DieView() for _ in range(5)]
		for dv in self._dvs:
			dv.onholdchange = self._handle_hold
			self.add_subview(dv)
		self._num_finished = 0
		self._enabled = True
		self.onholdchange = lambda i,v: None
		self.onrollfinished = lambda: None
		
	def layout(self):
		padding = 8
		x,y,w,h = self.frame
		box_size = (w - 4*padding) / 5
		for i,dv in enumerate(self._dvs):
			new_x = i * (box_size + padding)
			dv.frame = (new_x, 0, box_size, box_size)
		self.frame = (x,y,w,box_size)
		
	@property
	def enabled(self):
		return self._enabled
		
	@enabled.setter
	def enabled(self, val):
		self._enabled = val
		for dv in self._dvs:
			dv.enabled = val
		
	def roll_to(self, dice):
		self._num_finished = 0
		for i in range(5):
			dv = self._dvs[i]
			die = dice[i]
			if not die.held:
				dv.callback = lambda: self._die_finished()
				dv.roll_to(die.value)
			else:
				self._die_finished()
				
	# doesn't call the 'held' handler
	def reset(self):
		for dv in self._dvs:
			dv.reset()
				
	def release_all(self):
		for dv in self._dvs:
			dv.held = False
				
	def _die_finished(self):
		self._num_finished += 1
		if self._num_finished >= 5:
			self.onrollfinished()
				
	def _handle_hold(self, sender):
		try:
			idx = self._dvs.index(sender)
			held = self._dvs[idx].held
			self.onholdchange(idx, held)
		except Exception as ex:
			raise ex
		

if __name__ == '__main__':
	import sharedlibs
	sharedlibs.add_path_for('dice')
	from dice import Dice
	
	v = ui.View()
	v.background_color = '#fff'
	dice = Dice(5, 6)
	
	def hold_change(idx, held):
		if held:
			dice.hold(idx)
		else:
			dice.release(idx)
	
	x,y,w,h = v.frame
	dv = YahtzeeDiceView(frame=(5,5,w-10,100))
	dv.onholdchange = hold_change
	v.add_subview(dv)
	
	btn = ui.Button()
	btn.title = 'Roll'
	def rol(sender):
		btn.enabled = False
		dice.roll()
		dv.roll_to(dice)
	def re_enable_btn():
		btn.enabled = True
	dv.onrollfinished = lambda: re_enable_btn()
	btn.action = rol
	btn.frame = (5, 100, w - 10, 80)
	btn.flex = 'W'
	v.add_subview(btn)
	
	b2 = ui.Button()
	b2.title = 'Release All'
	b2.action = lambda s: dv.release_all()
	b2.frame = (5, 196, w - 10, 80)
	b2.flex = 'W'
	v.add_subview(b2)
	
	v.present('portrait')
