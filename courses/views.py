from django.shortcuts import render, get_object_or_404, redirect
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

    total_score = 0
    possible_score = course.question_set.count()

    for question in course.question_set.all():
        if question.is_get_score(selected_ids):
            total_score += 1

    return render(request, 'exam_result_bootstrap.html', {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': possible_score
    })