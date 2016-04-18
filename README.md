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



Course of Action
--------------------------------------------------------------
**Next steps**
	- Make transitions between states smoother (e.g. fade buttons in&out)
		+ * Fix some details in button fade animations (timing & spaghetti code)
		+ I might also use the same transitions to animate the clock (pulsing) before the countdown starts (here setLoopCount(nr of loops) should help)


**Key Functionality**
	- Functionality for user to change tea (not only in data but in front-end)
	- Functionality to store teas (in order to switch them out easily later)


**Appearance**
	- Include Display of finished tea (pulsing image of a herbal leaf + text notification)
	- Make the timer display blink before it starts (to show pause at start)
	- Change background and font color of main window continuously as infusion is getting closer to stop.


**Deployment**
	- Figure out how to pack & deploy so that people can use it without having to install PyQt
    	+ Currently this seems problematic using PyInstaller (stackoverflow post has been initiated)
    	+ If this does not get solved, consider switching to cx_Freeze
    	+ I could try PyInstaller again now that I have reinstalled Python and PyQt with Homebrew...
	- Finish documentation (Comments & Readme)
	- Deploy on GitHub