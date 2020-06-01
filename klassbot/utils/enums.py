from enum import Enum, unique


@unique
class CallbackType(Enum):
    """Enum for creating patterns.

    Arguments:
        Enum {int} -- Code for callback query data
    """ """"""

    # Klass settings
    klass_create = 1
    klass_delete = 2
    klass_update = 3
    klass_settings = 4
    # Assign
    assign_create = 10
    assign_delete = 11
    assign_update = 12
    assign_list = 13
    assign_finish = 14
    # Grade
    grade_create = 20
    grade_delete = 21
    grade_update = 23
    # Admin
    admin_add = 30
    admin_delete = 31
    # Student
    student_add = 40
    student_delete = 41
    # Teacher
    teacher_add = 50
    teacher_delete = 51
    # Menu
    menu_next = 61
    menu_prev = 62
