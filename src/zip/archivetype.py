from enum import Enum, auto


class ArchiveType(Enum):
    json = auto()
    html = auto()

    def __str__(self):
        return str(self.value)
