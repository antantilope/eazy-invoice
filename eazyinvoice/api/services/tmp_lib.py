
import uuid
import os.path

from django.conf import settings


def get_new_tmp_file_name(ext: str) -> str:
    fpath = os.path.join(settings.TMP_DIR, f"{uuid.uuid4()}.{ext}")
    if os.path.exists(fpath):
        return get_new_tmp_file_name(ext)
    else:
        return fpath
