from flask import send_file

def save_image(image, username):
    path = f'website/static/{username}.png'
    image.save(path)
    return path