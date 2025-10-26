import magic
import os

from src.inicial import console


class SimpleMagicValidation:
    """ ADAPTER PATTERN - Adaptee (biblioteca externa python-magic) """

    def __init__(self):
        try:
            self.magic: magic.Magic = magic.Magic(mime=True)
            self.is_available: bool = True

        except Exception as e:
            self.is_available = False
            raise RuntimeError(f"Magic library is not available: {e}")

    def get_file_type(self, file_path: str) -> dict[str, str]:
        if not self.is_available:
            return {
                'mime_type': 'unknown',
                'error': 'python-magic nao esta disponivel'
            }

        try:
            if not os.path.exists(file_path):
                return {
                    'mime_type': 'unknown',
                    'error': 'arquivo nao encontrado'
                }

            if not os.path.isfile(file_path):
                return {
                    'mime_type': 'unknown',
                    'error': 'caminho nao e um arquivo'
                }

            mime_type: str = self.magic.from_file(file_path)
            return {
                'mime_type': mime_type,
                'error': ''
            }

        except Exception as e:
            return {
                'mime_type': 'unknown',
                'error': f'erro ao determinar o tipo do arquivo: {e}'
            }

    def validate_file_type(self, file_path: str, expected_type: str) -> bool:
        result: dict[str, str] = self.get_file_type(file_path)

        if result['error']:
            console.print(result['error'])
            return False

        # Mapping expected types to MIME types
        type_mapping: dict[str, str] = {
            'pdf': 'application/pdf',
            'vídeo': 'video/mp4',
            'powerpoint': 'application/vnd.ms-powerpoint'
        }

        expected_mime = type_mapping.get(expected_type.lower())

        # Compares real MIME type with expected MIME type
        return result['mime_type'] == expected_mime


class MagicPythonValidationAdapter(Handler):
    """ ADAPTER PATTERN - Adapter para integrar python-magic nos validadores """

    @override
    def get_name(self) -> str:
        return "Validação do Tipo Real do Arquivo"

    @override
    def handle(self, content: Conteudo) -> ValidationResult:
        if not isinstance(content, Externo):
            return ValidationResult(
                is_valid=True,
                message="Não é conteúdo externo, pulando validação...",
                validator_name=self.get_name()
            )

        real_type_matches: bool = SimpleMagicValidation(). \
            validate_file_type(content.caminho, content.tipo)

        if not real_type_matches:
            return ValidationResult(
                is_valid=False,
                message="O tipo real do arquivo não corresponde ao tipo esperado.",
                validator_name=self.get_name()
            )

        return ValidationResult(
            is_valid=True,
            message="O tipo real do arquivo corresponde ao esperado.",
            validator_name=self.get_name()
        )