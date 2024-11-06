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
        self.image = Image.new("RGB", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.canvas = tk.Canvas(root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg='white')
        self.canvas.pack()

        # Переменные для отслеживания состояния
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = self.BRUSH_SIZES[0]
        self.previous_color = self.pen_color

        # Инициализация переменных для UI
        self.brush_size_var = tk.StringVar(value=str(self.BRUSH_SIZES[0]))
        self.eraser_button = None

        # Привязываем события к холсту
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-2>', self.pick_color)

        # Привязываем горячие клавиши
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

        self.setup_ui()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        tk.Button(control_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Сохранить", command=self.save_image).pack(side=tk.LEFT)

        tk.OptionMenu(control_frame, self.brush_size_var, *map(str, self.BRUSH_SIZES),
                      command=self.update_brush_size).pack(side=tk.LEFT)

        self.eraser_button = tk.Button(self.root, text="Ластик", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT)

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

    def clear_canvas(self):
        """
        Очистка холста и создание нового изображения с белым фоном.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """
        Выбор цвета пера с помощью диалога выбора цвета.
        """
        self.set_pen_color(colorchooser.askcolor(color=self.pen_color)[1])

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

    def save_image(self, event=None):
        """
        Сохранение изображения в формате PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, value):
        """
        Обновление размера кисти на основе выбранного значения.

        :param value: Выбранное значение размера кисти.
        """
        self.brush_size = int(value)

    def toggle_eraser(self):
        """
        Переключение между инструментом кисти и ластиком.
        """
        if self.pen_color == 'white':  # Если текущий цвет - белый, переключаемся обратно на предыдущий цвет
            self.set_pen_color(self.previous_color)
            self.eraser_button.config(text="Ластик")  # Обновляем текст кнопки
        else:
            self.set_pen_color('white')  # Устанавливаем цвет пера на белый (цвет фона)
            self.eraser_button.config(text="Кисть")  # Обновляем текст кнопки


def main():
    """
    Основная функция для запуска приложения.
    """
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()