# Блогикум - Личный блог

## Описание проекта:

**Блогикум** - это прототип блога

Функционал, реализованный в проекте:
- публикация, удаление и редактирование записей;
- выбор группы для поста;
- комментирование постов.

## Стек:

- Python 3.9;
- Django 3.2.16.

## Запуск проекта:

#### Развернуть виртуальное окружение:
- Linux/MacOS:
```Bash
python3 -m venv venv
```

- Windows:
```Bash
python -m venv venv
```

#### Активировать виртуальное окружение:
```Bash
source venv/bin/activate
```

#### Установить зависимости:
- Обновить pip:
```Bash
python -m pip install --upgrade pip 
```

- Установить зависимости:
```Bash
pip install -r requirements.txt
```

#### Применить миграций:
- Linux/MacOS:
```Bash
python3 manage.py migrate
```

- Windows:
```Bash
python manage.py migrate
```


#### Запустить проект:
- Linux/MacOS:
```Bash
python3 manage.py runserver
```

- Windows:
```Bash
python manage.py runserver
```

#### Создать суперпользователя:
- Linux/MacOS:
```Bash
python3 manage.py createsuperuser
```

- Windows:
```Bash
python manage.py createsuperuser
```

## Admin - панель
Доступна по эндпойнту:
```r
admin/
```

Полностью локализована и позволяет управлять пользователями и их действиями, а так же добавлять группы для постов.

---
Автор: [Сергей Кульбида](https://github.com/SergeyKDEV)
