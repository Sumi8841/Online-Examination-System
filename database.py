import sqlite3
import pandas as pd
from datetime import datetime
from models import Question, ExamResult, create_question_from_db_row, create_exam_result_from_db_row
from questions_data import SAMPLE_QUESTIONS

class ExamDatabase:
    def __init__(self, db_name='exam_system.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create and return database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with tables and sample questions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer CHAR(1) NOT NULL CHECK (correct_answer IN ('A', 'B', 'C', 'D'))
            )
        ''')
        
        # Create exam results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample questions if table is empty
        cursor.execute("SELECT COUNT(*) FROM questions")
        if cursor.fetchone()[0] == 0:
            self.insert_sample_questions(cursor)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    def insert_sample_questions(self, cursor):
        """Insert sample questions from questions_data.py into database"""
        for question in SAMPLE_QUESTIONS:
            cursor.execute('''
                INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                question['question_text'],
                question['option_a'],
                question['option_b'],
                question['option_c'],
                question['option_d'],
                question['correct_answer']
            ))
        
        print(f"Inserted {len(SAMPLE_QUESTIONS)} sample questions from questions_data.py!")
    
    def get_all_questions(self):
        """Get all questions from database as Question objects"""
        conn = self.get_connection()
        db_rows = conn.execute('SELECT * FROM questions ORDER BY id').fetchall()
        conn.close()
        
        # Convert to Question objects
        questions = [create_question_from_db_row(row) for row in db_rows]
        return questions
    
    def get_all_questions_as_dicts(self):
        """Get all questions from database as dictionaries"""
        conn = self.get_connection()
        questions = conn.execute('SELECT * FROM questions ORDER BY id').fetchall()
        conn.close()
        return questions
    
    def save_exam_result(self, student_name, score, total_questions, percentage):
        """Save exam result to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO exam_results (student_name, score, total_questions, percentage)
            VALUES (?, ?, ?, ?)
        ''', (student_name, score, total_questions, percentage))
        conn.commit()
        conn.close()
    
    def get_all_results(self):
        """Get all exam results as ExamResult objects"""
        conn = self.get_connection()
        db_rows = conn.execute('''
            SELECT * FROM exam_results 
            ORDER BY submitted_at DESC
        ''').fetchall()
        conn.close()
        
        # Convert to ExamResult objects
        results = [create_exam_result_from_db_row(row) for row in db_rows]
        return results
    
    def get_all_results_as_dicts(self):
        """Get all exam results as dictionaries"""
        conn = self.get_connection()
        results = conn.execute('''
            SELECT * FROM exam_results 
            ORDER BY submitted_at DESC
        ''').fetchall()
        conn.close()
        return results

# Create global database instance
exam_db = ExamDatabase()