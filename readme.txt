Evan Mead

This project is a near fully fledged version of the game solitaire inplemented in Python.

Solitaire is a card game about organizing and manipulating a set of cards based on specific conditions.
The game focuses on a table of face-down cards randomly set up in rows, the last card in each row is fliped over.
you need to organize the cards in the row in descending order with mix-matching colors.
Cards can be discarded by placing them in the ace-stacks on the right of the table, each stack must start with the ace and all cards placed in
the stack must be in accending order and of the same suiut and color.
The game is solved when all cards are discarded in storage and the deck and table are clear.

This program uses the pygame module for visual display and interaction.

This program implements some 'quality-of-life' functionality to the game, such as keeping track of the 'moves' or altercations
made to the table. As well as automatically detecting when the deck is solved, when the deck and hand is empty and all cards on the
table are face up. When this is true, the game closes as and informs the player that the deck has been solved with [n] moves.