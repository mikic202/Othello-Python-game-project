<h1>Othello</h1>
This is my first semester project that involved creating Othello game with playing algorithm in Python. The aim of the game is to have more pawns than your oponent at hte end of the game.
<h3>How to start the game</h3>
Before you try to play you need to download Pygame extension for Python. After you do this you need to copy master branch of this repository with newest commit then you open the whole folder (not just Othello_game) because otherwise assets wont load-in. Then you open Othello_graphical_interface.py or Window.py file and compile it. There are two files because in the Othello_graphical_interface.py file program is made of just functiona and in Window.py file program is made of Window class and its methods. Squere window should appeare on your screen.
<h3>How to play the game</h3>
You chose mode using mouse and chose board size using arrows. After you chose both of this things you need to press start to load the game. When you play, spaces on board where you can place your piec are higlighted and you need to click on the one where you want to place your pawn. In the lower left corner you can see curent scores and which color is playing. Game ends when all of the places on board are occupied with pawns or one of the players doesn't have andy pawns on board.

After game ends you can click new game button on the bottom of the screan. You will be transported to the main menu.

If you want to end the game at any point of the game you need to just click x button in the top right corner of the window.

If you want to increas or decreas dificulty level you need to open Othello_bot.py file and increase or decrease depth parameter in the chose_move method. :warning: Algorithm works better with odd depth.
<h3>General thoughts</h3>
Code for Graphical interface may not look verry nice. It's like that because while I was creating it I was also learning Pygame. That is wy i created separate Window class. Algorithm I'm using for the playing algorithm is minmax algorithm with alpha beta pruning.

One thing I would like to add in the future is scalable window.