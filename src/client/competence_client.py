'''
Module classe_client
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

import os
import requests

from typing import List, Optional
from utils.singleton import Singleton


class CompetenceClient(metaclass=Singleton):

    def __init__(self) -> None:
        self.HOST = os.environ["HOST_WEBSERVICE"]
        self.END_POINT = "/skills"

    def lister_competences(self) -> List[str]:

        req = requests.get(f"{self.HOST}{self.END_POINT}")

        return [c.get("name") for c in req.json().get("results")]
