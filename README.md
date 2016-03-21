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
	* Finish alignment of minimize button (probably create new grid and place it inside a container title row of the current grid?)
	* Finish securing that window can only be moved by clicking the title bar not the whole window
		- I see two options for making the window moveable:
			1. Figure out how to exclude the areas in which there are QPushButtons from being affected by the Eventhandlers (check if cursor is over Button area)
			2. Find a way to separate the event handler action from children of Form instance (i.e. not work on PushButtons)

**Key Functionality**
	- Functionality for user to change tea (not only in data but in front-end)
	- Functionality to store teas (in order to switch them out easily later)

**Appearance**
	- Specify things like font, font-size, etc. so that app looks similar on different platforms
	- Include Display of finished tea (pulsing image of a herbal leaf + text notification - or maybe make window vibrate)
	- Make the timer display blink before it starts (to show pause at start)
	- Make transitions between states smoother (e.g. fade buttons in&out)
	- Change background and font color of main window continuously as infusion is getting closer to stop.

**Deployment**
	- Figure out how to pack & deploy so that people can use it without having to install PyQt
    	+ Currently this seems problematic using PyInstaller (stackoverflow post has been initiated)
    	+ If this does not get solved, consider switching to cx_Freeze
	- Finish documentation (Comments & Readme)
	- Deploy on GitHub