"""
Data models for the Online Examination System
"""

class Student:
    def __init__(self, db_id, student_id, full_name, email=None):
        self.db_id = db_id
        self.student_id = student_id
        self.full_name = full_name
        self.email = email
    
    def to_dict(self):
        return {
            'db_id': self.db_id,
            'student_id': self.student_id,
            'full_name': self.full_name,
            'email': self.email
        }

class Category:
    def __init__(self, db_id, name, description=None):
        self.db_id = db_id
        self.name = name
        self.description = description
    
    def to_dict(self):
        return {
            'db_id': self.db_id,
            'name': self.name,
            'description': self.description
        }

class Question:
    def __init__(self, db_id, question_text, option_a, option_b, option_c, option_d, 
                 correct_answer, category_id, category_name=None, difficulty_level='Medium'):
        self.db_id = db_id
        self.question_text = question_text
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_answer = correct_answer
        self.category_id = category_id
        self.category_name = category_name
        self.difficulty_level = difficulty_level
    
    def to_dict(self):
        return {
            'db_id': self.db_id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'correct_answer': self.correct_answer,
            'category_id': self.category_id,
            'category_name': self.category_name,
            'difficulty_level': self.difficulty_level
        }

class ExamResult:
    def __init__(self, db_id, student_db_id, category_db_id, score, total_questions, 
                 percentage, time_taken, submitted_at, student_name=None, student_id=None, category_name=None):
        self.db_id = db_id
        self.student_db_id = student_db_id
        self.category_db_id = category_db_id
        self.score = score
        self.total_questions = total_questions
        self.percentage = percentage
        self.time_taken = time_taken
        self.submitted_at = submitted_at
        self.student_name = student_name
        self.student_id = student_id
        self.category_name = category_name
    
    def to_dict(self):
        return {
            'db_id': self.db_id,
            'student_db_id': self.student_db_id,
            'category_db_id': self.category_db_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': self.percentage,
            'time_taken': self.time_taken,
            'submitted_at': self.submitted_at,
            'student_name': self.student_name,
            'student_id': self.student_id,
            'category_name': self.category_name
        }
    
    def get_grade(self):
        if self.percentage >= 90: return "A"
        elif self.percentage >= 80: return "B"
        elif self.percentage >= 70: return "C"
        elif self.percentage >= 60: return "D"
        else: return "F"