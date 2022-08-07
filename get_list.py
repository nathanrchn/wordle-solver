# nathan ranchin

from tqdm import tqdm
from numpy import array, save


def compute_pattern(word: str, solution: list):
    result = ["0"]*len(word)
    for i in range(len(word)):
        if word[i] == solution[i]:
            result[i] = "2"
            solution[i] = "-"

    for i in range(len(word)):
        if result[i] != "0":
            continue

        found = False
        for j in range(len(word)):
            if word[i] == solution[j]:
                solution[j] = "-"
                found = True
                break
        if found:
            result[i] = "1"

    return result


with open("words.txt", "r") as words:
    word_list = words.read().splitlines()

matrix = []

for i in tqdm(range(len(word_list))):
    m = []
    for n in range(len(word_list)):
        m.append("".join(compute_pattern(word_list[i], list(word_list[n]))))
    matrix.append(m)

matrix = array(matrix)
save("wordle.npy", matrix)
