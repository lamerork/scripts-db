from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation
from environs import Env
import random
import sys

def find_schoolkid(schoolkid):

    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        return student
    except Schoolkid.DoesNotExist:
        sys.exit('Ученик не найден! Уточните ФИО ученика.')
    except Schoolkid.MultipleObjectsReturned:
        sys.exit('Слишком много совпадений! Уточните ФИО ученика.')


def fix_marks(schoolkid):

    student = find_schoolkid(schoolkid)
    Mark.objects.filter(schoolkid=student, points__in=[2 ,3]).update(points=5)
    print('Плохие оценки исправлены.')
 

def remove_chastisements(schoolkid):

    student = find_schoolkid(schoolkid)
    Chastisement.objects.filter(schoolkid=student).delete()
    print('Все замечания удалены.')


def create_commendation(schoolkid, subject):

    env = Env()
    env.read_env()
    commedation = random.choice(env.list('COMMENDATIONS'))
    student = find_schoolkid(schoolkid)

    try:
        subject = Subject.objects.filter(title=subject, year_of_study=student.year_of_study).get()
    except Schoolkid.DoesNotExist:
        sys.exit('Предмет не найден! Введите коректный предмет.')

    lesson = Lesson.objects.filter(year_of_study=student.year_of_study, group_letter=student.group_letter, subject=subject).order_by('date').last()

    Commendation.objects.create(text=commedation, created=lesson.date, schoolkid=student,subject=subject, teacher=lesson.teacher)
    print('Похвала добавлена.')
