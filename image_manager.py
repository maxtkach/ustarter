from os import listdir, remove
from os.path import isfile

UPLOAD_FOLDER = 'static/images_users'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

def getImagesCount():
    return len([f for f in listdir(UPLOAD_FOLDER) if "_" not in f])

def SaveImg(img):
    fileName = img.filename.split(".")
    fileName[0] = str(getImagesCount() + 1)
    fileName = f"{fileName[0]}.{fileName[-1]}"
    img.save(f"{UPLOAD_FOLDER}/{fileName}")
    return fileName

def EditImg(img, project):
    if isfile(f"{UPLOAD_FOLDER}/{getImageNameById(project.imageId)}"):
        remove(f"{UPLOAD_FOLDER}/{getImageNameById(project.imageId)}")
    fileName = img.filename.split(".")
    fileName[0] = str(project.imageId)
    fileName = f"{fileName[0]}.{fileName[-1]}"
    img.save(f"{UPLOAD_FOLDER}/{fileName}")
    return fileName

def SaveMedia(images):
    i = 1
    indexes = []
    for img in images:
        fileName = img.filename.split(".")
        fileName[0] = f"{getImagesCount()}_{i}"
        fileName = f"{fileName[0]}.{fileName[-1]}"
        img.save(f"{UPLOAD_FOLDER}/{fileName}")
        indexes.append(fileName)
        i += 1
    return " ".join(indexes)

def EditMedia(images, project):
    indexes = []
    media = getMediaNamesByIds(project.mediaNames)
    for m in media:
        if isfile(f"{UPLOAD_FOLDER}/{m}"):
            remove(f"{UPLOAD_FOLDER}/{m}")
    for i in range(len(images)):
        fileName = images[i].filename.split(".")
        fileName[0] = f"{project.imageId}_{i + 1}"
        fileName = f"{fileName[0]}.{fileName[-1]}"
        images[i].save(f"{UPLOAD_FOLDER}/{fileName}")
        indexes.append(fileName)
    return " ".join(indexes)

def getImageNameById(id):
    names = [f.split(".") for f in listdir(UPLOAD_FOLDER) if "_" not in f]
    for name in names:
        if int(name[0]) == id:
            return f"{name[0]}.{name[-1]}"

def getMediaNamesByIds(ids):
    return ids.split(" ")
