# CS581Project
Repo for CS581 Project: Key Designer

---
## Description

This project's goal is to create a user-friendly key designer, including common US key bitting and blank standard as well as the possibility to create your own specifications.

---

## Requirements

This project is being developed in Python 3.7, using PyQt4 to design the GUI.
The list of required python libraries will be expanded.

Requirements:

- Python 3.7
- numpy 1.15.1
- numpy-stl 2.10.0
- pyqt4 4.11.4
- pyqtgraph 0.10.0

NB: The specified versions are what was used during development, no other versions have been tested but some may work nonetheless.

---

## Usage

Launch main.py.  
Choose the bitting standard in the dropdown menu or manually set the specs for the key you want to design.
Choose the height of each pin.
Inspect the sketch/model of the key.
Click "Save .STL" to save the 3D model in .stl format.

---

## TODOS

Next steps in the development:

- Add depth to bottom part for tensioning.
