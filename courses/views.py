from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Course, Submission, Choice

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_details_bootstrap.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    submission = Submission.objects.create(user=request.user)

    for key in request.POST:
        if key.startswith('choice'):
            choice = Choice.objects.get(id=int(request.POST[key]))
            submission.choices.add(choice)

    return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    selected_ids = [choice.id for choice in submission.choices.all()]

    total = 0
    correct = 0

    for question in course.question_set.all():
        correct_choices = question.choice_set.filter(is_correct=True)
        total += len(correct_choices)

        for choice in correct_choices:
            if choice.id in selected_ids:
                correct += 1

    return render(request, 'exam_result_bootstrap.html', {
        'course': course,
        'selected_ids': selected_ids,
        'grade': correct,
        'possible': total
    })