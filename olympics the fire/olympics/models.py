from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Model for quiz questions
class QuizQuestion(models.Model):
    text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.text

# Model for quiz attempts
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    date_attempted = models.DateTimeField(auto_now_add=True)


class QuizDetail(models.Model):
    quiz_attempt = models.ForeignKey('QuizAttempt', on_delete=models.CASCADE, related_name='details')
    question = models.CharField(max_length=300, default="Question not available")  # Or a ForeignKey to your questions model
    user_answer = models.CharField(max_length=255)  # Store the user's selected answer
    correct_answer = models.CharField(max_length=255)  # Store the correct answer
    fact = models.TextField()  # Store the fact related to the question

    def __str__(self):
        return f"QuizDetail for Attempt: {self.quiz_attempt.id}"

class HurdlesRunScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_attempted = models.DateTimeField(auto_now_add=True)