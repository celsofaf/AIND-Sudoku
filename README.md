# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint propagation, roughly speaking, is about applying problem constraints repeatedly over (potentialy all) relevant subsets of our problem. In sudoku, our relevant subsets are called *units*, where a unit is either a full line, a full column, or a 3x3 square. Every unit has 9 available places, and the digits from 1 to 9 have to be distributed over each unit, each digit appearing exactly once on every unit. For the Naked Twins problem, the only relevant units are those containing *pairs* of boxes containing exactly 2 digits remaining on them, and the same 2 digits - lets call them *ab*. On those units, we may finaly exclude the digits *ab* from the remaining 7 boxes, and we are done.  

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: I have used the two methods implemented on earlier classes: *eliminate* and *only_choice*, coupled with a search tree, as it was implemented before, with the same constraints as before. But, since we now have a new rule (sudoku is now a *diagonal* sudoku), I had to take this new rule into account. I did it in a simple way: all I did was adding two more units to the unit set: the two diagonals. And it was enough to solve the problem. ;-)  

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

