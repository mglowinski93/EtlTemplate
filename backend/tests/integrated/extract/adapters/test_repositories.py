import os


from modules.extract.domain import ports
from tests.test_const import CORRECT_INPUT_CSV

def test_django_file_domain_repository_save_method_saves_file_from_bytes(tmp_path,
    test_extract_django_domain_repository: ports.AbstractFileDomainRepository,
):
    # Given
    with open(CORRECT_INPUT_CSV, "rb") as file:
        file_bytes = file.read()

    # When
    result = test_extract_django_domain_repository.save(file_name=os.path.basename(CORRECT_INPUT_CSV), file=file_bytes, location=str(tmp_path))

    # Then
    assert isinstance(result, str)
    assert (tmp_path / result).exists()

#todo raise OS error
#todo raise suspicious file operation

#todo test DjangoExtractDomainRepository
