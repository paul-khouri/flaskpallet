import secrets
file_string="hello.jpg"
ALLOWED_EXTENSIONS = {'txt' , 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    if '.' in filename:
        extension = filename.rsplit('.',1)[1].lower()
        if extension in ALLOWED_EXTENSIONS:
            return secrets.token_hex()+'.'+extension
        else:
            return None
    else:
        return None

print(allowed_file(file_string))
