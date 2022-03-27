from PIL import Image, ImageDraw, ImageFont

DOMINOS_VALUES = ["0", "005", "010", "025", "050", "1", "2", "5", "10", "20", "50", "100", "200"]

for i, dom1 in enumerate(DOMINOS_VALUES):
    for j, dom2 in enumerate(DOMINOS_VALUES):
        if i >= j:
            print(i, "->", dom1, "-", j, "->", dom2)
            img = Image.new('RGB', (2400, 602), color = 'black')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 90)
            draw.text((0, 0), "{}_{}".format(dom1, dom2), (255, 255, 255), font=font)
            img.save("../images/domino{}_{}.png".format(dom1, dom2))