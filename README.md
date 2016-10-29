# Tea Timer
This is a simple timer for the brewery of excellent tea. It allows the specification of up to two sorts of tea and three infusion times each. Users can specify tea names and infusion cycle durations directly in the front end by switching to the hidden menu (button upper right). Different infusion times are selected based on the number of clicks on a button.

![Screenshot Tea Timer](/resources/imgs/screenshot.jpg "screenshot tea timer")


## Getting Started
### Prerequisites
* Python3
* Qt5
* PyQt5

### Running
To run the timer, simply execute teaTimer.py.

## Known Issues
There are still a few minor issues to be fixed. These include:
* User Input Validation
    * Skipping cycles to which the duration 0 is set.
    * Validate tea name user input so that no empty name is set.
    * Making sure that not all three tea durations can be set to 0.
* Platform-dependent GUI
    * Currently there are slight misalignments of GUI elements on other systems than OS X.

## Authors
This project was created by [Michael Knierim](https://github.com/MKnierim).

## Licensing
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
