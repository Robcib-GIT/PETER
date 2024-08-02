# PETER INVERSE KINEMATICS

## PETER SIMULATOR

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


## PETER RANDOM DATA GENERATION

The purpose of the script 'PETER_random_data.py' is to generate random simulation data on the final effector positions of the robot given different configurations of actuation times for its actuators. These data are stored in a CSV file for subsequent use in training machine learning models.

## Requirements

- Python 3.x
- The following Python libraries:
  - numpy
  - pandas

## Use

1. Select number of modules.
2. Adjust constants.
3. Select number of simulations

The script runs and generates a file simulacion_random.csv with the following columns:

- Valvei_0, Valvei_1, Valvei_2: Actuation times of the valves for each module.
- Final_Effector_X, Final_Effector_Y, Final_Effector_Z: Final coordinates of the effector.

These data can be used to train machine learning models to predict the required actuation times to reach a desired final position of the effector.

## PETER TRAINING NEURAL NETWORK

The script PETER_trainning_NN.py trains a neural network to predict the actuation times of the valves in a modular soft robot (PETER) based on the desired final effector positions. The trained model can then be used to control the robot by providing the necessary actuation times to reach a specific position.

## Requirements

- Python 3.x
- The following Python libraries:
  - numpy
  - pandas
  - sklearn
  - tensorflow
  - matplotlib
  - joblib

  ## Use 

  1. Before running this script, ensure that the CSV file simulacion_random.csv exists in the same directory. This CSV file should contain the simulation data with columns for the final effector positions and the corresponding valve actuation times.
  2. Run the code.
  3. Close the 'Loss function' graph to save the model.


## PETER IK NN

The script PETER_IK_NN.py uses a pre-trained neural network model to predict the actuation times of the valves in a modular soft robot (PETER) based on the desired final effector positions input by the user. It features a graphical user interface (GUI) for easy interaction.

## Requirements

- Python 3.x
- The following Python libraries:
  - numpy
  - pandas
  - tensorflow
  - tkinter
  - joblib

## Use

 1. Before running this script, ensure that 'modelo_entrenado_optimizado.keras' and 'scaler.pkl' files exists in the same directory.
 2. Run the code.
 3. Enter the desired X, Y, Z coordinates in the respective input fields.
 4. Click the "Predecir" button to get the predicted valve actuation times.
 5. The predicted actuation times will be displayed in the GUI next to the respective valve labels.