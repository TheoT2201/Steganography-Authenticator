from PIL import Image

def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def embed_token_into_image(image_path, token):
    binary_token = text_to_binary(token)

    img = Image.open(image_path)
    pixels = img.load()

    data_index = 0
    binary_len = len(binary_token)
    print(binary_len)

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if data_index < binary_len:
                r, g, b = pixels[i, j]

                r = (r & ~1) | int(binary_token[data_index])
                data_index += 1
                if data_index < binary_len:
                    g = (g & ~1) | int(binary_token[data_index])
                    data_index += 1
                if data_index < binary_len:
                    b = (b & ~1) | int(binary_token[data_index])
                    data_index += 1
                
                pixels[i, j] = (r, g, b)
            
            else:
                break

        if data_index >= binary_len:
            break
    
    return img, binary_len