import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox

from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        # Создаем изображение размером 600x400 с белым фоном
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Создаем холст Tkinter размером 600x400 с белым фоном
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Переменные для отслеживания последних координат мыши
        self.last_x, self.last_y = None, None
        self.pen_color = 'black'  # Изначальный цвет пера
        self.brush_size = 1  # Изначальный размер кисти
        self.previous_color = self.pen_color  # Сохраняем предыдущий цвет пера

        # Список доступных размеров кисти
        self.brush_sizes = [1, 2, 5, 10]

        # Выпадающий список для выбора размера кисти
        self.brush_size_var = tk.StringVar(value=str(self.brush_sizes[0]))
        self.brush_size_menu = None  # Инициализируем переменную, но создаем меню позже

        # Привязываем события к холсту
        self.canvas.bind('<B1-Motion>', self.paint)  # Рисование при перемещении мыши с зажатой левой кнопкой
        self.canvas.bind('<ButtonRelease-1>', self.reset)  # Сброс координат при отпускании кнопки мыши

        self.setup_ui()

        # Кнопка для переключения на ластик/кисть
        self.eraser_button = tk.Button(self.root, text="Ластик", command=self.toggle_eraser)
        self.eraser_button.pack(side=tk.LEFT)

    def setup_ui(self):
        # Создаем фрейм для кнопок управления
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопка для очистки холста
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка для выбора цвета пера
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Кнопка для сохранения изображения
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Выпадающий список для выбора размера кисти
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *map(str, self.brush_sizes),
                                             command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT)

    def paint(self, event):
        # Рисование линии на холсте и на изображении
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        # Обновляем последние координаты мыши
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        # Сбрасываем последние координаты мыши
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        # Очищаем холст и создаем новое изображение с белым фоном
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        # Сохраняем текущий цвет перед выбором нового
        self.previous_color = self.pen_color
        # Открываем диалог выбора цвета и устанавливаем выбранный цвет
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        # Открываем диалог сохранения файла и сохраняем изображение в формате PNG
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, value):
        # Обновляем размер кисти на основе выбранного значения
        self.brush_size = int(value)

    def toggle_eraser(self):
        # Переключаемся между инструментом кисти и ластиком
        if self.pen_color == 'white':  # Если текущий цвет - белый, переключаемся обратно на предыдущий цвет
            self.pen_color = self.previous_color
            self.eraser_button.config(text="Ластик")  # Обновляем текст кнопки
        else:
            self.previous_color = self.pen_color  # Сохраняем текущий цвет перед переключением на ластик
            self.pen_color = 'white'  # Устанавливаем цвет пера на белый (цвет фона)
            self.eraser_button.config(text="Кисть")  # Обновляем текст кнопки


def main():
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
