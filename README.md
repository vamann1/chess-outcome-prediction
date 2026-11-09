# chess-outcome-prediction
This project is meant to find out how early the result of a chess game at an amateur level(<1000ELO, TBD) can be predicted. The research question I want to answwer is: How can you predict the outcome of an amateur game of chess, and which factors matter most?

I will be using the lichess.org database, and narrow down my analysis to a few thousand/tens of thousands of games, as there are millions of game in the database for just one month at a time. In this database there are also engine evaluations for 6% of the games, and I could also use these games in particular to predict whether amateur players maintain an early advantage throughout the game and end up winning. Each game is in PGN(Portable Game Notation) format and the evaluations are formatted as JSON. 

The features I'll be using are split into two groups. Pre-game factors are rating difference, colour, opening played, time control of the match, time of day. In-game factors are measured at moves 10, 15 and 20: material balance, castling early, early queen moves, blundering and remaining clock time. The evaluation mentioned above would also be an in-game factor. 

I will be using scikit-learn.
I will train a regression model, and a random forest model, compare them, and interpret the results
I would also like to make meaningful visualisations of chess games and graphs, but I need to think what specifically in more detail(I also mean some visualisations of the game board itself, not just data graphs).
