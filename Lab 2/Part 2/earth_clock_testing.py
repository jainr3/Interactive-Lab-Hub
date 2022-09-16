from PIL import Image, ImageDraw

def crop_image_flat_earth(scale, l, t, r, b):
    print(f"Cropping image at scale {scale} with l={l}, t={t}, r={r}, b={b}.")
    im = Image.open('earth.png')
    width, height = im.size
    left = l + r - (2-scale)*r#scale*l
    top = t + b - (2-scale)*b#scale*t
    right = (2 - scale)*r
    bottom = (2- scale)*b
    print(f"Effective limits after scale l={left}, t={top}, r={right}, b={bottom}.")

    im1 = im.crop((left, top, right, bottom))
    im1 = im1.convert('RGB')
    im1 = im1.save("earth_cropped.jpg")

#l, t, r, b = 200, 80 + 146, 600, 80 + 146*2
l, t, r, b = 140, 170, 140 + 240, 170 + 135 
scale = 1.00

#scale += 0.10

# Right test
#r = min(800, r + 240)
#l = r - 240

# Left test
l = max(0, l - 240)
r = l + 240

# Down test
b = min(520, b + 135)
t = b - 135

# Up test
t = max(80, t - 135)
b = t + 135

crop_image_flat_earth(scale, l, t, r, b)