# Distillation #
Data Science and Machine Learning using a distillation column simulator.

To begin with, this will be a steady-state simulator. The final goal is to convert it into a dynamic simulator.

## Table of Contents ##
1. [Motivation](#motivation)
2. [File Descriptions](#file_descriptions)
3. [Instructions for Use](#instructions_for_use)
4. [Libraries/Packages](#libraries_packages)
5. [Author](#author)

## Motivation<a name="motivation"></a> ##
This project serves the author's personal learning purposes. Developing the simulator will initially provide practice with Python classes, NumPy and SciPy. The simulator will then be used to learn and practice Data Science and Machine Learning.

## File Descriptions<a name="file_descriptions"></a> ##
There is only one Jupyter notebook file, currently.
+ **Distillation.ipynb**. This file contains all the Python code to run the simulation. The code is under development, and currently only includes a working example for a simple distillation column. This file contains the very first code and is not updated. Classes and functions in this file have been broken out into individual files.
+ **connector.py**. Connector class. Sets attributes of two Stream objects equal to each other.
+ **foust_8_11.py**. Runs Example 8.11 if Foust et al's textbook.
+ **mixer.py**. Mixer class. Mixes multiple input streams and outputs one or more streams with identical attributes (except flow rate).
+ **phy_props.py**. Specify physical properties of each component
+ **sim_utils.py**. Utility functions required for simulation.
+ **simplecolumn.py**. Class for simple distillation column.
+ **specify.py**. Class to specify attribute of a Stream object.
+ **stream.py**. Class to hold attributes of a stream.
+ **tray.py**. Class for tray in a distillation column.
+ **unit.py**. Parent class for all processing unit and stream classes.

## Instructions for Use<a name="instructions_for_use"></a> ##
Download the file in the [File Descriptions](#file_descriptions) section. Read the description to understand what the simulator includes and run it.

## Libraries/Packages<a name="libraries_packages"></a> ##
The following packages are used. The user must download and install these packages separately.
1. NumPy (https://www.numpy.org)
2. SciPy (https://www.scipy.org)
3. matplotlib (https://www.matplotlib.org)
4. pandas (https://pandas.pydata.org/pandas-docs/stable/)

## Author<a name="author"></a> ##
Ashutosh A. Patwardhan ([GitHub](https://github.com/a1pat), [LinkedIn](https://www.linkedin.com/in/ashutosh-patwardhan/))
