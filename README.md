# TeaTimer Application (smarTimer?)
## Title 2

### Running instructions

Here are some useful tips to help run the application:

#### Desktop

...

#### Mobile

...


### Features
* ...

## Course of Action
### Must-Haves
* Figure out how to pack & deploy so that people can use it without having to install PyQt
    - Currently this seems problematic using PyInstaller (stackoverflow post has been initiated)
    - If this does not get solved, consider switching to cx_Freeze
* Finish documentation (Comments & Readme)
* Deploy on GitHub

### Delighter
* Include Display of finished tea (pulsing image of a herbal leaf + text notification - or maybe make window vibrate)
* Make the timer display blink before it starts (to show pause at start)
* Make transitions between states smoother (e.g. fade buttons in&out)
* Change background and font color of main window continuously as infusion is getting closer to stop.

### Nice-to-have
* Add minimize button on top
* Consider securing that window can only be moved by clicking the title bar not the whole window
* Refactor code (simply with the goal of improving code quality)

### Core Changes
* **!!! MUST BE DONE** - Consider making the app more abstract (general configurable timer - not just tea)
* Functionality for user to change tea (not only in data but in front-end)

