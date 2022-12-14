'''
Module message_service
Auteurs : L.Deneuville, J-F.Parriaud, J.Torres, H.Wispelaere, B.Zhang
Date    : 20/09/2022
Licence : Domaine public
Version : 1.0
'''

from dao.message_dao import MessageDao


class MessageService:
    '''Classe des services messages

    Attributes
    ----------
    None

    Methods
    -------
    creer(destinataire : Joueur, texte : str) : None
    '''

    def creer(self, destinataire, texte):
        '''Creation d'un message

        Parameters
        ----------
        destinataire : Joueur
            joueur qui reçoit le message
        text : str
            contenu du message

        Returns
        -------
        None
        '''
        MessageDao().creer(destinataire, texte)
