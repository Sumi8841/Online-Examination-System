import streamlit as st
import database
import pandas as pd
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Online Examination System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = database.exam_db

def main():
    # Sidebar for navigation
    st.sidebar.title("🎓 Online Exam System")
    st.sidebar.markdown("---")
    
    # Navigation
    app_mode = st.sidebar.radio("Navigate to:", 
                               ["📝 Take Exam", "📊 View Results", "ℹ️ About"])
    
    if app_mode == "📝 Take Exam":
        take_exam()
    elif app_mode == "📊 View Results":
        view_results()
    else:
        show_about()

def take_exam():
    st.title("🎓 Online Examination System")
    st.markdown("---")
    
    # Check if exam is in progress
    if st.session_state.get('exam_started', False):
        display_exam_questions()
        return
    
    # Student registration - ONLY SHOW THIS IF EXAM NOT STARTED
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Student Registration")
        student_name = st.text_input("Enter your full name:", placeholder="John Smith", key="name_input")
        student_id = st.text_input("Enter your student ID:", placeholder="S12345", key="id_input")
        
        # Start Exam Button
        if st.button("🚀 Start Exam", type="primary", key="start_button"):
            if student_name.strip() and student_id.strip():
                # Store student info in session state
                st.session_state.student_name = student_name
                st.session_state.student_id = student_id
                st.session_state.exam_started = True
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.success(f"✅ Exam started for {student_name} (ID: {student_id})!")
                st.rerun()
            else:
                st.error("❌ Please enter both your name and student ID!")
    
    with col2:
        st.subheader("📋 Exam Instructions")
        st.info("""
        **Important Instructions:**
        - This exam contains 20 multiple choice questions
        - Each question has 4 options (A, B, C, D)
        - Select only one answer per question
        - You can navigate between questions
        - Click 'Submit Exam' when finished
        - Results will be shown immediately
        - No time limit
        """)
        
        # Show current student info if available
        if st.session_state.get('student_name'):
            st.warning(f"**Current Student:** {st.session_state.student_name}")
            st.warning(f"**Student ID:** {st.session_state.student_id}")
            
            # Option to delete/clear student info
            if st.button("🗑️ Clear Student Info", type="secondary"):
                clear_student_info()

def clear_student_info():
    """Clear student information from session state"""
    keys_to_clear = ['student_name', 'student_id', 'exam_started', 'current_question', 'answers', 'submitted']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.success("✅ Student information cleared! You can register again.")
    st.rerun()

