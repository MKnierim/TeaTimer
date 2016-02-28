## ===========================
## DATA DEFINITIONS

## Tea is Tea(String, Tupel)
## interp. the kind of tea and it's specific infusion times
##	- kind is the unique name of the kind of tea
##	- infusion_times is a tuple containing times in seconds for first, second and third infusion
class Tea(object):
	def __init__(self, kind, infusion_times, current_infusion):
		self.kind = kind
		self.infusion_times = infusion_times
		self.current_infusion = current_infusion

TEAONE = Tea("Premium\nSencha", (180,60,300), 1)		# temporary infusion durations
TEATWO = Tea("Premium\nBancha", (120,180,240), 1)		# temporary infusion durations

# def function_for_tea(tea):
# 	tea.tea_kind
# 	tea.infusion_times

## Template rules used:
##	- compound: 2 fields