'''
Module vue_abstraite
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from abc import ABC, abstractmethod


class VueAbstraite(ABC):

    def nettoyer_console(self):
        for i in range(30):
            print("")

    @abstractmethod
    def afficher(self):
        pass

    @abstractmethod
    def choisir_menu(self):
        pass
