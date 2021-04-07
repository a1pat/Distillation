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
+ **Distillation.ipynb**. This file contains all the Python code to run the simulation. The code is under development, and currently only includes simulation for a Mixer. A user-specified number of streams enter the Mixer. Each stream has its own flow rate, temperature, pressure and composition. There are no reactions or phase changes. A number of identical streams leave the Mixer, each with identical temperature, pressure and composition, but (possibly) different flow rate.

## Instructions for Use<a name="instructions_for_use"></a> ##
Download the file in the [File Descriptions](#file_descriptions) section. Read the description to understand what the simulator includes and run it.

## Libraries/Packages<a name="libraries_packages"></a> ##
The following packages are used. The user must download and install these packages separately.
1. NumPy(https://www.numpy.org)
2. SciPy(https://www/scipy.org)

## Author<a name="author"></a> ##
Ashutosh A. Patwardhan ([GitHub](https://github.com/a1pat), [LinkedIn](https://www.linkedin.com/in/ashutosh-patwardhan/))
