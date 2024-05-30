from enum import Enum


class LessonEnum(str, Enum):
    PRACTICE = 'семинар'
    LECTURE = 'лекции'
    LABORATORY = 'лабораторные занятия'


class SubgroupEnum(str, Enum):
    A = 'А'
    B = 'Б'


class RolesEnum(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
