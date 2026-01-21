# Модуль для генерации различных отчетов


from datetime import date
from typing import List
from child_record import ChildRecord, GroupType
from sorting import (
    sort_by_health_and_lastname,
    sort_by_birth_date,
    sort_by_group_and_lastname
)


def generate_full_report(children: List[ChildRecord]) -> List[str]:

    sorted_children = sort_by_health_and_lastname(children)

    report = ["ПОЛНЫЙ СПИСОК ВСЕХ ДЕТЕЙ",
              "=" * 50,
              "Сортировка: по убыванию количества здоровых заключений, "
              "по возрастанию фамилии",
              ""]

    for i, child in enumerate(sorted_children, 1):
        health_status = "здоров" if not child.health.needs_treatment() else "нуждается в лечении"
        report.append(f"{i:2}. {child.last_name} {child.first_name}")
        report.append(f"    Дата рождения: {child.birth_date.strftime('%d.%m.%Y')}")
        report.append(f"    Группа: {child.group.value}")
        report.append(f"    Здоровых заключений: {child.health.count_healthy()}/4")
        report.append(f"    Общий статус: {health_status}")
        report.append(f"    Заключения: "
                      f"невропатолог - {'здоров' if child.health.neurologist else 'лечение'}, "
                      f"отоларинголог - {'здоров' if child.health.otolaryngologist else 'лечение'}, "
                      f"ортопед - {'здоров' if child.health.orthopedist else 'лечение'}, "
                      f"окулист - {'здоров' if child.health.ophthalmologist else 'лечение'}")
        report.append("")

    return report


def generate_group_report(children: List[ChildRecord], group_type: GroupType) -> List[str]:

    group_children = [child for child in children if child.group == group_type]

    if not group_children:
        return [f"В {group_type.value} группе нет детей"]

    # Сортировка по дате рождения
    sorted_children = sort_by_birth_date(group_children)

    report = [f"СПИСОК ДЕТЕЙ {group_type.value.upper()} ГРУППЫ",
              "=" * 50,
              "Сортировка: по дате рождения (год, месяц, день)",
              ""]

    for i, child in enumerate(sorted_children, 1):
        age = calculate_age(child.birth_date)
        report.append(f"{i:2}. {child.last_name} {child.first_name}")
        report.append(f"    Дата рождения: {child.birth_date.strftime('%d.%m.%Y')} "
                      f"(возраст: {age} лет)")
        report.append(f"    Здоровых заключений: {child.health.count_healthy()}/4")
        report.append("")

    report.append(f"Всего детей в группе: {len(sorted_children)}")

    return report


def generate_treatment_report(children: List[ChildRecord]) -> List[str]:

    # Фильтрация детей, нуждающихся в лечении
    treatment_children = [child for child in children if child.health.needs_treatment()]

    if not treatment_children:
        return ["Нет детей, нуждающихся в лечении"]

    # Сортировка по группе и фамилии
    sorted_children = sort_by_group_and_lastname(treatment_children)

    report = ["СПИСОК ДЕТЕЙ, НУЖДАЮЩИХСЯ В ЛЕЧЕНИИ",
              "=" * 50,
              "Сортировка: по группе, по возрастанию фамилии",
              ""]

    for i, child in enumerate(sorted_children, 1):
        unhealthy_specialists = []
        if not child.health.neurologist:
            unhealthy_specialists.append("невропатолог")
        if not child.health.otolaryngologist:
            unhealthy_specialists.append("отоларинголог")
        if not child.health.orthopedist:
            unhealthy_specialists.append("ортопед")
        if not child.health.ophthalmologist:
            unhealthy_specialists.append("окулист")

        report.append(f"{i:2}. {child.last_name} {child.first_name}")
        report.append(f"    Группа: {child.group.value}")
        report.append(f"    Требуется лечение у: {', '.join(unhealthy_specialists)}")
        report.append("")

    report.append(f"Всего нуждаются в лечении: {len(sorted_children)} детей")

    return report


def calculate_age(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year

    # Корректировка, если день рождения еще не наступил в этом году
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age