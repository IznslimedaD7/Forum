import os
import secrets
from flask import current_app
from PIL import Image
from app import login_manager
from models import Users

def save_image(img, folder, size):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(img.filename)
    img_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', folder)
    img_path = os.path.join(full_path, img_fn)
    output_size = size

    i = Image.open(img)
    i.thumbnail(output_size)
    i.save(img_path)
    return img_fn


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
