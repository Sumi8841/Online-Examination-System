"""
Static question data for the Online Examination System
This file contains all the multiple choice questions and answers
"""

# List of all questions with their options and correct answers
SAMPLE_QUESTIONS = [
    # Programming Questions (1-5)
    {
        'id': 1,
        'question_text': 'What does CPU stand for?',
        'option_a': 'Computer Processing Unit',
        'option_b': 'Central Processing Unit', 
        'option_c': 'Central Program Unit',
        'option_d': 'Computer Program Unit',
        'correct_answer': 'B',
        'category': 'Programming'
    },
    {
        'id': 2,
        'question_text': 'Which language is known as the backbone of web development?',
        'option_a': 'Python',
        'option_b': 'JavaScript',
        'option_c': 'Java',
        'option_d': 'C++',
        'correct_answer': 'B',
        'category': 'Programming'
    },
    {
        'id': 3,
        'question_text': 'What does HTML stand for?',
        'option_a': 'Hyper Text Markup Language',
        'option_b': 'High Tech Modern Language',
        'option_c': 'Hyper Transfer Markup Language',
        'option_d': 'Home Tool Markup Language',
        'correct_answer': 'A',
        'category': 'Programming'
    },
    {
        'id': 4,
        'question_text': 'Which of these is not a Python web framework?',
        'option_a': 'Django',
        'option_b': 'Flask',
        'option_c': 'Spring',
        'option_d': 'FastAPI',
        'correct_answer': 'C',
        'category': 'Programming'
    },
    {
        'id': 5,
        'question_text': 'What is the output of: print(2 ** 3) in Python?',
        'option_a': '6',
        'option_b': '8',
        'option_c': '9',
        'option_d': '5',
        'correct_answer': 'B',
        'category': 'Programming'
    },
    
    # General Knowledge Questions (6-10)
    {
        'id': 6,
        'question_text': 'What is the capital of Australia?',
        'option_a': 'Sydney',
        'option_b': 'Melbourne',
        'option_c': 'Canberra',
        'option_d': 'Perth',
        'correct_answer': 'C',
        'category': 'General Knowledge'
    },
    {
        'id': 7,
        'question_text': 'Which planet is known as the Red Planet?',
        'option_a': 'Venus',
        'option_b': 'Mars',
        'option_c': 'Jupiter',
        'option_d': 'Saturn',
        'correct_answer': 'B',
        'category': 'General Knowledge'
    },
    {
        'id': 8,
        'question_text': 'What is the largest mammal in the world?',
        'option_a': 'Elephant',
        'option_b': 'Blue Whale',
        'option_c': 'Giraffe',
        'option_d': 'Polar Bear',
        'correct_answer': 'B',
        'category': 'General Knowledge'
    },
    {
        'id': 9,
        'question_text': 'Who wrote "Romeo and Juliet"?',
        'option_a': 'Charles Dickens',
        'option_b': 'William Shakespeare',
        'option_c': 'Jane Austen',
        'option_d': 'Mark Twain',
        'correct_answer': 'B',
        'category': 'General Knowledge'
    },
    {
        'id': 10,
        'question_text': 'Which country is known as the Land of the Rising Sun?',
        'option_a': 'China',
        'option_b': 'Thailand',
        'option_c': 'Japan',
        'option_d': 'South Korea',
        'correct_answer': 'C',
        'category': 'General Knowledge'
    },
    
    # Mathematics Questions (11-15)
    {
        'id': 11,
        'question_text': 'What is the result of 15 + 25 × 2?',
        'option_a': '80',
        'option_b': '65',
        'option_c': '50',
        'option_d': '40',
        'correct_answer': 'B',
        'category': 'Mathematics'
    },
    {
        'id': 12,
        'question_text': 'What is the square root of 144?',
        'option_a': '12',
        'option_b': '14',
        'option_c': '16',
        'option_d': '18',
        'correct_answer': 'A',
        'category': 'Mathematics'
    },
    {
        'id': 13,
        'question_text': 'What is 30% of 150?',
        'option_a': '45',
        'option_b': '35',
        'option_c': '50',
        'option_d': '40',
        'correct_answer': 'A',
        'category': 'Mathematics'
    },
    {
        'id': 14,
        'question_text': 'If x = 5 and y = 3, what is x² + y²?',
        'option_a': '64',
        'option_b': '34',
        'option_c': '16',
        'option_d': '28',
        'correct_answer': 'B',
        'category': 'Mathematics'
    },
    {
        'id': 15,
        'question_text': 'What is the value of π (pi) approximately?',
        'option_a': '3.14',
        'option_b': '2.71',
        'option_c': '1.61',
        'option_d': '3.16',
        'correct_answer': 'A',
        'category': 'Mathematics'
    },
    
    # Science Questions (16-20)
    {
        'id': 16,
        'question_text': 'What is the chemical symbol for Gold?',
        'option_a': 'Go',
        'option_b': 'Gd',
        'option_c': 'Au',
        'option_d': 'Ag',
        'correct_answer': 'C',
        'category': 'Science'
    },
    {
        'id': 17,
        'question_text': 'Which gas do plants absorb from the atmosphere?',
        'option_a': 'Oxygen',
        'option_b': 'Nitrogen',
        'option_c': 'Carbon Dioxide',
        'option_d': 'Hydrogen',
        'correct_answer': 'C',
        'category': 'Science'
    },
    {
        'id': 18,
        'question_text': 'What is the hardest natural substance on Earth?',
        'option_a': 'Gold',
        'option_b': 'Iron',
        'option_c': 'Diamond',
        'option_d': 'Platinum',
        'correct_answer': 'C',
        'category': 'Science'
    },
    {
        'id': 19,
        'question_text': 'How many bones are there in the adult human body?',
        'option_a': '206',
        'option_b': '300',
        'option_c': '150',
        'option_d': '250',
        'correct_answer': 'A',
        'category': 'Science'
    },
    {
        'id': 20,
        'question_text': 'What is the speed of light in vacuum?',
        'option_a': '299,792,458 m/s',
        'option_b': '300,000,000 m/s',
        'option_c': '150,000,000 m/s',
        'option_d': '299,792 km/s',
        'correct_answer': 'A',
        'category': 'Science'
    }
]

def get_all_questions():
    """Get all questions"""
    return SAMPLE_QUESTIONS

def get_total_questions_count():
    """Get total number of available questions"""
    return len(SAMPLE_QUESTIONS)