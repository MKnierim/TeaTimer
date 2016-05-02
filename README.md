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
	- See if I can make the color change over time into nicer code
	+ Also figure out how to apply color change without disrupting the whole qss
		* Possible but probably to complicate: rewrite style.qss and reload it every second
	+ Also figure out a way to adapt fader transitions to changing background color
	- Make transitions between states smoother (e.g. fade buttons in&out)
		+ I might also use the same transitions to animate the clock (pulsing) before the countdown starts (here setLoopCount(nr of loops) should help)


**Key Functionality**
	- Functionality for user to change tea (not only in data but in front-end)
	- Functionality to store teas (in order to switch them out easily later)


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
