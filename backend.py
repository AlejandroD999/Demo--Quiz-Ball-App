import json
import os
from difflib import SequenceMatcher
import random
import extract_questions as eq

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

    def ask_question(self):
        
        if not self._data:
            self.generate_questions()
            return
                
        if self.all_asked():
            print("\nAll questions have been answered...")
            print(" Generating new questions")
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


    def get_answer(self, index):
        #Get Answer
        answer = input("Answer: ")

        #Check Answer
        if self.check_answer(answer, index):
            print("✅ Correct!")
            self.score += 1

        else:
            print(f"Incorrect!!\nCorrect answer is {self._data[index]["correctAnswer"]}")

        self.total_questions_answered += 1


    def check_answer(self, answer, index):
        correct_answer = str(self._data[index]['correctAnswer'])

        try:
            answer_num = float(answer)
            correct_num = float(correct_answer)

            #True if ratio is <= 0.01
            return abs(answer_num - correct_num) <= 0.01
        except ValueError:
            return self.is_similar(answer, correct_answer)


    
    def is_similar(self, answer: str, correct: str, threshold: float = 0.6) -> bool:
            ratio = SequenceMatcher(None, answer.lower().strip(), correct.lower().strip()).ratio()
            return ratio >= threshold

    def display_score(self):
        print(f"\nJob well done.\nYour score is {self.score}/{self.total_questions_answered}")

    def generate_questions(self):
        eq.extract()
        self.load_questions()
        self.asked_questions.clear()

    def all_asked(self):
        return True if len(self.asked_questions) >= len(self._data) else False    

if __name__ == "__main__":
    q = Quiz()
    q.load_questions()

    while not q.all_asked():
        que = q.ask_question()

        print(que["text"])

        q.get_answer(que["index"])

    q.display_score()
