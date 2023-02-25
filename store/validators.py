from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_file = 200
    if file.size > max_size_file * 1024:
        raise ValidationError(f'file con not be langer than {max_size_file}kb')
