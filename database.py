import sqlite3
import pandas as pd
from datetime import datetime

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
        """Initialize database with proper tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer CHAR(1) NOT NULL CHECK (correct_answer IN ('A', 'B', 'C', 'D')),
                category_id INTEGER NOT NULL,
                difficulty_level TEXT DEFAULT 'Medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create exam_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percentage REAL NOT NULL,
                time_taken INTEGER DEFAULT 0,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Insert default categories if they don't exist
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            self.insert_default_categories(cursor)
        
        # Insert sample questions if table is empty
        cursor.execute("SELECT COUNT(*) FROM questions")
        if cursor.fetchone()[0] == 0:
            self.insert_sample_questions(cursor)
        
        conn.commit()
        conn.close()
        print("Database initialized successfully with proper tables!")
    
    def insert_default_categories(self, cursor):
        """Insert default categories"""
        categories = [
            ('Computer Science', 'Programming, algorithms, and computer fundamentals'),
            ('Mathematics', 'Algebra, calculus, and mathematical concepts'),
            ('Science', 'Physics, chemistry, and biology'),
            ('General Knowledge', 'Current affairs, history, and general awareness')
        ]
        
        cursor.executemany(
            'INSERT INTO categories (name, description) VALUES (?, ?)',
            categories
        )
        print("Inserted default categories!")
    
    def insert_sample_questions(self, cursor):
        """Insert sample questions into database"""
        
        # Get category IDs
        cursor.execute("SELECT id, name FROM categories")
        categories = {row['name']: row['id'] for row in cursor.fetchall()}
        
        sample_questions = [
            # Computer Science Questions
            {
                'question_text': 'What does CPU stand for?',
                'option_a': 'Computer Processing Unit',
                'option_b': 'Central Processing Unit', 
                'option_c': 'Central Program Unit',
                'option_d': 'Computer Program Unit',
                'correct_answer': 'B',
                'category_id': categories['Computer Science'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'Which language is known as the backbone of web development?',
                'option_a': 'Python',
                'option_b': 'JavaScript',
                'option_c': 'Java',
                'option_d': 'C++',
                'correct_answer': 'B',
                'category_id': categories['Computer Science'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What does HTML stand for?',
                'option_a': 'Hyper Text Markup Language',
                'option_b': 'High Tech Modern Language',
                'option_c': 'Hyper Transfer Markup Language',
                'option_d': 'Home Tool Markup Language',
                'correct_answer': 'A',
                'category_id': categories['Computer Science'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'Which data structure uses LIFO principle?',
                'option_a': 'Queue',
                'option_b': 'Stack',
                'option_c': 'Array',
                'option_d': 'Linked List',
                'correct_answer': 'B',
                'category_id': categories['Computer Science'],
                'difficulty': 'Medium'
            },
            {
                'question_text': 'What is the time complexity of binary search?',
                'option_a': 'O(n)',
                'option_b': 'O(n log n)',
                'option_c': 'O(log n)',
                'option_d': 'O(1)',
                'correct_answer': 'C',
                'category_id': categories['Computer Science'],
                'difficulty': 'Medium'
            },
            
            # Mathematics Questions
            {
                'question_text': 'What is the result of 15 + 25 × 2?',
                'option_a': '80',
                'option_b': '65',
                'option_c': '50',
                'option_d': '40',
                'correct_answer': 'B',
                'category_id': categories['Mathematics'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What is the square root of 144?',
                'option_a': '12',
                'option_b': '14',
                'option_c': '16',
                'option_d': '18',
                'correct_answer': 'A',
                'category_id': categories['Mathematics'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What is 30% of 150?',
                'option_a': '45',
                'option_b': '35',
                'option_c': '50',
                'option_d': '40',
                'correct_answer': 'A',
                'category_id': categories['Mathematics'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What is the derivative of x²?',
                'option_a': 'x',
                'option_b': '2x',
                'option_c': '2',
                'option_d': 'x²',
                'correct_answer': 'B',
                'category_id': categories['Mathematics'],
                'difficulty': 'Medium'
            },
            {
                'question_text': 'What is the value of π (pi) approximately?',
                'option_a': '3.14',
                'option_b': '2.71',
                'option_c': '1.61',
                'option_d': '3.16',
                'correct_answer': 'A',
                'category_id': categories['Mathematics'],
                'difficulty': 'Easy'
            },
            
            # Science Questions
            {
                'question_text': 'What is the chemical symbol for Gold?',
                'option_a': 'Go',
                'option_b': 'Gd',
                'option_c': 'Au',
                'option_d': 'Ag',
                'correct_answer': 'C',
                'category_id': categories['Science'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'Which gas do plants absorb from the atmosphere?',
                'option_a': 'Oxygen',
                'option_b': 'Nitrogen',
                'option_c': 'Carbon Dioxide',
                'option_d': 'Hydrogen',
                'correct_answer': 'C',
                'category_id': categories['Science'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What is the hardest natural substance on Earth?',
                'option_a': 'Gold',
                'option_b': 'Iron',
                'option_c': 'Diamond',
                'option_d': 'Platinum',
                'correct_answer': 'C',
                'category_id': categories['Science'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What is the atomic number of Carbon?',
                'option_a': '6',
                'option_b': '12',
                'option_c': '14',
                'option_d': '8',
                'correct_answer': 'A',
                'category_id': categories['Science'],
                'difficulty': 'Medium'
            },
            {
                'question_text': 'Which planet is known as the Red Planet?',
                'option_a': 'Venus',
                'option_b': 'Mars',
                'option_c': 'Jupiter',
                'option_d': 'Saturn',
                'correct_answer': 'B',
                'category_id': categories['Science'],
                'difficulty': 'Easy'
            },
            
            # General Knowledge Questions
            {
                'question_text': 'What is the capital of Australia?',
                'option_a': 'Sydney',
                'option_b': 'Melbourne',
                'option_c': 'Canberra',
                'option_d': 'Perth',
                'correct_answer': 'C',
                'category_id': categories['General Knowledge'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'Who wrote "Romeo and Juliet"?',
                'option_a': 'Charles Dickens',
                'option_b': 'William Shakespeare',
                'option_c': 'Jane Austen',
                'option_d': 'Mark Twain',
                'correct_answer': 'B',
                'category_id': categories['General Knowledge'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'Which country is known as the Land of the Rising Sun?',
                'option_a': 'China',
                'option_b': 'Thailand',
                'option_c': 'Japan',
                'option_d': 'South Korea',
                'correct_answer': 'C',
                'category_id': categories['General Knowledge'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'What is the largest ocean on Earth?',
                'option_a': 'Atlantic Ocean',
                'option_b': 'Indian Ocean',
                'option_c': 'Arctic Ocean',
                'option_d': 'Pacific Ocean',
                'correct_answer': 'D',
                'category_id': categories['General Knowledge'],
                'difficulty': 'Easy'
            },
            {
                'question_text': 'In which year did World War II end?',
                'option_a': '1944',
                'option_b': '1945',
                'option_c': '1946',
                'option_d': '1947',
                'correct_answer': 'B',
                'category_id': categories['General Knowledge'],
                'difficulty': 'Medium'
            }
        ]
        
        for question in sample_questions:
            cursor.execute('''
                INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, 
                                     correct_answer, category_id, difficulty_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                question['question_text'],
                question['option_a'],
                question['option_b'],
                question['option_c'],
                question['option_d'],
                question['correct_answer'],
                question['category_id'],
                question['difficulty']
            ))
        
        print(f"Inserted {len(sample_questions)} sample questions!")
    
    # Student Management
    def register_student(self, student_id, full_name, email=None):
        """Register a new student or return existing one"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO students (student_id, full_name, email)
                VALUES (?, ?, ?)
            ''', (student_id, full_name, email))
            
            # Get student ID
            cursor.execute('SELECT id FROM students WHERE student_id = ?', (student_id,))
            result = cursor.fetchone()
            
            conn.commit()
            return result['id'] if result else None
            
        except Exception as e:
            conn.rollback()
            print(f"Error registering student: {e}")
            return None
        finally:
            conn.close()
    
    def get_student_by_id(self, student_db_id):
        """Get student by database ID"""
        conn = self.get_connection()
        student = conn.execute(
            'SELECT * FROM students WHERE id = ?', (student_db_id,)
        ).fetchone()
        conn.close()
        return student
    
    # Category Management
    def get_all_categories(self):
        """Get all available categories"""
        conn = self.get_connection()
        categories = conn.execute(
            'SELECT id, name, description FROM categories ORDER BY name'
        ).fetchall()
        conn.close()
        return categories
    
    def get_category_name(self, category_id):
        """Get category name by ID"""
        conn = self.get_connection()
        category = conn.execute(
            'SELECT name FROM categories WHERE id = ?', (category_id,)
        ).fetchone()
        conn.close()
        return category['name'] if category else 'Unknown'
    
    # Question Management
    def get_questions_by_category(self, category_id):
        """Get questions by category ID"""
        conn = self.get_connection()
        questions = conn.execute(
            '''SELECT q.*, c.name as category_name 
               FROM questions q 
               JOIN categories c ON q.category_id = c.id 
               WHERE q.category_id = ? 
               ORDER BY q.id''', 
            (category_id,)
        ).fetchall()
        conn.close()
        return questions
    
    def get_questions_count_by_category(self, category_id):
        """Get number of questions in a category"""
        conn = self.get_connection()
        count = conn.execute(
            'SELECT COUNT(*) as count FROM questions WHERE category_id = ?',
            (category_id,)
        ).fetchone()
        conn.close()
        return count['count'] if count else 0
    
    # Exam Results Management
    def save_exam_result(self, student_db_id, category_id, score, total_questions, percentage, time_taken=0):
        """Save exam result to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO exam_results (student_id, category_id, score, total_questions, percentage, time_taken)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_db_id, category_id, score, total_questions, percentage, time_taken))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error saving exam result: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_results(self):
        """Get all exam results with student and category info"""
        conn = self.get_connection()
        results = conn.execute('''
            SELECT er.*, s.full_name, s.student_id, c.name as category_name
            FROM exam_results er
            JOIN students s ON er.student_id = s.id
            JOIN categories c ON er.category_id = c.id
            ORDER BY er.submitted_at DESC
        ''').fetchall()
        conn.close()
        return results
    
    def get_student_results(self, student_db_id):
        """Get exam results for a specific student"""
        conn = self.get_connection()
        results = conn.execute('''
            SELECT er.*, c.name as category_name
            FROM exam_results er
            JOIN categories c ON er.category_id = c.id
            WHERE er.student_id = ?
            ORDER BY er.submitted_at DESC
        ''', (student_db_id,)).fetchall()
        conn.close()
        return results

# Create global database instance
exam_db = ExamDatabase()