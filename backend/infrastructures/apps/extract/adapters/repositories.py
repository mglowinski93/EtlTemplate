import io
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from modules.extract.domain.ports import repositories as domain_repositories
from ....config import settings

class DjangoFileDomainRepository(domain_repositories.AbstractFileDomainRepository):
    """
    See description of parent class to get more details.
    """

    def save(self, byte_stream: io.BytesIO, file_name: str) -> Path:
        file_system_storage = FileSystemStorage(location=settings.MEDIA_ROOT)
        saved_file_name = file_system_storage.save(file_name, ContentFile(byte_stream.getvalue()))
        return Path(settings.MEDIA_ROOT) / Path(saved_file_name)
