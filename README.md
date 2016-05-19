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
	- Figure out how to integrate user input into program logic well (in teaMenu()) - See the book chapter on smart live modeless dialogs
	- Figure out how to store user inputs for future program uses. Right now I can think of several possibilities:
		+ Store in separate file (text file)
		+ Update code file (write into it)
		+ Serialize instance (use pickle module)


**Deployment**
	- Figure out how to pack & deploy so that people can use it without having to install PyQt
    	+ Currently this seems problematic using PyInstaller (stackoverflow post has been initiated)
    	+ If this does not get solved, consider switching to cx_Freeze
    	+ I could try PyInstaller again now that I have reinstalled Python and PyQt with Homebrew...
	- Finish documentation (Comments & Readme)
	- Deploy on GitHub