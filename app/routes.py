from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Quiz, Question, Result, Answer

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    elif current_user.is_teacher():
        return redirect(url_for('main.teacher_dashboard'))
    else:
        return redirect(url_for('main.student_dashboard'))


# ADMIN ROUTES
@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    total_users = User.query.count()
    total_teachers = User.query.filter_by(role='teacher').count()
    total_students = User.query.filter_by(role='student').count()
    total_quizzes = Quiz.query.count()
    
    return render_template('admin/dashboard.html',
                          total_users=total_users,
                          total_teachers=total_teachers,
                          total_students=total_students,
                          total_quizzes=total_quizzes)


@main_bp.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    users = User.query.filter(User.role != 'admin').all()
    return render_template('admin/users.html', users=users)


@main_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete admin users', 'danger')
        return redirect(url_for('main.admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted successfully', 'success')
    return redirect(url_for('main.admin_users'))


# TEACHER ROUTES
@main_bp.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if not current_user.is_teacher():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    return render_template('teacher/dashboard.html', quizzes=quizzes)


@main_bp.route('/teacher/create-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if not current_user.is_teacher():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        quiz = Quiz(
            title=request.form.get('title'),
            description=request.form.get('description'),
            teacher_id=current_user.id
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully', 'success')
        return redirect(url_for('main.teacher_dashboard'))
    
    return render_template('teacher/create_quiz.html')


@main_bp.route('/teacher/quiz/<int:quiz_id>')
@login_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id and not current_user.is_admin():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('teacher/edit_quiz.html', quiz=quiz)


# STUDENT ROUTES
@main_bp.route('/student/dashboard')
@login_required
def student_dashboard():
    if not current_user.is_student():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    available_quizzes = Quiz.query.filter_by(is_active=True).all()
    completed_quizzes = Result.query.filter_by(student_id=current_user.id).all()
    completed_quiz_ids = [r.quiz_id for r in completed_quizzes]
    
    return render_template('student/dashboard.html',
                          available_quizzes=available_quizzes,
                          completed_quiz_ids=completed_quiz_ids)


@main_bp.route('/student/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
@login_required
def attempt_quiz(quiz_id):
    if not current_user.is_student():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        # Process answers
        result = Result(
            student_id=current_user.id,
            quiz_id=quiz_id,
            total_questions=len(quiz.questions)
        )
        
        score = 0
        for question in quiz.questions:
            selected_answer = request.form.get(f'question_{question.id}')
            answer = Answer(
                question_id=question.id,
                selected_answer=selected_answer
            )
            result.answers.append(answer)
            
            if selected_answer and selected_answer.lower() == question.correct_answer.lower():
                score += 1
        
        result.score = score
        result.percentage = (score / len(quiz.questions) * 100) if quiz.questions else 0
        
        db.session.add(result)
        db.session.commit()
        
        return redirect(url_for('main.quiz_result', result_id=result.id))
    
    return render_template('student/attempt_quiz.html', quiz=quiz)


@main_bp.route('/student/result/<int:result_id>')
@login_required
def quiz_result(result_id):
    result = Result.query.get_or_404(result_id)
    
    if result.student_id != current_user.id and not current_user.is_admin():
        flash('Unauthorized access', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('student/result.html', result=result)
