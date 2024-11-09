import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox

from PIL import Image, ImageDraw


class DrawingApp:
    """
    Класс DrawingApp представляет собой простое приложение для рисования с использованием библиотек tkinter и Pillow.
    """

    CANVAS_WIDTH = 600  # Ширина холста
    CANVAS_HEIGHT = 400  # Высота холста
    BRUSH_SIZES = [1, 2, 5, 10]  # Доступные размеры кисти

    def __init__(self, root):
        """
        Инициализация приложения.

        :param root: Основное окно Tkinter.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создаем изображение и холст
        self.image = Image.new("RGB", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT),
                               "white")  # Создаем новое изображение с белым фоном
        self.draw = ImageDraw.Draw(self.image)  # Создаем объект для рисования на изображении
        self.canvas = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                bg='white')  # Создаем холст Tkinter с белым фоном
        self.canvas.pack()  # Размещаем холст в окне

        # Переменные для отслеживания состояния
        self.last_x, self.last_y = None, None  # Инициализация координат последней точки рисования
        self.pen_color = 'black'  # Установка начального цвета кисти
        self.brush_size = self.BRUSH_SIZES[0]  # Установка начального размера кисти
        self.previous_color = self.pen_color  # Сохранение текущего цвета кисти как предыдущего

        # Инициализация переменных для UI
        self.brush_size_var = tk.StringVar(
            value=str(self.BRUSH_SIZES[0]))  # Переменная для хранения текущего размера кисти
        self.eraser_button = None  # Кнопка для переключения между кистью и ластиком

        # Привязываем события к холсту
        self.canvas.bind('<B1-Motion>',
                         self.paint)  # Привязываем событие движения мыши с зажатой левой кнопкой к методу paint
        self.canvas.bind('<ButtonRelease-1>',
                         self.reset)  # Привязываем событие отпускания левой кнопки мыши к методу reset
        self.canvas.bind('<Button-2>',
                         self.pick_color)  # Привязываем событие нажатия средней кнопки мыши (правой на некоторых системах) к методу pick_color

        # Привязываем горячие клавиши
        self.root.bind('<Control-s>', self.save_image)  # Привязываем сохранение изображения к комбинации Ctrl+S
        self.root.bind('<Control-c>', self.choose_color)  # Привязываем выбор цвета к комбинации Ctrl+C
        self.root.bind('<Control-e>', self.toggle_eraser)  # Привязываем переключение ластика к комбинации Ctrl+E
        self.root.bind('<Control-n>', self.clear_canvas)  # Привязываем очистку холста к комбинации Ctrl+N
        self.root.bind('<Control-[>',
                       self.decrease_brush_size)  # Привязываем уменьшение размера кисти к комбинации Ctrl+[
        self.root.bind('<Control-]>',
                       self.increase_brush_size)  # Привязываем увеличение размера кисти к комбинации Ctrl+]
        self.root.bind('<Control-r>',
                       self.change_canvas_size)  # Привязываем изменение размера холста к комбинации Ctrl+R

        # Добавляем холст для предварительного просмотра цвета кисти
        self.color_preview_canvas = tk.Canvas(self.root, width=25, height=25, bg=self.pen_color)
        self.color_preview_canvas.pack(side=tk.LEFT, padx=5)

        self.setup_ui()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса.
        """
        control_frame = tk.Frame(self.root)  # Создаем фрейм для размещения элементов управления
        control_frame.pack(fill=tk.X)  # Размещаем фрейм в окне, заполняя его по горизонтали

        tk.Button(control_frame, text="Очистить", command=self.clear_canvas).pack(
            side=tk.LEFT)  # Добавляем кнопку "Очистить"
        tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color).pack(
            side=tk.LEFT)  # Добавляем кнопку "Выбрать цвет"
        tk.Button(control_frame, text="Сохранить", command=self.save_image).pack(
            side=tk.LEFT)  # Добавляем кнопку "Сохранить"
        tk.Button(control_frame, text="Изменить размер холста", command=self.change_canvas_size).pack(
            side=tk.LEFT)  # Добавляем кнопку для изменения размера холста

        tk.OptionMenu(control_frame, self.brush_size_var, *map(str, self.BRUSH_SIZES),
                      # Добавляем выпадающий список для выбора размера кисти
                      command=self.update_brush_size).pack(side=tk.LEFT)

        self.eraser_button = tk.Button(self.root, text="Ластик",
                                       command=self.toggle_eraser)  # Добавляем кнопку "Ластик"
        self.eraser_button.pack(side=tk.LEFT)  # Размещаем кнопку "Ластик" слева

    def paint(self, event):
        """
        Рисование линии на холсте и на изображении.

        :param event: Событие Tkinter, содержащее координаты мыши.
        """
        if self.last_x and self.last_y:
            # Рисуем линию на холсте Tkinter
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            # Рисуем линию на изображении Pillow
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        # Обновляем последние координаты мыши
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        """
        Сброс последних координат мыши.

        :param event: Событие Tkinter.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self, event=None):
        """
        Очистка холста и создание нового изображения с белым фоном.
        """
        self.canvas.delete("all")  # Очищаем холст от всех элементов
        self.image = Image.new("RGB", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT),
                               "white")  # Создаем новое изображение с белым фоном
        self.draw = ImageDraw.Draw(self.image)  # Создаем объект для рисования на изображении

    def choose_color(self, event=None):
        """
        Выбор цвета пера с помощью диалога выбора цвета.
        """
        color = colorchooser.askcolor(color=self.pen_color)[1]  # Вызываем диалог выбора цвета и получаем выбранный цвет
        if color:  # Проверяем, что цвет был выбран
            self.set_pen_color(color)  # Устанавливаем выбранный цвет кисти

    def pick_color(self, event):
        """
        Выбор цвета с холста при нажатии правой кнопки мыши.

        :param event: Событие Tkinter, содержащее координаты мыши.
        """
        x, y = event.x, event.y
        color = self.image.getpixel((x, y))  # Получаем цвет пикселя с изображения
        self.set_pen_color('#%02x%02x%02x' % color)  # Преобразуем цвет в формат HEX

    def set_pen_color(self, color):
        """
        Установка цвета пера и сохранение предыдущего цвета.

        :param color: Новый цвет пера.
        """
        self.previous_color = self.pen_color  # Сохраняем предыдущий цвет
        self.pen_color = color  # Устанавливаем новый цвет
        self.color_preview_canvas.config(bg=self.pen_color)  # Обновляем цвет предварительного просмотра

    def save_image(self, event=None):
        """
        Сохранение изображения в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(
            filetypes=[('PNG files', '*.png')])  # Открываем диалог сохранения файла с фильтром для PNG файлов
        if file_path:  # Если пользователь выбрал путь для сохранения
            if not file_path.endswith('.png'):  # Если путь не заканчивается на .png, добавляем его
                file_path += '.png'
            self.image.save(file_path)  # Сохраняем изображение по выбранному пути
            messagebox.showinfo("Информация",
                                "Изображение успешно сохранено!")  # Показываем сообщение об успешном сохранении

    def update_brush_size(self, value):
        """
        Обновление размера кисти на основе выбранного значения.

        :param value: Выбранное значение размера кисти.
        """
        self.brush_size = int(value)

    def toggle_eraser(self, event=None):
        """
        Переключение между инструментом кисти и ластиком.
        """
        if self.pen_color == 'white':  # Если текущий цвет - белый, переключаемся обратно на предыдущий цвет
            self.set_pen_color(self.previous_color)
            self.eraser_button.config(text="Ластик")  # Обновляем текст кнопки
        else:
            self.set_pen_color('white')  # Устанавливаем цвет пера на белый (цвет фона)
            self.eraser_button.config(text="Кисть")  # Обновляем текст кнопки

    def decrease_brush_size(self, event=None):
        """
        Уменьшение размера кисти.
        """
        current_index = self.BRUSH_SIZES.index(self.brush_size)  # Получаем индекс текущего размера кисти
        if current_index > 0:
            self.brush_size = self.BRUSH_SIZES[current_index - 1]  # Уменьшаем размер кисти на один шаг
            self.brush_size_var.set(str(self.brush_size))  # Обновляем значение переменной размера кисти

    def increase_brush_size(self, event=None):
        """
        Увеличение размера кисти.
        """
        current_index = self.BRUSH_SIZES.index(self.brush_size)  # Получаем индекс текущего размера кисти
        if current_index < len(
                self.BRUSH_SIZES) - 1:  # Проверяем, не является ли текущий размер кисти последним в списке
            self.brush_size = self.BRUSH_SIZES[current_index + 1]  # Увеличиваем размер кисти на следующий в списке
            self.brush_size_var.set(str(self.brush_size))  # Обновляем значение переменной размера кисти в интерфейсе

    def change_canvas_size(self, event=None):
        """
        Изменение размера холста.
        """
        # Создаем новое диалоговое окно для ввода новых размеров холста
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение размера холста")

        # Добавляем метку и поле ввода для ширины
        tk.Label(dialog, text="Ширина:").grid(row=0, column=0)
        width_entry = tk.Entry(dialog)
        width_entry.insert(0, str(self.CANVAS_WIDTH))  # Предзаполняем поле текущей шириной холста
        width_entry.grid(row=0, column=1)

        # Добавляем метку и поле ввода для высоты
        tk.Label(dialog, text="Высота:").grid(row=1, column=0)
        height_entry = tk.Entry(dialog)
        height_entry.insert(0, str(self.CANVAS_HEIGHT))  # Предзаполняем поле текущей высотой холста
        height_entry.grid(row=1, column=1)

        # Определяем функцию для применения изменений
        def apply_changes():
            new_width = int(width_entry.get())  # Получаем введенную ширину
            new_height = int(height_entry.get())  # Получаем введенную высоту
            if new_width > 0 and new_height > 0:  # Проверяем, что введенные значения положительные
                self.CANVAS_WIDTH = new_width  # Обновляем ширину холста
                self.CANVAS_HEIGHT = new_height  # Обновляем высоту холста

                # Обновляем размер холста
                self.canvas.config(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)

                # Создаем новое изображение с новыми размерами
                self.image = Image.new("RGB", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), "white")
                self.draw = ImageDraw.Draw(self.image)

                # Очищаем текущий холст
                self.canvas.delete("all")

            dialog.destroy()

        # Создаем кнопку "Применить" и привязываем ее к функции apply_changes
        tk.Button(dialog, text="Применить", command=apply_changes).grid(row=2, columnspan=2)


def main():
    """
    Основная функция для запуска приложения.
    """
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
