from autocorrect import Speller

class WordRecognition:
    def __init__(self, min_consecutive_letter = 8, min_word_break = 100):
        self.min_consecutive_letter = min_consecutive_letter # Minimum frames of same letter required to register as a letter
        self.min_word_break = min_word_break # Minimum number of frames needed to register as a break between words
        self.num_consecutive_letter = 0 # Number of consecutive frames for the current letter
        self.num_consecutive_unknown = 0
        self.curr_letter = '' # current letter from most recent frame
        self.curr_word = '' # current word from recent egistered letter groupings
        self.word_is_finished = False # Word is finished if min_consecutive_unknown is reached
        self.past_word = ''
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
        self.correct = Speller()
    def get_letter(self, letter_num):
        return self.letters[letter_num]

    def is_letter(self, letter):
        if letter == self.curr_letter:
            self.num_consecutive_letter += 1
        else:
            self.num_consecutive_letter = 0
        if self.num_consecutive_letter == self.min_consecutive_letter:
            return True
        else:
            return False


    def add_letter(self, letter_num):
        # Letter is unknown
        if letter_num == -2:
            self.num_consecutive_unknown +=1
            if self.num_consecutive_unknown < self.min_word_break:
                self.past_word = ''
            if self.num_consecutive_unknown == self.min_word_break:
                self.past_word = self.correct(self.curr_word)
            if self.num_consecutive_unknown > self.min_word_break:    
                self.curr_word = ''
            return self.curr_word
        if letter_num == -1:
            return
        letter = self.get_letter(letter_num)
        if self.is_letter(letter):
            if self.num_consecutive_unknown > self.min_word_break:
                self.num_consecutive_unknown = 0
            self.curr_word = self.curr_word + letter
        self.curr_letter = letter
        return self.curr_word

    def find_word(self):
        return self.correct(self.curr_word)

    def past_word(self):
        return self.correct(self.past_word)