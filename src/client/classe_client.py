from typing import List, Optional
from utils.singleton import Singleton
import requests


class ClasseClient(metaclass=Singleton):

    def __init__(self) -> None:
        self.HOST = "https://www.dnd5eapi.co/api"
        self.END_POINT = "/classes"

    def lister_classes(self) -> List[str]:

        req = requests.get(f"{self.HOST}{self.END_POINT}")

        return [c.get("name") for c in req.json().get("results")]
