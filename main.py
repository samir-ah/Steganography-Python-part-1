import png
import argparse
import sys
# return the binary value in 8bit of ascii decimal
def decimalToBinary(n):  
    binValue = bin(n).replace("0b", "")  
    return (8-len(binValue))*"0"+binValue
# reveive list with binary values corresponding to message chars ["010101","01010101"...]
def binaryToString(b):  
    result = ""
    for i in b:
        result += chr(int(i,2))
    return result

parser = argparse.ArgumentParser()
parser.add_argument("-w",action="store_true")
parser.add_argument("-f")
parser.add_argument("-t")
args = parser.parse_args()

file_name = None
message = None
if(args.f):
        file_name = args.f
else:
    file_name = input("Entrez le chemin du fichier source : ")

if args.w: #write on image -w
    if(args.t):
        message = args.t
    else:
        message = input("Entrez le message à cacher : ")
    r=png.Reader(file_name)
    # convert message into list with binary values per char
    input_message_binary_ascii_list = [decimalToBinary(ord(c)) for c in message]
    # print(input_message_binary_ascii_list)
    # check if the image size support the length of message
    nb_required_pixels = len(message)*3 # every char needs 3px
    nb_image_pixels = r.asRGBA8()[0]*r.asRGBA8()[1]
    if(nb_image_pixels < nb_required_pixels):
        print("image trop petite")
        sys.exit()
    
    pixels = []
    # read pixels from image
    for row in r.asRGBA8()[2]:
        pixels.append(list(row))
    # print(pixels)
    # with open('input.txt', 'w') as f:
    #     f.truncate()
    #     print(pixels, file=f)
    bit_index = 0
    char_index = 0
    print("encoder algo...")
    for row in range(0,len(pixels)-1):
        for col in range(0,len(pixels[row])-1):
            if(bit_index < 8):
                if(int(input_message_binary_ascii_list[char_index][bit_index])%2 == 0):
                    if(pixels[row][col]%2 != 0): 
                        if(pixels[row][col] == 255):
                            pixels[row][col] -= 1
                        else:
                            pixels[row][col] += 1
                else:
                    if(pixels[row][col]%2 == 0): 
                        if(pixels[row][col] == 255):
                            pixels[row][col] -= 1
                        else:
                            pixels[row][col] += 1
                bit_index += 1
            else:
                if(char_index+1 < len(input_message_binary_ascii_list)):
                    char_index += 1
                    bit_index = 0
                    if(pixels[row][col]%2 != 0): 
                        if(pixels[row][col] == 255):
                            pixels[row][col] -= 1
                        else:
                            pixels[row][col] += 1
                else:
                    if(pixels[row][col]%2 == 0): 
                        if(pixels[row][col] == 255):
                            pixels[row][col] -= 1
                        else:
                            pixels[row][col] += 1
                    break
    #print(len(pixels)*len(pixels[0]))
    # with open('output.txt', 'w') as f:
    #     f.truncate()
    #     print(pixels, file=f)   
    png.from_array(pixels, 'RGBA').save('output.png')  
    print("message cachée dans output.png")


