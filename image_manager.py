from os import listdir, remove
from os.path import isfile

UPLOAD_FOLDER = 'static/images_users'
UPLOAD_FOLDER_AVATARS = 'static/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

def getImagesCount(upload_folder=UPLOAD_FOLDER):
    return len([f for f in listdir(upload_folder) if "_" not in f])

def SaveImg(img, upload_folder=UPLOAD_FOLDER, img_id=0):
    fileName = img.filename.split(".")
    fileName[0] = str(getImagesCount() + 1) if img_id == 0 else img_id
    fileName = f"{fileName[0]}.{fileName[-1]}"
    img.save(f"{upload_folder}/{fileName}")
    return fileName

def EditImg(img, obj, upload_folder=UPLOAD_FOLDER):
    if isfile(f"{upload_folder}/{getImageNameById(obj.id)}"):
        remove(f"{upload_folder}/{getImageNameById(obj.id)}")
    fileName = img.filename.split(".")
    fileName[0] = str(obj.id)
    fileName = f"{fileName[0]}.{fileName[-1]}"
    img.save(f"{upload_folder}/{fileName}")
    return fileName

def SaveMedia(images, upload_folder=UPLOAD_FOLDER, img_id=0):
    i = 1
    indexes = []
    for img in images:
        fileName = img.filename.split(".")
        fileName[0] = f"{str(getImagesCount() + 1) if img_id == 0 else img_id}_{i}"
        fileName = f"{fileName[0]}.{fileName[-1]}"
        img.save(f"{upload_folder}/{fileName}")
        indexes.append(fileName)
        i += 1
    return " ".join(indexes)

def EditMedia(images, project, upload_folder=UPLOAD_FOLDER):
    indexes = []
    media = getMediaNamesByIds(project.mediaNames)
    for m in media:
        if isfile(f"{upload_folder}/{m}"):
            remove(f"{upload_folder}/{m}")
    for i in range(len(images)):
        fileName = images[i].filename.split(".")
        fileName[0] = f"{project.id}_{i + 1}"
        fileName = f"{fileName[0]}.{fileName[-1]}"
        images[i].save(f"{upload_folder}/{fileName}")
        indexes.append(fileName)
    return " ".join(indexes)

def getImageNameById(id, upload_folder=UPLOAD_FOLDER):
    names = [f.split(".") for f in listdir(upload_folder) if "_" not in f]
    for name in names:
        if int(name[0]) == id:
            return f"{name[0]}.{name[-1]}"

def getMediaNamesByIds(ids):
    return ids.split(" ")
