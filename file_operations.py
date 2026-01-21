# Модуль для операций с файлами: чтение и запись данных


import os
from datetime import date
from typing import List
from child_record import ChildRecord, GroupType, HealthConclusion


def read_database(filename: str) -> List[ChildRecord]:

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл '{filename}' не найден")

    children = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
                # Разделяем строку по запятым
                parts = [part.strip() for part in line.split(',')]

                # Ожидаем 8 полей: Фамилия, Имя, Дата, Группа, и 4 заключения врачей
                if len(parts) != 8:
                    raise ValueError(
                        f"Неверное количество полей в строке {i}: {len(parts)} вместо 8. "
                        f"Формат: Фамилия, Имя, Дата(ГГГГ.ММ.ДД), Группа, Невропатолог, "
                        f"Отоларинголог, Ортопед, Окулист"
                    )

                last_name = parts[0]
                first_name = parts[1]

                # Парсинг даты (формат: ГГГГ.ММ.ДД)
                date_str = parts[2]
                if '.' in date_str:
                    date_parts = date_str.split('.')
                else:
                    date_parts = date_str.split('.')

                if len(date_parts) != 3:
                    raise ValueError(f"Неверный формат даты в строке {i}: {date_str}")

                year, month, day = map(int, date_parts)
                birth_date_obj = date(year, month, day)
                group_str = parts[3].lower()
                if "младш" in group_str:
                    group = GroupType.JUNIOR
                elif "средн" in group_str:
                    group = GroupType.MIDDLE
                elif "старш" in group_str:
                    group = GroupType.SENIOR
                else:
                    raise ValueError(f"Неверное название группы в строке {i}: {group_str}")

                # Создание объекта HealthConclusion (4 заключения врачей)
                health = HealthConclusion.from_strings(
                    parts[4], parts[5], parts[6], parts[7]
                )

                child = ChildRecord(
                    last_name=last_name,
                    first_name=first_name,
                    birth_date=birth_date_obj,
                    group=group,
                    health=health
                )
                children.append(child)

            except (ValueError, IndexError) as e:
                print(f"Ошибка в строке {i}: {e}")
                continue
            except Exception as e:
                print(f"Неожиданная ошибка в строке {i}: {e}")
                continue

    except Exception as e:
        raise ValueError(f"Ошибка чтения файла: {e}")

    if not children:
        raise ValueError("Файл не содержит корректных записей")

    print(f"Успешно загружено {len(children)} записей")
    return children


def save_report(filename: str, report_lines: List[str]) -> None:

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('\n'.join(report_lines))
        print(f"Отчет сохранен в файл: {filename}")
    except Exception as e:
        print(f"Ошибка сохранения отчета: {e}")