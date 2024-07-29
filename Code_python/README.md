# PETER SIMULATOR

This project includes a simulator of the PETER soft robot, which allows to control the module inflation valves through a graphical interface. The simulator displays in real time the configuration and status of the robot, as well as the positions of the actuators and the end effector.

## Features

- Valve control by means of sliders or text inputs.
- Display of the position of the end effector.
- Possibility to save the simulation data in a CSV file.
- Possibility to choose the number of modules.

## Requirements

- Python 3.x
- The following Python libraries:
  - numpy
  - matplotlib
  - tkinter
  - pandas

## Installation

- Clone the project repository:
```sh
   git clone -b mar/develop https://github.com/Robcib-GIT/PETER
```
## Use

1. Select number of modules.
2. Adjust constants.
3. Run the code.
4. Set desired valve values in sliders or text input.
5. Click on “Actualizar simuación”.
6. Click on “Guardar datos”.
7. Repeat from step 4 until the desired data is obtained.
8. Stop simulation.