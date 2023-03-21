from os import listdir

UPLOAD_FOLDER = 'static/images_users'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getImagesCount():
    return len([f for f in listdir(UPLOAD_FOLDER)])

def SaveImg(img):
    fileName = img.filename.split(".")
    fileName[0] = str(getImagesCount() + 1)
    fileName = ".".join(fileName)
    img.save(f"{UPLOAD_FOLDER}/{fileName}")

def getImageNameById(id):
    names = [f.split(".") for f in listdir(UPLOAD_FOLDER)]
    for name in names:
        if int(name[0]) == id:
            return ".".join(name)
