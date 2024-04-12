from dataclasses import dataclass, field

@dataclass
class Forecast:
    city_name: str = ""
    temp_now: int = None
    temp_feel: int = None
    time_now: str = ""
    description: list = field(default_factory=list)
    time:list = field(default_factory=list)
    temp:list = field(default_factory=list)


