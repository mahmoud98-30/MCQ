import django_filters

from paper.models import Student, Teacher


class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter()
    class_room = django_filters.CharFilter()
    teacher_name = django_filters.CharFilter(lookup_expr='subject')

    class Meta:
        model = Student
        fields = ['name', 'class_room', 'teacher_name', ]


