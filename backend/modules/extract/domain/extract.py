import backend.modules.extract.services.ports.strategies as ex
from backend.modules.data.domain.exceptions import FileTypeNotSupportedErrod
import pandas as pd
import services.ports.strategies as strat
from pathlib import Path


class ExtractManager:
    def extract(self, file_path: Path) -> pd.DataFrame:
        chosen_strat = self.chooseStrategy(file_path.suffix)
        return chosen_strat.extract(self.path_to_file)

    def chooseStrategy(
        supported_extensions: dict[str, strat.ExtractStrategy], file_extension: str
    ) -> ex.ExtractStrategy:
        strat = supported_extensions.get(file_extension)
        if strat == None:
            raise FileTypeNotSupportedErrod(file_extension)
