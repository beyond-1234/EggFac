from dataclasses import dataclass

@dataclass
class Track:
    """ 轨道实体类 """
    type: str
    name: str
    probe: None
