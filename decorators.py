from illegal_action import IllegalAction

class StateBoundAction(object):
	def __init__(self, action):
		self.action = action
	def __call__(self, f):
		def wrapper(*args, **kwargs):
			inst = args[0]
			state = inst._game_state
			sam = inst._state_action_map
			if self.action in sam[state]:
				return f(*args, **kwargs)
			else:
				raise IllegalAction('State Restricted: Cannot call "%s()" in state "%s".' % (f.__name__, state))
		return wrapper
