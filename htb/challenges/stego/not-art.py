from PIL import Image

img_name = 'not_art.png'

try:
    img = Image.open(img_name)   # Return an Image object
except:
    print ('Put not_art.png file on this directory')
    exit(1)

pixels = img.load()

processed_rgb = []
rgb_decoded = []

first = 0
last = 29

while first*10+5 < 135: #Just follow the lines of the image each 10 pixels (blocks)
    for i in range(first, last+1):
        processed_rgb.append(pixels[i*10+5,first*10+5])
    for i in range(first+1, last+1):
        processed_rgb.append(pixels[last*10+5,i*10+5])
    for i in reversed(range(first, last)):
        processed_rgb.append(pixels[i*10+5,last*10+5])
    for i in reversed(range(first+2, last)):
        processed_rgb.append(pixels[first*10+5,i*10+5])
    processed_rgb.append(pixels[(first+1)*10+5,(first+2)*10+5])
    first += 2
    last -= 2
processed_rgb.append(pixels[145,145])
processed_rgb.append(pixels[155,145])
processed_rgb.append(pixels[155,155])
#print(processed_rgb)

for i in range(len(processed_rgb)):
    temp = 0
    for j in range(3):  # Conversion to base 3
        if processed_rgb[i][j] == 192:
            temp += 1*(3**(2-j))
        if processed_rgb[i][j] == 255:
            temp += 2*(3**(2-j))
    rgb_decoded.append(chr(97+((temp+12)%26))) # ROT+13 decode + ascii decode
    #print(temp, chr(97+((temp+12)%26)))

message = "".join(rgb_decoded)
print(message)
message = message.replace("underscore", "_")
message = message.replace("leftcurlybracket", "{")
message = message.replace("rightcurlybracket", "}")
message = message.replace("exclamationmark", "!")
message = message.replace("lowercase", "")

while message.find("uppercase") != -1:
    array = list(message)
    array[message.find("uppercase") + 9] = array[message.find("uppercase") + 9].upper()
    message = "".join(array)
    message = message.replace("uppercase", "", 1)

message = message.replace("htb", "HTB").replace("eof", "")

print(message)