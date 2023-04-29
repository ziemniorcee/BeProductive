from PIL import Image, ImageTk
import math

images = []
img_id = 0


def create_imagetk(file, x, y, angle=0, index=0):
    global images
    global img_id
    img = Image.open(file)
    img = img.resize((x, y))
    print(img_id)
    images.append(ImageTk.PhotoImage(img.rotate(-angle)))
    img_id += 1

    if index == 0:
        return images[img_id - 1]
    else:

        return images[index]


def calculate_angle(x, y, r1, hour):
    angle = 0
    round1 = r1

    if y <= 250 and x >= 250:
        a = 250 - y
        b = x - 250
        if a == 0:
            angle = 90
        else:
            tangens = b / a
            angle = math.degrees(math.atan(tangens))
    elif y >= 250 and x >= 250:
        a = y - 250
        b = x - 250

        if b == 0:
            angle = 180
        else:
            tangens = a / b
            angle = math.degrees(math.atan(tangens)) + 90
    elif y >= 250 and x <= 250 and round1 != 0:
        a = y - 250
        b = 250 - x

        if a == 0:
            angle = 270
        else:
            tangens = b / a
            angle = math.degrees(math.atan(tangens)) + 180
    elif y <= 250 and x <= 250 and round1 != 0:
        a = 250 - y
        b = 250 - x

        if a == 0:
            angle = 0
        else:
            tangens = a / b
            angle = math.degrees(math.atan(tangens)) + 270

    return angle
