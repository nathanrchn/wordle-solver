# nathan ranchin

from tqdm import tqdm
from math import log2
from os import system, name
from numpy import load, array, unique


class Wordle():
    def __init__(self, matrix_file, word_list_file):
        self.matrix = load(matrix_file)
        with open(word_list_file, "r") as words:
            self.word_list = words.read().splitlines()

    def compute_pattern(self, word: str, solution: list):
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

        return "".join(result)

    def print_pattern(self, pattern: list):
        print_pattern = ""
        for i in range(len(pattern)):
            if pattern[i] == "2":
                print_pattern += "🟩"
            elif pattern[i] == "1":
                print_pattern += "🟨"
            else:
                print_pattern += "⬜️"

        return print_pattern

    def get_E(self, word_list: list, matrix):
        E = []
        for i in range(len(word_list)):
            e = 0
            o, count = unique(matrix[i], return_counts=True)
            for j in range(len(count)):
                p = (count[j]/len(word_list))
                e += p*(-log2(p))
            E.append([word_list[i], e])

        return array(E)

    def get_new_word_list(self, word_list: list, pattern: list, word: str):
        attributes_3 = []
        attributes_2 = []
        attributes_1 = []
        attributes_0 = []
        new_word_list = []
        new_attributes_0 = []

        for i in range(len(pattern)):
            if pattern[i] == "2":
                attributes_2.append([word[i], i])
            elif pattern[i] == "1":
                attributes_1.append([word[i], i])
            else:
                attributes_0.append(word[i])

        for i in range(len(attributes_0)):
            attributes_2_o = [attributes_2[j][0]
                              for j in range(len(attributes_2))]
            attributes_1_o = [attributes_1[j][0]
                              for j in range(len(attributes_1))]
            if attributes_0[i] not in attributes_1_o and attributes_0[i] not in attributes_2_o:
                new_attributes_0.append(attributes_0[i])
            else:
                try:
                    n = attributes_2_o.count(attributes_0[i])
                except:
                    n = attributes_1_o.count(attributes_0[i])
                attributes_3.append(
                    [attributes_0[i], word.count(attributes_0[i]) - n])

        attributes_0 = new_attributes_0

        word_list.pop(word_list.index(word))

        for i in range(len(word_list)):
            if all([attributes_2[j][1] in [pos for pos, char in enumerate(word_list[i]) if char == attributes_2[j][0]] for j in range(len(attributes_2))]) and all([attributes_1[j][0] in word_list[i] for j in range(len(attributes_1))]) and all([attributes_1[j][1] not in [pos for pos, char in enumerate(word_list[i]) if char == attributes_1[j][0]] for j in range(len(attributes_1))]) and all([attributes_0[j] not in word_list[i] for j in range(len(attributes_0))]) and all(word_list[i].count(attributes_3[j][0]) == attributes_3[j][1] for j in range(len(attributes_3))):
                new_word_list.append(word_list[i])

        return new_word_list

    def custom_play(self):
        system("cls" if name == "nt" else "clear")
        solution = input(str("enter a word: "))
        system("cls" if name == "nt" else "clear")

        for i in range(6):
            z = self.get_E(self.word_list, self.matrix)
            z = z[z[:, 1].argsort()[::-1]]
            print(
                f"the best option is: {z[0][0]} with a score of {round(float(z[0][1]), 2)}")
            word = input(str("enter a word: "))
            pattern = self.compute_pattern(word, list(solution))
            if pattern == "22222":
                print(f"{word} - {self.print_pattern(pattern)}")
                print(f"{word} is the solution. You find it with {i+1} tries")
                return True
            else:
                print(f"{word} - {self.print_pattern(pattern)}")
                if input(str("type q and enter to continue: ")) == "q":
                    self.word_list = self.get_new_word_list(
                        self.word_list, list(pattern), word)

                    new_matrix = []
                    for i in tqdm(range(len(self.word_list))):
                        m = []
                        for j in range(len(self.word_list)):
                            m.append("".join(self.compute_pattern(
                                self.word_list[i], list(self.word_list[j]))))
                        new_matrix.append(m)
                    self.matrix = array(new_matrix)

        return False

    def play(self):
        system("cls" if name == "nt" else "clear")

        for i in range(6):
            z = self.get_E(self.word_list, self.matrix)
            z = z[z[:, 1].argsort()[::-1]]
            print(
                f"the best option is: {z[0][0]} with a score of {round(float(z[0][1]), 2)}")
            word = input(str("enter a word: "))
            print("enter 2 for green, 1 for yellow, 0 for white")
            pattern = input(str("enter the pattern: "))
            if pattern == "22222":
                print(f"{word} - {self.print_pattern(pattern)}")
                print(f"{word} is the solution. You find it with {i+1} tries")
                return True
            else:
                self.word_list = self.get_new_word_list(
                    self.word_list, list(pattern), word)

                new_matrix = []
                for i in tqdm(range(len(self.word_list))):
                    m = []
                    for j in range(len(self.word_list)):
                        m.append("".join(self.compute_pattern(
                            self.word_list[i], list(self.word_list[j]))))
                    new_matrix.append(m)
                self.matrix = array(new_matrix)

    def benchmark(self, n: int):
        system("cls" if name == "nt" else "clear")

        good_times = 0
        number_of_bets = 0

        for i in tqdm(range(n)):
            try:
                solution = self.word_list[i]
            except:
                break

            matrix = self.matrix.copy()
            word_list = self.word_list.copy()

            for j in range(6):
                if j == 0:
                    word = "tarie"
                else:
                    z = self.get_E(word_list, matrix)
                    z = z[z[:, 1].argsort()[::-1]]
                    word = z[0][0]
                pattern = self.compute_pattern(word, list(solution))
                if pattern == "22222":
                    break
                else:
                    word_list = self.get_new_word_list(
                        word_list, list(pattern), word)
                    if len(word_list) == 0:
                        break
                    new_matrix = []
                    for k in range(len(word_list)):
                        m = []
                        for l in range(len(word_list)):
                            m.append("".join(self.compute_pattern(
                                word_list[k], list(word_list[l]))))
                        new_matrix.append(m)
                    matrix = array(new_matrix)

            if pattern == "22222":
                good_times += 1
                number_of_bets += j+1

        print(
            f"{(round(good_times/n, 2))*100}% and {round(number_of_bets/good_times, 2)} tries")
