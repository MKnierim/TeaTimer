# TeaTimer Application (smarTimer?)
**Quick Thoughts**
* ...



Features
--------------------------------------------------------------
* ...



Running instructions
--------------------------------------------------------------
Here are some useful tips to help run the application:

### Desktop
...

### Mobile
...


Dependencies
--------------------------------------------------------------
* Python3
* Qt5
* PyQt5


Course of Action
--------------------------------------------------------------
**Next steps**
	- Make transitions between states smoother (e.g. fade buttons in&out)
		+ I might also use the same transitions to animate the clock (pulsing) before the countdown starts (here setLoopCount(nr of loops) should help)
	- Make sure that user input for infusion times is user friendly - they should not have to compute the number of seconds but rather use an intuitive input format (like minutes & seconds). I think it would be fine to exclude handlers for hours here...


**Key Functionality**
	- Functionality for user to change tea (not only in data but in front-end)


**Appearance**
	- Include Display of finished tea (pulsing image of a herbal leaf + text notification)
	- Make the timer display blink before it starts (to show pause at start)


**Deployment**
	- Figure out how to pack & deploy so that people can use it without having to install PyQt
    	+ Currently this seems problematic using PyInstaller (stackoverflow post has been initiated)
    	+ If this does not get solved, consider switching to cx_Freeze
    	+ I could try PyInstaller again now that I have reinstalled Python and PyQt with Homebrew...
	- Finish documentation (Comments & Readme)
	- Deploy on GitHub
