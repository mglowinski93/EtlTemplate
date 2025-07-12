from modules.common.domain import commands as common_commands
from modules.extract.domain import commands


def test_extract_data_command_is_domain_command_type():
    assert issubclass(commands.ExtractData, common_commands.DomainCommand)
    assert commands.ExtractData.__dataclass_params__.frozen
