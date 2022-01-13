from flask import session

from app import app

import os

def has_signed_user() -> bool:
    return "signed_user" in session and session["signed_user"] != None

def retrieve_image(pk):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'front_cover_{pk}' in filename:
            return filename

def delete_image(pk):
    filename = retrieve_image(pk)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))