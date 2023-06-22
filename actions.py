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


def calculate_element(block, arr):
    for i in range(len(arr)):
        for j in range(3):
            if arr[i][j] == block:
                return i
