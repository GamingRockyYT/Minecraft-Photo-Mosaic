import os
import PIL
from PIL import Image
import timeit

start = timeit.default_timer()
temp, all = [], []
Tex_RGBval, AvgRGBval = {}, {}
sumR, sumG, sumB, count, absdiff, minabsdiff = 0, 0, 0, 0, 0, 300

image_path = "output1.jpg"  #Remove initially existing output
if os.path.isfile(image_path):
    os.remove(image_path)

image_path = "output.jpg"  #Remove initially existing output
if os.path.isfile(image_path):
    os.remove(image_path)

try:
    try:
        img = PIL.Image.open("target.webp")  #Lower dimension of input
        width, height = img.size
        inp = int(input(str(width) + " " + str(height) + " >>>"))
        image_path = "target.webp"
        output = Image.open(image_path, 'r').resize((width//inp, height//inp))
        try:
            output.save("output1.jpg", quality=95)
        except OSError:
            im = Image.open("target.webp").resize((width//inp, height//inp))
            rgb_im = im.convert('RGB')
            rgb_im.save('output1.jpg', quality=95)
    except FileNotFoundError:
        try:
            img = PIL.Image.open("target.jpeg")  # Lower dimension of input
            width, height = img.size
            image_path = "target.jpeg"
            inp = int(input(str(width) + " " + str(height) + " >>>"))
            output = Image.open(image_path, 'r').resize((width//inp, height//inp))
            output.save("output1.jpg", quality=95)
        except FileNotFoundError:
            img = PIL.Image.open("target.jpg")  # Lower dimension of input
            width, height = img.size
            image_path = "target.jpg"
            inp = int(input(str(width) + " " + str(height) + " >>>"))
            output = Image.open(image_path, 'r').resize((width//inp, height//inp))
            output.save("output1.jpg", quality=95)
except FileNotFoundError:
    img = PIL.Image.open("target.png")  # Lower dimension of input
    width, height = img.size
    image_path = "target.png"
    inp = int(input(str(width) + " " + str(height) + " >>>"))
    output = Image.open(image_path, 'r').resize((width//inp, height//inp))
    try:
        output.save("output1.jpg", quality=95)
    except OSError:
        inp = int(input(str(width) + " " + str(height) + " >>>"))
        im = Image.open("target.png").resize((width//inp, height//inp))
        rgb_im = im.convert('RGB')
        rgb_im.save('output1.jpg', quality=95)

image_path = "output1.jpg"  #Get RGB value of each pixel in compressed image
img = Image.open(image_path, 'r')
pix_val = list(img.getdata())
width, height = img.size

Tdir = 'C:\\Users\\User1\\Desktop\\Minecraft Photo Mosaic\\textures\\'    #Get textures dir (Change this to your own directory)
textures = [f for f in os.listdir(Tdir) if os.path.isfile(os.path.join(Tdir, f))]

for i in textures:  #Compare RGB value
    img2 = Image.open(Tdir + i, 'r')
    pix_val2 = list(img2.getdata())
    for j in pix_val2:
        j = list(j)
        if len(j) == 4:
            j.pop(3)
        if count == 256:
            all.append(temp)
            temp, count = [], 0
        temp.append(j)
        count += 1
all.append(temp)

for i in range(len(textures)):
    Tex_RGBval[textures[i]] = all[i]

for i in Tex_RGBval:
    for j in Tex_RGBval[i]:
        sumR += j[0]
        sumG += j[1]
        sumB += j[2]
        AvgRGBval[i] = [sumR/256, sumG/256, sumB/256]
    sumR, sumG, sumB = 0, 0, 0

sq=[]
for i in pix_val:
    for j in AvgRGBval:
        absdiff = 0
        absdiff += abs(i[0] - AvgRGBval[j][0])
        absdiff += abs(i[1] - AvgRGBval[j][1])
        absdiff += abs(i[2] - AvgRGBval[j][2])
        if absdiff < minabsdiff:
            minabsdiff = absdiff
            temp = j
    minabsdiff = 300
    sq.append(temp)

for i in range(len(sq)):
    sq[i] = Tdir + sq[i]

def image_grid(imgs, rows = height, cols = width):

    assert len(imgs) == rows * cols
    w, h = PIL.Image.open(imgs[0]).size
    grid = Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(PIL.Image.open(img), box=(i % cols * w, i // cols * h))
    return grid

grid = image_grid(sq, height, width)
grid.save("output.jpg")

image_path = "output1.jpg"  #Remove initially existing output
if os.path.isfile(image_path):
    os.remove(image_path)
stop = timeit.default_timer()

print('Runtime: ', stop - start, 'seconds')
