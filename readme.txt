sjwang2 - Sarah Wang

Title - Perennial Summer
My project is an isometric game that takes place during the summer. 
The player can navigate an infinitely generated terrain composed of hills, trees, grass, and clouds using arrow keys. 
The game is aimed to be peaceful and reflective; one of the features for user interaction is a journal where the user can write down their thoughts.
The game’s colors change in response to emotions the user displays in the journal.
In addition, the user can interact with the landscape by performing actions such as picking fruits. 
Another feature is a "home" location, where the user can cook recipes using fruits or items located in the cabinet / fridge areas. 


How to run 
If running once, then everything should work w/o additional modifications
If running more than once, to reset everything:
journal.txt should have nothing in it
date.txt should only have "6/1" in it (without quotes)
feeling.txt should only have "happy" (without quotes)

Libraries
random
pygame (needs to be installed)
text2emotion (needs to be installed) using:
pip install text2emotion
Link: https://pypi.org/project/text2emotion/


Shortcut commands:
Two ways to get 4 different color variations (first way is better):
1. At bed screen (has image of player sleeping), press "h" for happy, "s" for sad, "l" for neutral", "a" for anxious and press "y" to move onto next day
2. changing feeling.txt to contain one word, which can be either "happy", "sad", "neutral", or "anx" w/o quotes and re-running



