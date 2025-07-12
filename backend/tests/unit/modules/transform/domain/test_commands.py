from modules.common.domain import commands as common_commands
from modules.transform.domain import commands


def test_save_data_command_is_domain_command_type():
    assert issubclass(commands.TransformData, common_commands.DomainCommand)
    assert commands.TransformData.__dataclass_params__.frozen
