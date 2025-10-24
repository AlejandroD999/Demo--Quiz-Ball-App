from difflib import SequenceMatcher
import extract_questions as eq
import json
import os
import random


class Quiz:

    def __init__(self):
        self.score = 0
        self._data = None
        self.total_questions_answered = 0
        self.asked_questions = set()

    def load_questions(self):
        scripts_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            questions_dir = os.path.join(scripts_dir, "resources", "questions.json")
            with open(questions_dir, 'r') as file:
                data = json.load(file)    
            
            self._data = data
        
        except FileNotFoundError:
            print("Extraction of questions required")
            self.generate_questions()
    
    def ask_question(self):
        
        if not self._data:
            self.generate_questions()
            return
                
        if self.all_asked():
            self.generate_questions()

        question_index = self.generate_index()

        self.asked_questions.add(question_index)

        
        return {
            "index": question_index,
            "text": self._data[question_index]['question']['text']
        }

    def generate_index(self):

        random_index = random.randint(0, len(self._data) - 1)

        while random_index in self.asked_questions:
            random_index = random.randint(0, len(self._data) - 1)

        return random_index

    def get_possible_answers(self, index):
        incorrect_answers = self._data[index]["incorrectAnswers"]
        correct_answer = self._data[index]["correctAnswer"]
     
        possible_answers = []

        for incorrect_answer in incorrect_answers:
            possible_answers.append(incorrect_answer)

        possible_answers.append(correct_answer)
        random.shuffle(possible_answers)

        return possible_answers

    def generate_questions(self):
        eq.extract()
        self.load_questions()
        self.asked_questions.clear()

    def all_asked(self):
        return True if len(self.asked_questions) >= len(self._data) else False    

    def reset(self):
        self.score = 0
        self._data = None
        self.total_questions_answered = 0
        self.asked_questions.clear()


if __name__ == '__main__':
    q = Quiz()
    q.load_questions()
