from dataclasses import dataclass, field

@dataclass
class Forecast_week:
    city_name: str = ""
    description: list = field(default_factory=list)
    days_name:list = field(default_factory=list)
    days_int:list = field(default_factory=list)
    temp_min:list = field(default_factory=list)
    temp_max:list = field(default_factory=list)

