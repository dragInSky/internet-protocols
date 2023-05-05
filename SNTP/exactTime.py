from subprocess import check_output
from datetime import datetime
import configparser


def get_delay():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return int(config['time']['delay'])


def get_exact_time():
    date = check_output(["date", "+%Y-%m-%d-%H-%M-%S"]).split(b"-")
    dt = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))

    # Время в секундах от 1970-01-01 00:00:00 (UTC)
    timestamp = dt.timestamp()

    # Прибавляем секунды, указанные в конфиге
    timestamp += get_delay()

    # Смотрим погрешность во времени, сравнивая с надежным сервером точного времени
    offset = check_output(["sntp", "time.apple.com"]).split(b" ")
    to_add = float(offset[0][1:])
    max_error = offset[1] + b" " + offset[2]

    # Добавляем миллисекунды
    timestamp = float(timestamp * 1000 + to_add * 1000) / 1000

    # Конвертируем время в секундах в привычный вид
    time_with_add = datetime.fromtimestamp(timestamp).strftime("DATE: %Y-%m-%d%nTIME: %H:%M:%S:%f").encode("utf-8")

    return time_with_add + b" " + max_error
