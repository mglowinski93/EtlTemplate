from ...domain import commands as domain_commands
from ....data.domain import value_objects as data_value_objects
import pandas as pd
import pandera as pa
from ....common.domain.exceptions import DataValidationException, DataFormatNotSupportedException
from typing import List

def extract(command : domain_commands.ExtractData) -> List[data_value_objects.InputData] : 
    #1) validate if file exists
    if not command.file_path.exists():
        raise FileNotFoundError("Input file doesn't exist.")
    
    #2) read file according to format
    suffix = command.file_path.suffix
    if suffix == ".csv":
        df = pd.read_csv(command.file_path)
    elif suffix == ".xls" or suffix == ".xlsx":
        df = pd.read_excel(command.file_path)
    else :
        raise DataFormatNotSupportedException(f"Data format {suffix} is not supported.")

    #3)validate dataframe
    try:
        validated_data : pd.DataFrame = data_value_objects.InputData.validate(df)
    except pa.errors.SchemaError as e:
        raise DataValidationException("Input data is invalid.")
    
    #4)translate it into list of data model
    dict_representation: dict = validated_data.to_dict(orient="records")
    input_data_rows = []
    for row in dict_representation:
        name = row["name"]
        surname = row["surname"]
        age = row["age"]
        is_satisfied = row["is_satisfied"]
        data_entry = data_value_objects.InputData(name, surname, age, is_satisfied)
        input_data_rows.append(data_entry)

    return input_data_rows

    # return InputData 
