from PIL import Image
import pyheif

def resize_length(img, length):
    if img.width / img.height >= 1:
        aspect_ratio = length / img.width
        new_width = length
        new_height = round(img.height * aspect_ratio)
    else:
        aspect_ratio = length / img.height
        new_width = round(img.width * aspect_ratio)
        new_height = length
    return img.resize((new_width, new_height))

def image_to_pil(file_storage):
    splited_mimetype = file_storage.mimetype.split('/')
    if not splited_mimetype[0] == 'image':
        return

    if splited_mimetype[1] == 'heic':
        heif_file = pyheif.read(file_storage)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
            )
        return image
    return Image.open(file_storage)