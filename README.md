# mines
## Analyze Minesweeper Scenarios

I find Minesweeper interesting because it combines pure logic with probability.  This script helps improve intuition on the probability aspect of the game by quickly computing the set of solutions associated with a given board state and summing over them to indicate the likelihood that a mine will be present in a given square.  The current version of the code doesn't handle exposed mines directly, but you can treat them as possible mines and look at the subset of the possible solutions in which they are determined to be mines.
