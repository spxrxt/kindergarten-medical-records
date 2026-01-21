# Модуль с функциями сортировки выбором


from typing import List, Callable
from child_record import ChildRecord, GroupType


def selection_sort(arr: List[ChildRecord], key_func: Callable) -> List[ChildRecord]:

    sorted_list = arr.copy()
    n = len(sorted_list)

    for i in range(n):
        # Находим индекс минимального элемента в оставшейся части
        min_idx = i
        for j in range(i + 1, n):
            if key_func(sorted_list[j]) < key_func(sorted_list[min_idx]):
                min_idx = j

        # Меняем местами найденный минимальный элемент с текущим
        sorted_list[i], sorted_list[min_idx] = sorted_list[min_idx], sorted_list[i]

    return sorted_list


def sort_by_health_and_lastname(children: List[ChildRecord]) -> List[ChildRecord]:


    def key_func(child: ChildRecord) -> tuple:
        # Сортировка по убыванию количества здоровых заключений
        # Для этого используем отрицательное значение
        return (-child.health.count_healthy(), child.last_name.lower())

    return selection_sort(children, key_func)


def sort_by_birth_date(children: List[ChildRecord]) -> List[ChildRecord]:


    def key_func(child: ChildRecord) -> tuple:
        return (child.birth_date.year, child.birth_date.month, child.birth_date.day)

    return selection_sort(children, key_func)


def sort_by_group_and_lastname(children: List[ChildRecord]) -> List[ChildRecord]:

    def key_func(child: ChildRecord) -> tuple:
        # Порядок сортировки групп
        group_order = {
            GroupType.JUNIOR: 1,
            GroupType.MIDDLE: 2,
            GroupType.SENIOR: 3
        }
        return (group_order[child.group], child.last_name.lower())

    return selection_sort(children, key_func)