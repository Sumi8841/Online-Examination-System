"""
Data models for the Online Examination System
This file defines the structure of our data
"""

class Question:
    """Represents a single multiple choice question"""
    
    def __init__(self, id, question_text, option_a, option_b, option_c, option_d, correct_answer):
        self.id = id
        self.question_text = question_text
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_answer = correct_answer
    
    def to_dict(self):
        """Convert question to dictionary"""
        return {
            'id': self.id,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'correct_answer': self.correct_answer
        }
    
    def __str__(self):
        return f"Question {self.id}: {self.question_text}"

class ExamResult:
    """Represents an exam result for a student"""
    
    def __init__(self, id, student_name, score, total_questions, percentage, submitted_at):
        self.id = id
        self.student_name = student_name
        self.score = score
        self.total_questions = total_questions
        self.percentage = percentage
        self.submitted_at = submitted_at
    
    def to_dict(self):
        """Convert result to dictionary"""
        return {
            'id': self.id,
            'student_name': self.student_name,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': self.percentage,
            'submitted_at': self.submitted_at
        }
    
    def get_grade(self):
        """Calculate grade based on percentage"""
        if self.percentage >= 90:
            return "A"
        elif self.percentage >= 80:
            return "B"
        elif self.percentage >= 70:
            return "C"
        elif self.percentage >= 60:
            return "D"
        else:
            return "F"
    
    def __str__(self):
        return f"{self.student_name}: {self.score}/{self.total_questions} ({self.percentage}%)"

def create_question_from_db_row(db_row):
    """Create a Question object from database row"""
    return Question(
        id=db_row['id'],
        question_text=db_row['question_text'],
        option_a=db_row['option_a'],
        option_b=db_row['option_b'],
        option_c=db_row['option_c'],
        option_d=db_row['option_d'],
        correct_answer=db_row['correct_answer']
    )

def create_exam_result_from_db_row(db_row):
    """Create an ExamResult object from database row"""
    return ExamResult(
        id=db_row['id'],
        student_name=db_row['student_name'],
        score=db_row['score'],
        total_questions=db_row['total_questions'],
        percentage=db_row['percentage'],
        submitted_at=db_row['submitted_at']
    )