from dataclasses import dataclass, field

@dataclass
class User:
    name: str = ""
    lastname: str = ""
    id: int = 0
    city: str = ""
    status: str = 'Пользователь'


