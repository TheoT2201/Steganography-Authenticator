from PIL import Image
import base64

def extract_token_from_image(image_path, data_length):
    img = Image.open(image_path)
    pixels = img.load()

    binary_data = ''
    bits_extracted = 0

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if bits_extracted < data_length:
                r, g, b = pixels[i, j]

                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

                bits_extracted += 3
            else:
                break
        if bits_extracted >= data_length:
            break
    
    return binary_data

def binary_to_text(binary_str):
    str_data = ''
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        str_data += chr(int(byte, 2))
    return str_data

def decode_base64(base64_str):
    return base64.b64decode(base64_str)