from abc import ABC, abstractmethod
from typing_extensions import override

import questionary
from rich.panel import Panel
from rich.text import Text

from src.inicial import console
from src.models.models import ForumPost, Usuario, Comentario
from src.validations import is_non_empty
