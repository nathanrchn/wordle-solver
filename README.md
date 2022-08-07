# Wordle-solver
## What is Wordle-solver ?
Wordle-solver is an algorithm that solves the French Wordle with 5 letter words. This algorithm uses the mathematical concept of Entropy.

## Usage
To use the Wordle-solver, you need a list of words. Then, to create the sequence matrix, you just need to run the file get_matrix.py.
```python
from get_list import get_list

get_list() # It will create a file named wordle.npy
```

Then here is an example of use:
```python
from wordle import Wordle

Wordle("wordle.npy", "words.txt").play()
```
Then follow the insctructions.

If you want to do a benchmark on the word-list, simply run:
```python
from wordle import Wordle

Wordle("wordle.npy", "words.txt").benchmark(5069) # The number of games
```
