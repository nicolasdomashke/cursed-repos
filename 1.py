from datetime import datetime, timedelta
from openpyxl import Workbook


class Driver:
    count = 0
    def __init__(self, type, start_time):
        self.type = type
        self.start_time = start_time
        self.index = Driver.count
        self.actions = {}
        Driver.count += 1

def is_peak_time(time):
    return (datetime.strptime("07:00", "%H:%M").time() <= time.time() < datetime.strptime("09:00", "%H:%M").time()) or (datetime
            .strptime("17:00", "%H:%M").time() <= time.time() < datetime.strptime("19:00", "%H:%M").time())

def basic_method(drivers_list, shift_start_times):
    for index, driver in enumerate(drivers_list):
        shift_start = datetime.strptime(shift_start_times[index], '%H:%M')
        current_time = shift_start
        work_time = 0

        driver.actions = {}
        if driver.type == "A":
            break_schedule = [4]
        else:
            break_schedule = [3, 6]

        driver.actions[current_time.strftime('%H:%M')] = 'Начало смены'
        current_time += timedelta(hours=1)
        work_time += 1

        while work_time < 8:
            if break_schedule and work_time == break_schedule[0]:
                if is_peak_time(current_time):
                    driver.actions[current_time.strftime('%H:%M')] = 'Перерыв сдвинут'
                    current_time += timedelta(hours=1)
                    break_schedule[0] += 1
                    continue
                if driver.type == 'A':
                    driver.actions[current_time.strftime('%H:%M')] = 'Перерыв 1 час'
                    current_time += timedelta(hours=1)
                elif driver.type == 'B':
                    driver.actions[current_time.strftime('%H:%M')] = 'Перерыв 15 минут'
                    current_time += timedelta(minutes=15)
                break_schedule.pop(0)
            else:
                driver.actions[current_time.strftime('%H:%M')] = 'Выезд'
                current_time += timedelta(hours=1)
                work_time += 1


        driver.actions[current_time.strftime('%H:%M')] = 'Конец смены'

        drivers_list[index] = driver

    return drivers_list

shift_start_times = [
    "06:00",
    "07:00",
    "07:00",
    "08:00",
    "10:00",
    "12:00",
    "15:00",
    "17:00",
    "18:00"
]

drivers_list = [Driver("B" if i < 5 else "A", shift_start_times[i]) for i in range(8)]


drivers_list = basic_method(drivers_list, shift_start_times)

times = set()
for d in drivers_list:
    for t in list(d.actions.keys()):
        times.add(t)

times = sorted(list(times), key=lambda x: datetime.strptime(x, '%H:%M'))

wb = Workbook()
ws = wb.active

first_line = [""]
for t in times:
    first_line.append(t)
ws.append(first_line)
for i, d in enumerate(drivers_list):
    data = [f"Водитель №{i + 1}"]
    for t in times:
        if t in list(d.actions.keys()):
            data.append(d.actions[t])
        else:
            data.append("-")
    ws.append(data)

wb.save("schedule.xlsx")
