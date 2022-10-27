'''
Module message_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from dao.message_dao import MessageDao


class MessageService:

    def creer(self, destinataire, texte):
        MessageDao().creer(destinataire, texte)
