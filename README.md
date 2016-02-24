# TeaTimer Application (smarTimer?)
## Title 2

### Running instructions

Here are some useful tips to help run the app:

#### Desktop

...

#### Mobile

...


### Features
* ...

## To Do

### GUI
* Make Window moveable again after removing window frame
* Add minimize button on top

### Functionality
* Figure out how to make buttons clickable multiple times before starting the timer (adjusting infusion cycle with repeated clicks) - Could be done with one shot QTimer?
* Make sure that clicking a different button resets the cycle count (don't increase if a different tea is chosen) - Maybe I could integrate the cycle state into the Tea object (in data.py) later...

### Data
* Integrate infusion times from data.py into countdown function - Could possibly be done by storing the button object in the data class?
    - Other way might be to extend the QPushButton class to store the Tea object. This way upon instantiation the Tea object is directly linked to the button

### Style
* Change background and font color of main window continously as infusion is getting closer to stop.
