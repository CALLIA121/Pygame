from PIL import Image

size = (35, 35)


def process_image_enemy(input_path, output_path):
    # Открываем изображение
    with Image.open(input_path) as img:
        # Сжимаем изображение до 34x34 пикселей
        img_resized_34 = img.resize((size[0] + 4, size[1] + 4))

        img_resized_34 = img_resized_34.transpose(Image.FLIP_LEFT_RIGHT)

        # Заменяем цвета всех непрозрачных пикселей на красный
        pixels = img_resized_34.load()
        for y in range(size[0] + 4):
            for x in range(size[1] + 4):
                if pixels[x, y][3] > 0:  # Если пиксель непрозрачный
                    pixels[x, y] = (255, 0, 0, 255)

        # Сжимаем исходное изображение до 30x30 пикселей
        img_resized_30 = img.resize(size)

        # Отражаем изображение по горизонтали
        img_resized_30 = img_resized_30.transpose(Image.FLIP_LEFT_RIGHT)

        # Накладываем сжатое изображение по центру
        position = (2, 2)
        img_resized_34.paste(img_resized_30, position, img_resized_30)

        # Обрезаем изображение до 30x30 пикселей
        final_image = img_resized_34.crop((2, 2, size[0], size[1]))

        # Сохраняем итоговое изображение
        final_image.save(f"{output_path}_e.png", format='PNG')


def process_image_normal(input_path, output_path):
    # Открываем изображение
    with Image.open(input_path) as img:
        # Сжимаем исходное изображение до 30x30 пикселей
        img_resized_30 = img.resize(size)

        img_resized_30.save(f"{output_path}_n.png", format='PNG')


# Путь к входному изображению
input_image_path = r'data\shooter.png'
# Путь для сохранения сжатого изображения
output_image_path = r'data\shooter'
# Сжимаем изображение (добавляем обводку врагу)
process_image_enemy(input_image_path, output_image_path)
process_image_normal(input_image_path, output_image_path)
# Путь к входному изображению
input_image_path = r'data\defender.png'
# Путь для сохранения сжатого изображения
output_image_path = r'data\defender'
# Сжимаем изображение (добавляем обводку врагу)
process_image_enemy(input_image_path, output_image_path)
process_image_normal(input_image_path, output_image_path)
# Путь к входному изображению
input_image_path = r'data\atacker.png'
# Путь для сохранения сжатого изображения
output_image_path = r'data\atacker'
# Сжимаем изображение (добавляем обводку врагу)
process_image_enemy(input_image_path, output_image_path)
process_image_normal(input_image_path, output_image_path)
