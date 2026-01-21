# Основной модуль программы "Учёт результатов диспансеризации"


import sys
from typing import List
from child_record import ChildRecord, GroupType
from file_operations import read_database, save_report
from reports import (
    generate_full_report,
    generate_group_report,
    generate_treatment_report
)


def display_menu() -> None:
    #Отображение главного меню
    print("УЧЕТ РЕЗУЛЬТАТОВ ДИСПАНСЕРИЗАЦИИ")
    print("1. Показать полный список всех детей")
    print("2. Показать список детей по группам")
    print("3. Показать список детей, нуждающихся в лечении")
    print("4. Сохранить отчет в файл")
    print("5. Выход")


def display_group_menu() -> None:
    # Отображение меню выбора группы
    print("\nВыберите группу:")
    print("1. Младшая группа")
    print("2. Средняя группа")
    print("3. Старшая группа")
    print("4. Назад в главное меню")


def get_user_choice(min_val: int, max_val: int, prompt: str = "Выберите пункт: ") -> int:

    while True:
        try:
            choice = input(prompt)
            if not choice.isdigit():
                print("Пожалуйста, введите число.")
                continue

            choice_num = int(choice)
            if min_val <= choice_num <= max_val:
                return choice_num
            else:
                print(f"Пожалуйста, введите число от {min_val} до {max_val}.")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем.")
            sys.exit(0)
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def display_report(report_lines: List[str]) -> None:
    # Отображение отчета на экране
    print("\n" + "\n".join(report_lines))


def main() -> None:
    # Основная функция программы
    database_filename = "kindergarten_database.txt"

    try:
        print("Загрузка базы данных...")
        children = read_database(database_filename)
        print(f"База данных успешно загружена. Записей: {len(children)}")

        # Переменные для хранения текущего отчета
        current_report = None
        current_report_name = None

        while True:
            display_menu()
            choice = get_user_choice(1, 5)

            if choice == 1:
                # Полный список всех детей
                current_report = generate_full_report(children)
                current_report_name = "Полный список всех детей"
                display_report(current_report)

            elif choice == 2:
                # Список детей по группам
                while True:
                    display_group_menu()
                    group_choice = get_user_choice(1, 4)

                    if group_choice == 1:
                        group_type = GroupType.JUNIOR
                    elif group_choice == 2:
                        group_type = GroupType.MIDDLE
                    elif group_choice == 3:
                        group_type = GroupType.SENIOR
                    else:
                        break

                    current_report = generate_group_report(children, group_type)
                    current_report_name = f"Список детей {group_type.value} группы"
                    display_report(current_report)

            elif choice == 3:
                # Список детей, нуждающихся в лечении
                current_report = generate_treatment_report(children)
                current_report_name = "Список детей, нуждающихся в лечении"
                display_report(current_report)

            elif choice == 4:
                # Сохранение отчета в файл
                if current_report is None:
                    print("Сначала сгенерируйте отчет!")
                else:
                    filename = input("Введите имя файла для сохранения (по умолчанию: report.txt): ")
                    if not filename:
                        filename = "report.txt"
                    save_report(filename, current_report)

            elif choice == 5:
                # Выход
                print("Спасибо за использование программы. До свидания!")
                break

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        print("Пожалуйста, создайте файл 'kindergarten_database.txt' с данными.")
    except ValueError as e:
        print(f"Ошибка в данных: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()