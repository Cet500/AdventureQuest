import os
from typing import Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
from io import BytesIO
from ..config import MEDIA_FOLDER, LOCATION_FOLDER


def ensure_media_folder():
    os.makedirs( MEDIA_FOLDER, exist_ok = True )
    os.makedirs( MEDIA_FOLDER + LOCATION_FOLDER, exist_ok = True )


def validate_and_save_image(upload: UploadFile) -> Tuple[str, int, int, int, str]:
    """
    Проверяет изображение, сохраняет в media/locations/, возвращает:
    (relative_path, width, height, size_bytes, mime)
    """

    content = upload.file.read()

    if not content:
        raise HTTPException(400, "File is empty")

    # Проверка MIME-типа
    if not upload.content_type.startswith("image/"):
        raise HTTPException(400, "Uploaded file is not an image")

    try:
        image = Image.open(BytesIO(content))
        width, height = image.size
        mime = Image.MIME.get(image.format, upload.content_type)
    except Exception:
        raise HTTPException(400, "Invalid image file")

    ensure_media_folder()

    filename = upload.filename
    save_path = os.path.join( MEDIA_FOLDER, LOCATION_FOLDER, filename )

    # Избегаем перезаписи
    base, ext = os.path.splitext(filename)
    i = 1
    while os.path.exists(save_path):
        filename = f"{base}_{i}{ext}"
        save_path = os.path.join( MEDIA_FOLDER, LOCATION_FOLDER, filename )
        i += 1

    with open(save_path, "wb") as f:
        f.write(content)

    rel_path = f"{LOCATION_FOLDER}{filename}"

    size_bytes = len(content)

    return rel_path, width, height, size_bytes, mime
