from pathlib import Path

from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from modules.common.domain import exceptions as domain_exceptions
from modules.extract.domain.ports import repositories as domain_repositories

from ....config import settings


class DjangoFileDomainRepository(domain_repositories.AbstractFileDomainRepository):
    """
    See description of parent class to get more details.
    """

    def save(self, file: bytes, file_name: str) -> Path:
        file_system_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
        try:
            return Path(settings.MEDIA_ROOT) / Path(
                file_system_storage.save(file_name, ContentFile(file))
            )
        except OSError as err:
            raise domain_exceptions.FileSaveError(
                message="File '%s' can not be saved.", file_name=file_name
            ) from err
        except django_exceptions.SuspiciousFileOperation as err:
            raise domain_exceptions.FileSaveError(
                message="File '%s' can not be saved.", file_name=file_name
            ) from err
