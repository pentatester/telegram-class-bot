from enum import Enum, unique


@unique
class CallbackType(Enum):
    """Enum for creating patterns.

    Arguments:
        Enum {int} -- Code for callback query data
    """ """"""

    SEPARATOR = "|"

    # Klass settings
    klass_create = 1
    klass_delete = 2
    klass_update = 3
    klass_settings = 4
    klass_list = 5
    klass_detail = 9
    # Assign
    assign_create = 10
    assign_delete = 11
    assign_update = 12
    assign_finish = 14
    assign_list = 15
    # Grade
    grade_create = 20
    grade_delete = 21
    grade_update = 23
    grade_list = 25
    # Admin
    admin_add = 30
    admin_delete = 31
    admin_list = 35
    # Student
    student_add = 40
    student_delete = 41
    student_quit = 43
    student_list = 45
    # Teacher
    teacher_add = 50
    teacher_delete = 51
    teacher_list = 55
    # Menu
    menu_next = 61
    menu_prev = 62


@unique
class CallbackAction(Enum):
    none = 0
    accept = 1
    cancel = 2
    close = 3
    page = 4
    page_prev = 5
    page_next = 6
