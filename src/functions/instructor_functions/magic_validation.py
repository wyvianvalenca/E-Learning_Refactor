import magic
import os

"""ADAPTER PATTERN"""

# EXTERNAL SERVICE

class SimpleMagicValidation:
    def __init__(self):
        try:
            self.magic = magic.Magic(mime=True)
            self.is_available = True

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
            
            mime_type = self.magic.from_file(file_path)
            return {
                'mime_type': mime_type,
                'error': None
            }

        except Exception as e:
            return {
                'mime_type': 'unknown',
                'error': f'erro ao determinar o tipo do arquivo: {e}'
            }
        