def display_exam_questions():
    st.markdown("---")
    
    # Student info header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"📝 Examination in Progress")
    with col2:
        st.info(f"**Student:** {st.session_state.student_name}")
    
    st.write(f"**Student ID:** {st.session_state.student_id}")
    st.markdown("---")
    
    # Get all questions
    questions = db.get_all_questions()
    total_questions = len(questions)
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / total_questions
    st.progress(progress)
    st.write(f"**Progress: Question {st.session_state.current_question + 1} of {total_questions}**")
    
    # Display current question
    current_q = questions[st.session_state.current_question]
    
    st.markdown(f"### Question {st.session_state.current_question + 1}")
    st.markdown(f"**{current_q.question_text}**")
    
    # Radio buttons for options
    options = {
        'A': current_q.option_a,
        'B': current_q.option_b, 
        'C': current_q.option_c,
        'D': current_q.option_d
    }
    
    # Get or initialize answer for current question
    question_key = f"q_{current_q.id}"
    current_answer = st.session_state.answers.get(question_key, None)
    
    selected_option = st.radio(
        "Select your answer:",
        options=['A', 'B', 'C', 'D'],
        format_func=lambda x: f"{x}. {options[x]}",
        key=question_key,
        index=['A', 'B', 'C', 'D'].index(current_answer) if current_answer else 0
    )
    
    # Store the answer
    st.session_state.answers[question_key] = selected_option
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous Question"):
                st.session_state.current_question -= 1
                st.rerun()
        else:
            st.button("⬅️ Previous Question", disabled=True)
    
    with col2:
        if st.session_state.current_question < total_questions - 1:
            if st.button("Next Question ➡️"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.button("Next Question ➡️", disabled=True)
    
    with col3:
        if st.button("🔄 Restart Exam", type="secondary"):
            # Clear only exam progress, keep student info
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.info("🔄 Exam restarted! All answers cleared.")
            st.rerun()
    
    with col4:
        if st.button("✅ Submit Exam", type="primary"):
            calculate_results(questions)

def calculate_results(questions):
    """Calculate and display exam results"""
    score = 0
    total_questions = len(questions)
    results = []
    
    for question in questions:
        question_key = f"q_{question.id}"
        user_answer = st.session_state.answers.get(question_key)
        correct = user_answer == question.correct_answer
        
        if correct:
            score += 1
        
        results.append({
            'question': question.question_text,
            'user_answer': user_answer,
            'correct_answer': question.correct_answer,
            'is_correct': correct,
            'options': {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d
            }
        })
    
    percentage = (score / total_questions) * 100
    
    # Save to database
    db.save_exam_result(st.session_state.student_name, score, total_questions, percentage)
    
    # Display results
    st.session_state.submitted = True
    st.session_state.results = results
    st.session_state.score = score
    st.session_state.percentage = percentage
    st.session_state.total_questions = total_questions
    
    show_results()

def show_results():
    st.markdown("---")
    st.title("🎯 Exam Results")
    
    # Student info
    st.info(f"**Student:** {st.session_state.student_name} | **ID:** {st.session_state.student_id}")
    
    # Score summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score", f"{st.session_state.score}/{st.session_state.total_questions}")
    
    with col2:
        st.metric("Percentage", f"{st.session_state.percentage:.1f}%")
    
    with col3:
        grade = "A" if st.session_state.percentage >= 90 else "B" if st.session_state.percentage >= 80 else "C" if st.session_state.percentage >= 70 else "D" if st.session_state.percentage >= 60 else "F"
        st.metric("Grade", grade)
    
    # Progress bar for score
    st.progress(st.session_state.percentage / 100)
    
    # Pass/Fail status
    if st.session_state.percentage >= 60:
        st.success("🎉 Congratulations! You passed the exam!")
    else:
        st.error("😞 Sorry, you did not pass. Better luck next time!")
    
    # Detailed results
    st.subheader("📋 Detailed Results")
    
    for i, result in enumerate(st.session_state.results, 1):
        with st.expander(f"Question {i}: {'✅ Correct' if result['is_correct'] else '❌ Incorrect'}"):
            st.write(f"**Question:** {result['question']}")
            st.write(f"**Your Answer:** {result['user_answer']}. {result['options'][result['user_answer']]}")
            st.write(f"**Correct Answer:** {result['correct_answer']}. {result['options'][result['correct_answer']]}")
            
            if result['is_correct']:
                st.success("✅ You answered correctly!")
            else:
                st.error("❌ Your answer was incorrect")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View All Results"):
            st.session_state.show_all_results = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Take New Exam"):
            # Keep student info but restart exam
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.results = None
            st.success("🔄 Ready for a new exam! Your student information is saved.")
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All & Register New"):
            clear_student_info()

def view_results():
    st.title("📊 Exam Results History")
    st.markdown("---")
    
    # Get all results from database
    results = db.get_all_results_as_dicts()
    
    if not results:
        st.info("No exam results found. Take an exam to see results here!")
        return
    
    # Convert to DataFrame for better display
    results_data = []
    for result in results:
        percentage = result['percentage']
        grade = "A" if percentage >= 90 else "B" if percentage >= 80 else "C" if percentage >= 70 else "D" if percentage >= 60 else "F"
        
        results_data.append({
            'Student Name': result['student_name'],
            'Score': f"{result['score']}/{result['total_questions']}",
            'Percentage': f"{percentage:.1f}%",
            'Grade': grade,
            'Date': result['submitted_at']
        })
    
    df = pd.DataFrame(results_data)
    
    # Display statistics
    st.subheader("📈 Overall Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Exams", len(results))
    
    with col2:
        avg_percentage = sum([r['percentage'] for r in results]) / len(results)
        st.metric("Average Score", f"{avg_percentage:.1f}%")
    
    with col3:
        highest_score = max([r['percentage'] for r in results])
        st.metric("Highest Score", f"{highest_score:.1f}%")
    
    with col4:
        passed_exams = len([r for r in results if r['percentage'] >= 60])
        st.metric("Exams Passed", passed_exams)
    
    # Display results table
    st.subheader("📋 All Exam Results")
    st.dataframe(df, use_container_width=True)
    
    # Download option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="exam_results.csv",
        mime="text/csv"
    )

def show_about():
    st.title("ℹ️ About Online Examination System")
    st.markdown("---")
    
    st.write("""
    ## 🎓 Online Examination System
    
    A complete web-based examination system built with **Streamlit** and **SQLite**.
    
    ### Features:
    - ✅ **Student Registration** with name and ID
    - 📝 **20 Multiple Choice Questions** with 4 options
    - 🔄 **Question Navigation** (Previous/Next)
    - 🎯 **Instant Results** with detailed feedback
    - 📊 **Results History** with statistics
    - 💾 **SQLite Database** for data storage
    - 📱 **Responsive Design** works on all devices
    
    ### Technology Stack:
    - **Frontend & Backend**: Streamlit (Python)
    - **Database**: SQLite
    - **Data Handling**: Pandas
    
    ### How to Use:
    1. Go to **"Take Exam"** section
    2. Enter your name and student ID
    3. Click **"Start Exam"** button
    4. Answer all 20 questions
    5. Submit your exam
    6. View instant results and detailed feedback
    7. Check **"View Results"** for history
    
    ---
    *Built with ❤️ using Python and Streamlit*
    """)

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