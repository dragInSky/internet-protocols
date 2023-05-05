# internet-protocols
## Task1.2: SNTP-server

### Описание:
Сервер точного времени (SNTP-server), сервер прослушивает 123 порт UDP и узнает время у надежного сервера точного времени - time.apple.com
После чего «врет» на заданное в своем конфиге (config.ini) число секунд

### Запуск:
1.  Запуск сервера
```
sudo python3 server.py
```
2.  Запуск клиента
```
sudo python3 client.py
```

### Демонстрация программы:

![](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzg3M2JlM2QxZWMwNTJiMjdlYjExNzRhMDdjOGQwNDY0MjZjYTkwZiZjdD1n/mC9FGg8zmNa4wNJSTu/giphy.gif)
