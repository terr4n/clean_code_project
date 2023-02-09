from dataclasses import dataclass, field


@dataclass
class Patient:
    id: int
    status: int
    str_status: str = field(init=False)

    def __post_init__(self):
        self.str_status = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}.get(self.status)


def get_number_of_elements(list_patients, value):
    count = 0
    for element in list_patients:
        if element == value:
            count += 1
    return count


class Hospital:

    def __init__(self, db_patients):
        self.Patients = db_patients

    def check_id(self, id_patient):
        try:
            id_patient = int(id_patient)
            if id_patient == 0 or id_patient < 0:
                raise ValueError
            else:
                result_id = self.Patients[id_patient - 1]
        except IndexError:
            print('Ошибка. В больнице нет пациента с таким ID')
        except ValueError:
            print('Ошибка. ID пациента должно быть числом (целым, положительным)')
        else:
            if result_id == 0 or result_id > 0:
                return True

    def get_id(self, id_patient):
        if self.check_id(id_patient):
            return int(id_patient)

    def get_status(self, id_patient):
        if self.check_id(id_patient):
            patient = Patient(self.get_id(id_patient), self.Patients[self.get_id(id_patient) - 1])
            return patient.str_status

    def status_up(self, id_patient):
        if self.check_id(id_patient):
            self.Patients[self.get_id(id_patient) - 1] += 1
            patient = Patient(self.get_id(id_patient), self.Patients[self.get_id(id_patient) - 1])
            return patient.str_status

    def status_down(self, id_patient):
        if self.check_id(id_patient):
            self.Patients[self.get_id(id_patient) - 1] -= 1
            patient = Patient(self.get_id(id_patient), self.Patients[self.get_id(id_patient) - 1])
            return patient.str_status

    def discharge(self, id_patient):
        if self.check_id(id_patient):
            patient = Patient(self.get_id(id_patient), self.Patients[self.get_id(id_patient) - 1])
            self.Patients.pop(patient.id - 1)
            return True

    def calculate_statistics(self):
        all_patients = len(self.Patients)
        status_0 = get_number_of_elements(self.Patients, 0)
        status_1 = get_number_of_elements(self.Patients, 1)
        status_2 = get_number_of_elements(self.Patients, 2)
        status_3 = get_number_of_elements(self.Patients, 3)
        return all_patients, status_0, status_1, status_2, status_3


if __name__ == '__main__':
    #  Подготовка входных данных
    patients = [1 for i in range(0, 200)]

    #  Запуск программы
    hospital_test = Hospital(patients)

    while True:
        command = input("Введите команду: ").lower()

        if command == "узнать статус пациента" or command == "get status":
            patient_id = input("Введите ID пациента: ")
            if hospital_test.check_id(patient_id):
                result = hospital_test.get_status(patient_id)
                if result:
                    print(f'Статус пациента: "{result}"')

        elif command == "повысить статус пациента" or command == "status up":
            patient_id = input("Введите ID пациента: ")
            if hospital_test.check_id(patient_id):
                if hospital_test.get_status(patient_id) == 'Готов к выписке':
                    command = input('Желаете этого клиента выписать? (да/нет): ')
                    if command == 'да':
                        hospital_test.discharge(patient_id)
                        print('Пациент выписан из больницы')
                        continue
                    else:
                        print('Пациент остался в статусе "Готов к выписке"')
                        continue
                result = hospital_test.status_up(patient_id)
                if result:
                    print(f'Новый статус пациента: "{result}"')

        elif command == "понизить статус пациента" or command == "status down":
            patient_id = input("Введите ID пациента: ")
            if hospital_test.check_id(patient_id):
                if hospital_test.get_status(patient_id) == "Тяжело болен":
                    print('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')
                    continue
                result = hospital_test.status_down(patient_id)
                if result:
                    print(f'Новый статус пациента: "{result}"')

        elif command == "выписать пациента" or command == "discharge":
            patient_id = input("Введите ID пациента: ")
            if hospital_test.check_id(patient_id):
                result = hospital_test.discharge(patient_id)
                if result:
                    print('Пациент выписан из больницы')

        elif command == "рассчитать статистику" or command == "calculate statistics":
            result = hospital_test.calculate_statistics()
            if result:
                result_data = f'В больнице на данный момент находится {result[0]} чел., из них:'
                if result[1] != 0:
                    result_data += f'\n    - в статусе "Тяжело болен": {result[1]} чел.'
                if result[2] != 0:
                    result_data += f'\n    - в статусе "Болен": {result[2]} чел.'
                if result[3] != 0:
                    result_data += f'\n    - в статусе "Слегка болен": {result[3]} чел.'
                if result[4] != 0:
                    result_data += f'\n    - в статусе "Готов к выписке": {result[4]} чел.'
                print(result_data)
        elif command == "стоп" or command == "stop":
            print('Сеанс завершён.')
            break

        else:
            print('Неизвестная команда! Попробуйте ещё раз')






