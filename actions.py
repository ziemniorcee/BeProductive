from PIL import Image, ImageTk

images = []
img_id = 0


def create_imagetk(file, x=0, y=0, angle=0, index=0):
    global images
    global img_id
    img = Image.open(file)
    if x != 0:
        img = img.resize((x, y))

    images.append(ImageTk.PhotoImage(img.rotate(-angle)))
    img_id += 1

    if index == 0:
        return images[img_id - 1]
    else:

        return images[index]


def calculate_category(block, arr):
    for cat in range(2):
        for i in range(len(arr[cat])):
            for j in range(3):
                if arr[cat][i][j] == block:
                    return cat, i


def calculate_element(block, arr):
    for i in range(len(arr)):
        for j in range(3):
            if arr[i][j] == block:
                return i


def format_time(minutes):
    """from 00(minutes) to 00:00"""
    hour = int(minutes) // 60
    minutes = int(minutes) % 60
    timer = f"{hour if hour > 9 else '0' + str(hour)}:{minutes if minutes > 9 else '0' + str(minutes)}"
    return timer


def deformat_time(timer):
    """from 00:00 to 00(minutes)"""
    hours = timer[0:2]
    minutes = timer[3:5]
    intiger = int(hours) * 60 + int(minutes)
    return str(intiger)
