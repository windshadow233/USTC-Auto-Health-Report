from PIL import Image
import imageio
import cv2


img = imageio.read('gif_green.gif')
for i in range(img.get_length()):
    png = img.get_data(i)
    png = cv2.resize(png, (300, 300), cv2.INTER_LINEAR)
    image = Image.fromarray(png)
    # image = image.resize((300, 300), Image.ANTIALIAS)
    image.save(f'xcm/gif_green/gif_{i}.png')
