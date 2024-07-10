The aim of the project is to implement a program as a virtual world simulator, which is supposed to have the structure of a two-dimensional grid of any user-specified size NxM (for 4 Points you can stop at a fixed size 20x20). 
In this world there will be simple forms of life with different behavior. 
Each of the organisms occupies exactly one field in the array, each field can contain at most one organism (in the event of a collision, one of them should be removed or moved).

The simulator has a turn-based character. 
In each turn, all organisms existing in the world have to perform an action appropriate to their type. 
Some of them will move (animal organisms), some will be immobile (plant organisms). 

In the event of a collision (one of the organisms will be in the same field as the other), one of the organisms wins, killing (e.g. wolf) or driving away (e.g. turtle) competitor. 
The order of movements of organisms in a turn depends on their initiative. The animals with the highest initiative are the first to move. In the case of animals
on the same initiative, the order is decided by the principle of seniority (the first to move is the longer-lived). 

The victory at the meeting depends on the strength of the organism, although there will be exceptions to this rule. 
With equal strength, the organism that attacked wins. A specific type of animal is man. Unlike animals, humans do not move randomly. 

The direction of its movement is determined before the start of the turn using the arrow keys on the keyboard. Humans also have a special ability that can be activated with a separate button. 
The activated ability remains active for 5 more rounds, after which it is deactivated. 
Once deactivated, an ability cannot be activated until 5 more rounds have elapsed. 

When you start the program on the board should appear a few pieces of all kinds of animals and plants. 
The program window should contain a field in which information about the results of fights, consumption of plants and others will be written events occurring in the world.
