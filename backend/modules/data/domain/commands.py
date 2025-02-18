from dataclasses import dataclass
from pathlib import Path
import value_objects as data_value_objects


@dataclass
class ExtractData:
    file_path: Path

@dataclass
class TransformData:
    input_data: data_value_objects.InputData

@dataclass
class SaveData:
    output_data: data_value_objects.OutputData    
