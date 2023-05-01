from PIL import Image, ImageTk

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
