from modules.common.domain import commands as common_commands
from modules.load.domain import commands


def test_save_data_command_is_domain_command_type():
    assert issubclass(commands.SaveData, common_commands.DomainCommand)
    assert commands.SaveData.__dataclass_params__.frozen
