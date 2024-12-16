from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Avg, Max
from .models import QuizAttempt, QuizDetail
from .models import HurdlesRunScore
from .models import HurdlesRunScore
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.utils import timezone
from datetime import timedelta

# View to render the home page
@csrf_protect
def index(request):
    return render(request, 'index.html')

# Static views
@csrf_protect
def about(request):
    return render(request, 'about.html')

@csrf_protect
def winnersCountries(request):
    return render(request, 'medalsTable.html')

@csrf_protect
def medalWinners(request):
    return render(request, 'medalist.html')

@csrf_protect
def highlights(request):
    return render(request, 'highlights.html')

@csrf_protect
def games(request):
    return render(request, 'games.html')

@csrf_protect
def players(request):
    return render(request, 'players.html')

@csrf_protect
def opening(request):
    return render(request, 'opening.html')

@csrf_protect
def closing(request):
    return render(request, 'closing.html')

@csrf_protect
def torch(request):
    return render(request, 'torch_relay.html')

@csrf_protect
def gamesD(request):
    return render(request, 'games_details.html')

# User Login View
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')  # Redirect to the dashboard or a relevant page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')  # Render your custom login template

# User Signup View
@csrf_protect
def signup_view(request):
    logout(request)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords don't match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, "Signup successful! Welcome.")
            return redirect('login')  # Redirect to login after successful signup
        except Exception as e:
            messages.error(request, f"Signup failed: {e}")

    return render(request, 'signup.html')  # Render your custom signup template

# Dashboard Profile View

@login_required
def dashboard_profile(request):
    user = request.user

    # Quiz statistics
    attempts = QuizAttempt.objects.filter(user=user)
    total_quizzes = attempts.count()
    average_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    best_score = attempts.aggregate(Max('score'))['score__max'] or 0
    recent_quizzes = attempts.order_by('-date_attempted')[:5]

    # Hurdle Run statistics
    hurdle_attempts = HurdlesRunScore.objects.filter(user=user)
    high_score = 0
    all_scores = []
    all_score_objects = []  # Store actual score objects

    for attempt in hurdle_attempts:
        all_scores.append(attempt.score)
        all_score_objects.append(attempt)  # Add the attempt object
        if attempt.score > high_score:
            high_score = attempt.score

    attempt_count = len(all_scores)

    # Prepare context for the template
    context = {
        'user': user,
        'total_quizzes': total_quizzes,
        'average_score': average_score,
        'best_score': best_score,
        'recent_quizzes': recent_quizzes,
        'high_score': high_score,
        'attempt_count': attempt_count,
        'all_scores': all_scores,
        'all_score_objects': all_score_objects,  # Pass the score objects
    }

    return render(request, 'quiz_dashboard.html', context)

@login_required
def delete_hurdle_score(request, score_id):
    if request.method == 'POST':
        score = get_object_or_404(HurdlesRunScore, id=score_id, user=request.user)
        score.delete()
        return redirect('dashboard')

def clear_scores(request):
    if request.method == "POST":
        HurdlesRunScore.objects.filter(user=request.user).delete()  # Deletes all scores for the logged-in user
        return redirect('dashboard')  # Redirect to the dashboard or any other page

# User Logout View
@csrf_protect
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to your custom login page after logout

# Quiz Results View
@login_required
@csrf_protect
def quiz_results_view(request, quiz_attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id)
    details = attempt.details.all()
    score = sum(1 for detail in details if detail.user_answer == detail.correct_answer)

    context = {
        'score': score,
        'correct_answers': details,
    }
    return render(request, 'quiz_results.html', context)

# View Past Quizzes
@login_required
@csrf_protect
def view_past_quizzes(request):
    attempts = QuizAttempt.objects.filter(user=request.user)
    quizzes_data = [
        {
            'attempt_id': attempt.id,
            'score': attempt.score,
            'details': list(attempt.details.values()),
        }
        for attempt in attempts
    ]

    return render(request, 'view_past_quizzes.html', {'quizzes': quizzes_data})

# Take Quiz View
@login_required
@csrf_protect
def take_quiz_view(request):
    if request.method == 'POST':
        user = request.user
        score = int(request.POST.get('score', 0))
        total_questions = int(request.POST.get('total_questions', 0))
        facts = request.POST.get('facts')
        user_answers_raw = request.POST.get('user_answers')
        correct_answers_raw = request.POST.get('correct_answers')
        questions_raw = request.POST.get('questions')

        if not (user_answers_raw and correct_answers_raw and questions_raw):
            messages.error(request, "Missing quiz submission data.")
            return redirect('take_quiz')

        user_answers = json.loads(user_answers_raw)
        correct_answers = json.loads(correct_answers_raw)
        questions = json.loads(questions_raw)
        facts_list = json.loads(facts)

        attempt = QuizAttempt.objects.create(
            user=user,
            score=score,
            total_questions=total_questions,
        )

        for i in range(len(user_answers)):
            QuizDetail.objects.create(
                quiz_attempt=attempt,
                question=questions[i],
                user_answer=user_answers[i],
                correct_answer=correct_answers[i],
                fact=facts_list[i],
            )

        return redirect('quiz_results', quiz_attempt_id=attempt.id)

    return render(request, 'take_quiz.html')

# Game View
@login_required
@csrf_protect
def game_view(request):
    return render(request, 'olympic_game.html')

@login_required
@csrf_exempt
def save_score(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        score = data.get("score")

        # Check if a score entry exists within the last 5 seconds to prevent duplicates
        recent_score = HurdlesRunScore.objects.filter(
            user=user,
            date_attempted__gte=timezone.now() - timedelta(seconds=5)
        ).exists()

        if not recent_score:
            HurdlesRunScore.objects.create(user=user, score=score)
            return JsonResponse({"status": "Score saved"})
        else:
            return JsonResponse({"status": "Duplicate score detected, not saved"}, status=400)