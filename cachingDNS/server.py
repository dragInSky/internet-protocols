import socket
import pickle
import time

from dnslib import DNSRecord, RCODE

# Задаем адрес и порт для прослушивания
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 53
BUF_LEN = 1024


def pretty_parse(record, q_type):
    questions = record.questions
    res = ''
    if questions:
        qname = questions[0].qname
        answers = record.rr
        if answers:
            for answer in answers:
                if q_type == 'A':
                    res += f'Доменное имя: {qname}\nIP-адрес: {answer.rdata}\n'
                else:
                    res += f'Доменное имя: {answer.rdata}\nIP-адрес: {qname}\n'

    return res.encode('utf-8')


def resolve_query(data, cache):
    """
    Разрешает доменное имя или IP-адрес в IP-адрес или доменное имя соответственно.
    """
    try:
        # декодируем DNS пакет
        query = DNSRecord.parse(data)

        if cache.get((query.q.qtype, query.q.qname)):
            print(f'Найдена запись в кэше: {data}')

            record, ttl = cache.get((query.q.qtype, query.q.qname))
            return pretty_parse(record, 'A') if query.q.qtype == 1 else pretty_parse(record, 'PTR')

        print('Ожидание запроса')

        # 77.88.8.1 - secondary.dns.yandex.ru.
        response = query.send('77.88.8.1', 53, timeout=5)
        record = DNSRecord.parse(response)

        if record.header.rcode == RCODE.NOERROR:
            print(f'Данные в кэше отсутствуют и будут записаны: {data}')
            for rr in record.rr:  # проходимся по записям resource record
                cache[(rr.rtype, rr.rname)] = (record, time.time() + rr.ttl)
            return pretty_parse(record, 'PTR') if query.q.qtype == 12 else pretty_parse(record, 'A')

        return None

    except Exception as e:
        print(f'Не удалось разрешить запрос {data}\nОшибка: {e}')
        return None


def server_cycle(cache):
    # Основной цикл сервера
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_ADDRESS, SERVER_PORT))
        # устанавливаем таймаут на получение запроса
        s.settimeout(5)
        print(f'Сервер запущен на: {SERVER_ADDRESS}:{SERVER_PORT}')
        while True:
            try:
                # Получаем запрос от клиента
                data, address = s.recvfrom(BUF_LEN)
                print(f'Получен запрос от: {address}')

                # разрешаем запрос
                response = resolve_query(data, cache)
                if response is not None:
                    # Отправляем ответ клиенту
                    s.sendto(response, address)

                # Проверяем кэш на просроченные записи и удаляем их
                for key in list(cache.keys()):
                    if cache.get(key)[1] < time.time():
                        del cache[key]
                        print(f'Удалена просроченная запись: {key}')

                save(cache)

            except socket.timeout:
                pass
            except socket.error as e:
                # Обработка ошибки сети при сохранении кэша
                print(f'Ошибка при сохранении кэша: {e}')
            except KeyboardInterrupt:
                s.close()
                save(cache)
                print('Закрытие сервера. Кэш сохранен')
                break


def save(cache):
    with open('cache.txt', 'wb') as f:
        pickle.dump(cache, f)


def load():
    # Загружаем данные из файла, если он существует
    try:
        with open('cache.txt', 'rb') as f:
            cache = {}
            data = pickle.load(f)
            for key in list(data.keys()):
                if data.get(key)[1] > time.time():
                    cache[key] = data[key]
            return cache
    except FileNotFoundError:
        return {}


def main():
    cache = load()

    server_cycle(cache)


if __name__ == '__main__':
    main()
