# internet-protocols
## Task3 (8): vkApi

### Описание:
Работа vkApi с помощью библиотеку requests. 
Вывод в удобочитаемом виде информации о пользователе по его id в vk:
списки друзей, подписчиков, подписок и групп

### Preparation:
В файле config.ini в переменной access_token ввести токен от своего vk приложения

### Usage:
```
main.py [-h] [-i USERID] [-f] [-l] [-s] [-g]
```

### Optional arguments:
```
  -h, --help            show this help message and exit
  -i USERID, --userId USERID
                        target user id
  -f, --friends         friends print
  -l, --followers       followers print
  -s, --subscriptions   subscriptions print
  -g, --groups          groups print
```

### Демонстрация программы:
![](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzhmMjk0M2E1MWIzMmY0YzVmM2M5YmM2NzNjMDA1NmZmNGVkYmMwYiZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/ha6Eke1yUxzcIaERhI/giphy.gif)
