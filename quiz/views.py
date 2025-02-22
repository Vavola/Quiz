from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Quiz, Question, Answer, Result
from .forms import QuizForm, QuestionForm
import json

class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'quizzes'

class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'

@login_required
def play_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    # Перетворюємо QuerySet у список словників
    questions_data = json.dumps([
        {
            'id': q.id,
            'text': q.text,
            'photo': q.photo.url if q.photo else None,
            'answers': [{'text': a.text} for a in q.answers.all()]
        }
        for q in questions
    ])

    return render(request, 'quiz/play_quiz.html', {
        'quiz': quiz,
        'questions': questions_data,  # JSON-готовий рядок
        'total_time': quiz.total_time
    })
@login_required
def submit_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        import json
        user_answers = json.loads(request.POST.get('user_answers', '{}'))
        score = 0
        for question in quiz.questions.all():
            correct = question.answers.filter(is_correct=True).first()
            if correct and user_answers.get(str(question.id)) == correct.text:
                score += 1
        Result.objects.create(user=request.user, quiz=quiz, score=score)
        return render(request, 'quiz/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': quiz.questions.count()
        })
    return redirect('play_quiz', pk=pk)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionFormSet, AnswerFormSet
from .models import Quiz, Question

@login_required
def create_quiz(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        quiz_form = QuizForm(request.POST, request.FILES)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            # Отримуємо кількість питань із форми
            try:
                question_count = int(quiz_form.cleaned_data.get('question_count', 0))
            except (TypeError, ValueError):
                question_count = 0
            # Для кожного питання обробляємо дані
            for i in range(1, question_count + 1):
                q_text = request.POST.get(f'question_{i}_text')
                q_time = request.POST.get(f'question_{i}_time_limit')
                # Файли завантажуються у request.FILES
                q_photo = request.FILES.get(f'question_{i}_photo')
                if not q_text or not q_time:
                    continue  # Пропускаємо, якщо основні дані відсутні
                try:
                    q_time = int(q_time)
                except ValueError:
                    q_time = 30  # значення за замовчуванням
                # Створюємо питання
                question = Question.objects.create(
                    quiz=quiz,
                    text=q_text,
                    time_limit=q_time,
                    order=i,
                    photo=q_photo  # Якщо q_photo є None, це нормально
                )
                # Для відповіді: шукаємо варіанти з номерами від 1 до 6
                for j in range(1, 7):
                    answer_text = request.POST.get(f'question_{i}_answer_{j}')
                    if answer_text:
                        # Якщо прапорець встановлено, request.POST поверне "on"
                        is_correct = request.POST.get(f'question_{i}_answer_{j}_is_correct') == "on"
                        Answer.objects.create(
                            question=question,
                            text=answer_text,
                            is_correct=is_correct,
                            # Для фото варіанту відповіді (якщо потрібно):
                            photo=request.FILES.get(f'question_{i}_answer_{j}_photo')
                        )
            print("Quiz saved, id =", quiz.pk)
            return redirect('quiz_detail', pk=quiz.pk)
        else:
            print("QuizForm errors:", quiz_form.errors)
    else:
        quiz_form = QuizForm()
    return render(request, 'quiz/quiz_form.html', {'quiz_form': quiz_form})