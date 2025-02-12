from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileExtracted:
    file_path: Path
