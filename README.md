<h1>Othello</h1>
This is my first semester project that involve creating Othello game with playing algorithm in Python. The aim of the game is to have more pawns than your oponent at hte end of the game.
<h3>How to start the game</h3>
Before you try to play you need to download Pygame extension for Python. After you do this you need to copy master branch of this repository with newest commit then you open the whole folder (not just Othello_game) because otherwise assets wont load-in. Then you open Othello_graphical_interface.py file and compile it. Squere window should appeare on your screen.
<h3>How to play the game</h3>
You chose mode using mouse and chose board size using arrows. After you chose both of this things you need to press start to load the game. When you play, places on board where you can place your piec are higlighted and you need to click on the one where you want to place your pawn. In the lower left corner you can see curent scores and which color is playing. Game ends when all of the places on board are occupied with pawns or one of the players doesn't have andy pawns on board.
<h3>General thoughts</h3>
Code for Graphical interface may not look verry nice. It's like that because while I was creating it I was also learning Pygame. That code needs to be packed into one class, but unfortunately I don't have curently time for that. Algorithm I'm using for the playing algorithm is minmax algorithm with alpha beta pruning.