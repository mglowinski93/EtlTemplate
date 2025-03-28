from pathlib import Path

from django.conf import settings
from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from modules.extract.domain.ports import repositories as domain_repositories
from modules.extract.domain import value_objects

from ..exceptions import FileSaveError

from ..models import ExtractHistory


class DjangoFileDomainRepository(domain_repositories.AbstractFileDomainRepository):
    def save(self, file: bytes, file_name: str) -> Path:
        """
        :param file: File to extract data.
        :param file_name: File name to save file with.
        :raises FileSaveError: Failed to save file from which data must be extracted.

        :return: Path to the saved file.
        """

        try:
            return Path(settings.MEDIA_ROOT) / Path(
                FileSystemStorage(location=settings.MEDIA_ROOT).save(
                    file_name, ContentFile(file)
                )
            )
        except OSError as err:
            raise FileSaveError(
                message=f"File {file_name} can not be saved.", file_name=file_name
            ) from err
        except django_exceptions.SuspiciousFileOperation as err:
            raise FileSaveError(
                message=f"File {file_name} can not be saved.", file_name=file_name
            ) from err

class DjangoExtractDomainRepository(domain_repositories.AbstractExtractDomainRepository):
    def create(self, extract_history: value_objects.ExtractHistory) -> None:
        """
        See description of parent class to get more details.
        """

        ExtractHistory.objects.create(
            ExtractHistory(
                input_file_name = extract_history.input_file_name,
                saved_file_name = extract_history.saved_file_name,
            ) 
        )
