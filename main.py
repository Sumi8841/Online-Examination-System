import streamlit as st
import database
import pandas as pd
from datetime import datetime

# Configure the page - MUST BE FIRST
st.set_page_config(
    page_title="Online Examination System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# HIDE EVERYTHING - Deploy button, menu, footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    #stMainMenu {display: none;}
    .stApp > header {display: none;}
    .stApp > footer {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .exam-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        margin: 10px 0;
    }
    .student-card {
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .question-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #00d4ff;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
db = database.exam_db

def main():
    if st.session_state.get('show_registration', False):
        show_registration_page()
    elif st.session_state.get('exam_started', False) and not st.session_state.get('submitted', False):
        show_exam_interface()
    else:
        show_homepage()

def show_homepage():
    st.markdown("<h1 style='text-align: center; color: white; font-size: 4rem; margin-bottom: 30px;'>ONLINE EXAMINATION SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START EXAM", type="primary", use_container_width=True, key="home_start_btn"):
            st.session_state.show_registration = True
            st.rerun()
    
    st.markdown("---")
    st.markdown("<h2 style='color: white; text-align: center;'>PREVIOUS EXAMINATIONS</h2>", unsafe_allow_html=True)
    show_previous_exams()

def show_registration_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("BACK", key="back_btn"):
            st.session_state.show_registration = False
            st.rerun()
    
    with col2:
        st.markdown("<h1 style='text-align: center; color: white; font-size: 3rem;'>STUDENT REGISTRATION</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("<h3 style='color: white; text-align: center;'>Enter Your Details</h3>", unsafe_allow_html=True)
            
            student_name = st.text_input("FULL NAME", placeholder="John Smith", key="name_input")
            student_id = st.text_input("STUDENT ID", placeholder="S12345", key="id_input")
            
            # Category selection
            categories = db.get_all_categories()
            category_names = [f"{cat['name']}" for cat in categories]
            category_dict = {cat['name']: cat['id'] for cat in categories}
            
            selected_category_name = st.selectbox("SELECT EXAM CATEGORY", category_names, key="category_select")
            selected_category_id = category_dict[selected_category_name]
            
            # Show questions count
            questions_count = db.get_questions_count_by_category(selected_category_id)
            st.info(f"Total questions in {selected_category_name}: {questions_count}")
            
            # Next button
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("NEXT - START EXAM", type="primary", use_container_width=True, key="next_btn"):
                    if student_name.strip() and student_id.strip():
                        # Register student and get database ID
                        student_db_id = db.register_student(student_id, student_name)
                        
                        if student_db_id:
                            st.session_state.student_db_id = student_db_id
                            st.session_state.student_name = student_name
                            st.session_state.student_id = student_id
                            st.session_state.selected_category_id = selected_category_id
                            st.session_state.selected_category_name = selected_category_name
                            st.session_state.exam_started = True
                            st.session_state.show_registration = False
                            st.session_state.current_question = 0
                            st.session_state.answers = {}
                            st.session_state.submitted = False
                            st.session_state.exam_start_time = datetime.now()
                            st.rerun()
                        else:
                            st.error("Error registering student. Please try again.")
                    else:
                        st.error("Please enter both your name and student ID!")

def show_previous_exams():
    results = db.get_all_results()
    
    if not results:
        st.markdown("""
        <div class='exam-card'>
        <h4 style='color: white; text-align: center;'>No previous exams found</h4>
        <p style='color: #ccc; text-align: center;'>Be the first to take the exam!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display last 5 unique student attempts
    displayed_students = set()
    count = 0
    
    for result in results:
        if count >= 5:
            break
            
        student_key = result['student_id']
        if student_key not in displayed_students:
            displayed_students.add(student_key)
            percentage = result['percentage']
            grade = "A" if percentage >= 90 else "B" if percentage >= 80 else "C" if percentage >= 70 else "D" if percentage >= 60 else "F"
            
            st.markdown(f"""
            <div class='student-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h4 style='color: white; margin: 0;'>{result['full_name']}</h4>
                        <p style='color: #ccc; margin: 5px 0;'>ID: {result['student_id']} | {result['category_name']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <p style='color: #00d4ff; margin: 0; font-weight: bold;'>Score: {result['score']}/{result['total_questions']}</p>
                        <p style='color: #fff; margin: 0;'>Grade: {grade}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            count += 1

def show_exam_interface():
    display_exam_questions()

def clear_student_info():
    keys_to_clear = [
        'student_db_id', 'student_name', 'student_id', 'exam_started', 
        'current_question', 'answers', 'submitted', 'show_registration', 
        'selected_category_id', 'selected_category_name', 'exam_start_time'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def display_exam_questions():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("HOME", key="home_from_exam"):
            clear_student_info()
    
    with col2:
        st.markdown("<h1 style='text-align: center; color: white; font-size: 3rem; margin-bottom: 20px;'>EXAMINATION IN PROGRESS</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-card'>
        <h3 style='color: white; text-align: center; margin: 0;'>
        Student: {st.session_state.student_name} | ID: {st.session_state.student_id} | Category: {st.session_state.selected_category_name}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get questions by category
    questions = db.get_questions_by_category(st.session_state.selected_category_id)
    total_questions = len(questions)
    
    if total_questions == 0:
        st.error(f"No questions available for {st.session_state.selected_category_name} category!")
        if st.button("BACK TO REGISTRATION"):
            st.session_state.show_registration = True
            st.session_state.exam_started = False
            st.rerun()
        return
    
    # Progress section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        progress = (st.session_state.current_question + 1) / total_questions
        st.progress(progress)
        st.markdown(f"<h4 style='text-align: center; color: white;'>Question {st.session_state.current_question + 1} of {total_questions}</h4>", unsafe_allow_html=True)
    
    # Current question
    current_q = questions[st.session_state.current_question]
    
    st.markdown(f"""
    <div class='question-container'>
        <h2 style='color: white;'>Question {st.session_state.current_question + 1}</h2>
        <h3 style='color: white;'>{current_q['question_text']}</h3>
        <p style='color: #ccc; font-style: italic;'>Category: {current_q['category_name']} | Difficulty: {current_q['difficulty_level']}</p>
    </div>
    """, unsafe_allow_html=True)
        
    # Radio buttons
    with st.container():
        options = {
            'A': current_q['option_a'],
            'B': current_q['option_b'], 
            'C': current_q['option_c'],
            'D': current_q['option_d']
        }
        
        question_key = f"q_{current_q['id']}"
        current_answer = st.session_state.answers.get(question_key, None)
        
        selected_option = st.radio(
            "SELECT YOUR ANSWER:",
            options=['A', 'B', 'C', 'D'],
            format_func=lambda x: f"{x}. {options[x]}",
            key=question_key,
            index=['A', 'B', 'C', 'D'].index(current_answer) if current_answer else 0
        )
        
        st.session_state.answers[question_key] = selected_option
    
    # Navigation
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("PREVIOUS", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
        else:
            st.button("PREVIOUS", disabled=True, use_container_width=True)
    
    with col2:
        if st.session_state.current_question < total_questions - 1:
            if st.button("NEXT", type="primary", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("SUBMIT EXAM", type="primary", use_container_width=True):
                calculate_results(questions)
    
    with col3:
        if st.button("RESTART", type="secondary", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.info("Exam restarted! All answers cleared.")
            st.rerun()
    
    with col4:
        if st.button("EXIT EXAM", type="secondary", use_container_width=True):
            clear_student_info()

def calculate_results(questions):
    score = 0
    total_questions = len(questions)
    results = []
    
    for question in questions:
        question_key = f"q_{question['id']}"
        user_answer = st.session_state.answers.get(question_key)
        correct = user_answer == question['correct_answer']
        
        if correct:
            score += 1
        
        results.append({
            'question': question['question_text'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'is_correct': correct,
            'options': {
                'A': question['option_a'],
                'B': question['option_b'],
                'C': question['option_c'],
                'D': question['option_d']
            },
            'category': question['category_name'],
            'difficulty': question['difficulty_level']
        })
    
    percentage = (score / total_questions) * 100
    
    # Calculate time taken
    time_taken = 0
    if 'exam_start_time' in st.session_state:
        time_taken = int((datetime.now() - st.session_state.exam_start_time).total_seconds())
    
    # Save to database
    success = db.save_exam_result(
        st.session_state.student_db_id,
        st.session_state.selected_category_id,
        score,
        total_questions,
        percentage,
        time_taken
    )
    
    if success:
        st.session_state.submitted = True
        st.session_state.results = results
        st.session_state.score = score
        st.session_state.percentage = percentage
        st.session_state.total_questions = total_questions
        st.session_state.time_taken = time_taken
        st.session_state.exam_started = False
        
        show_results()
    else:
        st.error("Error saving exam results. Please try again.")

def show_results():
    st.markdown("<h1 style='text-align: center; color: white; font-size: 3rem;'>EXAMINATION RESULTS</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f"""
    <div class='metric-card'>
        <h3 style='color: white; text-align: center;'>
        Student: {st.session_state.student_name} | ID: {st.session_state.student_id} | Category: {st.session_state.selected_category_name}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Score cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>SCORE</h3>
            <h2 style='color: #00d4ff;'>{st.session_state.score}/{st.session_state.total_questions}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>PERCENTAGE</h3>
            <h2 style='color: #00d4ff;'>{st.session_state.percentage:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        grade = "A" if st.session_state.percentage >= 90 else "B" if st.session_state.percentage >= 80 else "C" if st.session_state.percentage >= 70 else "D" if st.session_state.percentage >= 60 else "F"
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>GRADE</h3>
            <h2 style='color: #00d4ff;'>{grade}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status = "PASS" if st.session_state.percentage >= 60 else "FAIL"
        status_color = "#00ff88" if st.session_state.percentage >= 60 else "#ff4444"
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>STATUS</h3>
            <h2 style='color: {status_color};'>{status}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Time taken
    if hasattr(st.session_state, 'time_taken'):
        minutes = st.session_state.time_taken // 60
        seconds = st.session_state.time_taken % 60
        st.info(f"Time taken: {minutes} minutes {seconds} seconds")
    
    st.progress(st.session_state.percentage / 100)
    
    if st.session_state.percentage >= 60:
        st.success("CONGRATULATIONS! YOU PASSED THE EXAM!")
    else:
        st.error("SORRY, YOU DID NOT PASS. BETTER LUCK NEXT TIME!")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("VIEW HISTORY", use_container_width=True):
            st.session_state.show_all_results = True
            st.rerun()
    
    with col2:
        if st.button("NEW EXAM", type="primary", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.results = None
            st.session_state.exam_started = False
            st.success("READY FOR A NEW EXAM!")
            st.rerun()
    
    with col3:
        if st.button("BACK TO HOME", type="secondary", use_container_width=True):
            clear_student_info()

def view_results():
    st.markdown("<h1 style='text-align: center; color: white; font-size: 3rem;'>RESULTS HISTORY</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    results = db.get_all_results()
    
    if not results:
        st.info("No exam results found. Take an exam to see results here!")
        return
    
    # Statistics
    st.markdown("<h2 style='color: white;'>OVERALL STATISTICS</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_exams = len(results)
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>TOTAL EXAMS</h3>
            <h2 style='color: #00d4ff;'>{total_exams}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_percentage = sum([r['percentage'] for r in results]) / len(results)
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>AVERAGE SCORE</h3>
            <h2 style='color: #00d4ff;'>{avg_percentage:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        highest_score = max([r['percentage'] for r in results])
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>HIGHEST SCORE</h3>
            <h2 style='color: #00d4ff;'>{highest_score:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        passed_exams = len([r for r in results if r['percentage'] >= 60])
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: white;'>EXAMS PASSED</h3>
            <h2 style='color: #00d4ff;'>{passed_exams}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Results table
    st.markdown("<h2 style='color: white;'>ALL EXAM RESULTS</h2>", unsafe_allow_html=True)
    
    results_data = []
    for result in results:
        percentage = result['percentage']
        grade = "A" if percentage >= 90 else "B" if percentage >= 80 else "C" if percentage >= 70 else "D" if percentage >= 60 else "F"
        
        results_data.append({
            'Student Name': result['full_name'],
            'Student ID': result['student_id'],
            'Category': result['category_name'],
            'Score': f"{result['score']}/{result['total_questions']}",
            'Percentage': f"{percentage:.1f}%",
            'Grade': grade,
            'Date': result['submitted_at']
        })
    
    df = pd.DataFrame(results_data)
    st.dataframe(df, use_container_width=True)
    
    # Download
    csv = df.to_csv(index=False)
    st.download_button(
        label="DOWNLOAD RESULTS AS CSV",
        data=csv,
        file_name="exam_results.csv",
        mime="text/csv"
    )

# Initialize session state
if 'exam_started' not in st.session_state:
    st.session_state.exam_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if __name__ == "__main__":
    main()