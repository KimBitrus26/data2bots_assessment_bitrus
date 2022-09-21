import os
from django.core.exceptions import ValidationError


def validate_file(value):
    """A function to validate upload file  not more than 5mb. """

    ext = os.path.splitext(value.name)[1]  # [1] returns file extension
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    if value.size > 5 * 1024 * 1024:  # max 5mb
        raise ValidationError("Image file too large (must be less than 5mb)")
    return value
