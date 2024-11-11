# Рисовалка на Python с использованием Tkinter и Pillow

Этот проект представляет собой простую рисовалку, написанную на Python с использованием библиотек Tkinter и Pillow. Приложение позволяет пользователю рисовать на холсте, выбирать цвет и размер кисти, а также сохранять результат в формате PNG.

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [Структура проекта](#структура-проекта)
- [Функциональность](#функциональность)
- [Горячие клавиши](#горячие-клавиши)
- [Контакты](#контакты)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/kenisdee/Drawing_app.git

2. Перейдите в директорию проекта:

   ```bash
   cd Drawing_app

3. Создайте виртуальное окружение:

   ```bash
   python3 -m venv venv

4. Активируйте виртуальное окружение:

   ```bash
   source venv/bin/activate

5. Установите зависимости:

   ```bash
   pip3 install -r requirements.txt

## Использование

1. Запуск проекта:

   ```bash
   python3 drawing_app.py

## Структура проекта

drawing_app.py: Основной файл с кодом приложения.

requirements.txt: Файл с зависимостями проекта.

README.md: Файл с описанием проекта.

## Функциональность

**Рисование:** Начните рисовать, перемещая мышь с зажатой левой кнопкой.

**Выбор цвета:** Используйте кнопку "Выбрать цвет". Доступны горячие клавиши Control+C, чтобы изменить цвет кисти.

**Выбор размера кисти:** Выберите размер кисти из выпадающего списка. Доступны горячие клавиши Control+[ для уменьшения или Control+] для увеличения размера кисти.

**Выбор цвета холста:** Используйте кнопку "Изменить фон". Доступны горячие клавиши Control+B, чтобы изменить цвет фона.

**Добавление текста:** Используйте кнопку "Текст". Доступны горячие клавиши Control+T, чтобы добавить текст.

**Ластик:** Переключайтесь между кистью и ластиком с помощью кнопки "Ластик/Кисть". Доступны горячие клавиши Control+E

**Пипетка:** При нажатии правой (macOS) или средней (колеса прокрутки) (Windows, Linux) кнопки мыши на холсте будет выбран цвет пикселя под курсором, и этот цвет станет текущим цветом пера.

**Очистка холста:** Нажмите "Очистить", чтобы очистить холст. Доступны горячие клавиши Control+N

**Изменение размера холста:** Нажмите "Изменить размер холста", чтобы изменить размер холста. Доступны горячие клавиши Control+R

**Сохранение изображения:** Нажмите "Сохранить", чтобы сохранить изображение в формате PNG. Доступны горячие клавиши Control+S

## Горячие клавиши

**Очистка холста:** Control+N

**Выбор цвета фона:** Control+B

**Добавление текста** Control+T

**Переключение между инструментами Ластик/Кисть:** Control+E

**Выбор цвета кисти:** Control+C

**Увеличение размера кисти:** Control+]

**Уменьшение размера кисти:** Control+[

**Изменение размера холста:** Control+R

**Сохранение изображения:** Control+S

## Контакты

Для связи с автором проекта, пожалуйста, используйте следующие контактные данные:

Email: kenisdee@ya.ru

GitHub: https://github.com/kenisdee