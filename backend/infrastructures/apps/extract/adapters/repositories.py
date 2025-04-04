from pathlib import Path

from django.conf import settings
from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from modules.extract.domain import value_objects
from modules.extract.domain import ports

from ..exceptions import FileSaveError
from ..models import ExtractHistory


class DjangoFileDomainRepository(ports.AbstractFileDomainRepository):
    def save(self, file: bytes, file_name: str) -> Path:
        """
        :param file: File to extract data.
        :param file_name: File name to save file with.
        :raises FileSaveError: Failed to save file from which data must be extracted.

        :return: Name of the saved file.
        """

        try:
            return FileSystemStorage(location=settings.MEDIA_ROOT).save(
                    name=file_name, content=ContentFile(file)
                )
            
        except OSError as err:
            raise FileSaveError(
                message=f"File {file_name} can not be saved.", file_name=file_name
            ) from err
        except django_exceptions.SuspiciousFileOperation as err:
            raise FileSaveError(
                message=f"File {file_name} can not be saved.", file_name=file_name
            ) from err

    def file_exists(self, file_name: str) -> bool:
        """
        See description of parent class to get more details.
        """

        return (Path(settings.MEDIA_ROOT) / file_name).exists


class DjangoExtractDomainRepository(ports.AbstractExtractDomainRepository):
    def create(self, extract_history: value_objects.ExtractHistory) -> None:
        """
        See description of parent class to get more details.
        """

        ExtractHistory.objects.create(
            input_file_name=extract_history.input_file_name,
            saved_file_name=extract_history.saved_file_name,
            created_at=extract_history.timestamp,
        )
