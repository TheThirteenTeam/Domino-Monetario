from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (2400, 602), color = 'black')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 90)
draw.text((0, 0), "Domino Back", (255, 255, 255), font=font)
img.save("dominoBack.png")