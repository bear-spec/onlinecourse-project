from django.shortcuts import render, get_object_or_404
from .models import Course

def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_details_bootstrap.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    selected_choices = request.POST
    score = 0
    total = course.question_set.count()

    for question in course.question_set.all():
        correct_choices = question.choice_set.filter(is_correct=True)
        selected = request.POST.getlist(str(question.id))
        correct_ids = [str(c.id) for c in correct_choices]

        if set(selected) == set(correct_ids):
            score += 1

    return show_exam_result(request, score, total)


def show_exam_result(request, score, total):
    return render(request, 'result.html', {
        'score': score,
        'total': total,
        'message': "🎉 Congratulations! You completed the exam!"
    })