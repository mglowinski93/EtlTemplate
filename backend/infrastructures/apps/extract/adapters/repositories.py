from pathlib import Path

from django.conf import settings
from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from modules.extract.domain.ports import repositories as domain_repositories

from ..exceptions import FileSaveError


class DjangoFileDomainRepository(domain_repositories.AbstractFileDomainRepository):
    def save(self, file: bytes, file_name: str) -> Path:
        """
        :param file: File to extract data.
        :param file_name: File name to save file with.
        :raises FileSaveError: Failed to save file from which data must be extracted.

        :return: Path to the saved file.
        """

        file_system_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
        try:
            return Path(settings.MEDIA_ROOT) / Path(
                file_system_storage.save(file_name, ContentFile(file))
            )
        except OSError as err:
            raise FileSaveError(
                message=f"File {file_name} can not be saved.", file_name=file_name
            ) from err
        except django_exceptions.SuspiciousFileOperation as err:
            raise FileSaveError(
                message=f"File {file_name} can not be saved.", file_name=file_name
            ) from err
