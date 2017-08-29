# PyFEA
Basic FE program on Python with unique GUI to input boundary conditions

*INTRODUCTION*

This is a program written to integrate finite element analysis solver with a unique GUI setting which helps in applying boundary condition at nodal level. The intention of the developers is to create a basic linear solver which provides basic framework which seperates connectivity table, material properties, boundary conditions for formulation of a finite element problem and its solving techniques in a relatively easy fashion so that the treatment of each parameter can be controlled by the user.This framework could be used to test different types of algorithms- explicit, implicit, linear, non-linear and many others.Another important part of the program is the GUI which can help the user to visualize their test problem for the algorithm and apply boundary conditions in such a way so that they have to total control over each and every node and element. It may be noted that one could use a simple txt file to input the problem as well following the documented rules on other file but as the user starts creating higher quantity elements it becomes difficult to analyze position and value of each point by simple txt output and visual could be a big support.Currently we are still on development stage and we are rigorously testing the complete system.

*PRE-REQUISITES*

In order to run the system you will need 
- Python 2.7 runtime environment
- Numpy, Scipy, Matplotlib and KIVY library installed up until latest version

*CONTRIBUTING*

We are currently in development stage and would love some feedback on almost any aspect of this software. In order to make any changes to the code to meet your requirement you can either write to us at sambhavpyfea@gmail.com and/or you can put a pull request from SambhavPyFEA.

*SCOPE*

The scope for this project is to be able to test and develop new techniques for solving finite element problems using much more comprehensive methods. A few may involve statistical analysis of displacement, algorithm for automated boundary conditions generation, generative component design and many others. 

