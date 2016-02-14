## A simple tea timer for the brewery of excellent tea
__author__ = "Michael Knierim"


from tkinter import *

## ===========================
## CONSTANTS

# Application Frame Dimensions
F_WIDTH = 690
F_HEIGHT = 435

# Application Colors
C_PALE_GREEN = "#F5FFCE"
C_BRIGHT_GREEN = "#C9F621"
C_DARK_GREEN = "#617610"



## ===========================
## DATA DEFINITIONS

## Tea is Tea(String, Tupel)
## interp. the kind of tea and it's specific infusion times
##	- tea_kind is the unique name of the kind of tea
##	- infusion_times is a tuple containing times in seconds for first, second and third infusion
class Tea(object):
	def __init__(self, tea_kind, infusion_times):
		self.tea_kind = tea_kind
		self.infusion_times = infusion_times

P_SENCHA = Tea("Premium Sencha", (180,30,300))		# temporary infusion durations
P_BANCHA = Tea("Premium Bancha", (120,180,240))		# temporary infusion durations

# def function_for_tea(tea):
# 	tea.tea_kind
# 	tea.infusion_times
# 	pass

## Template rules used:
##	- compound: 2 fields


## ===========================
## FUNCTIONS

# Check out PyQt as it might be a better alternative to Tkinter when it comes to creating a nice GUI

# class TeaTimerGUI:
# 		def __init__(self, master):
# 				self.master = master
# 				master.title("A simple GUI")

# 				self.frame = Frame(master, bg=C_PALE_GREEN, width=F_WIDTH, height=F_HEIGHT)
# 				self.frame.grid()

# 				self.label = Label(self.frame, text="This is our first GUI!")
# 				self.label.grid(columnspan=2)

# 				self.p_sencha_button = Button(self.frame, text="Premium Sencha", bg=C_DARK_GREEN, bd=0, command=self.infuse)
# 				self.p_sencha_button.grid(row=1)

# 				self.p_bancha_button = Button(self.frame, text="Premium Bancha", bg=C_DARK_GREEN, bd=0, command=self.infuse)
# 				self.p_bancha_button.grid(row=2)

# 		def infuse(self):
# 				print("Infusing!")

# root = Tk()
# my_gui = TeaTimerGUI(root)
# root.mainloop()
