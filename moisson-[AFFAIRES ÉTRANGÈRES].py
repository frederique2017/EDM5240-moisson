#   coding: utf-8


#IMPORT Os : nous sert à enlever l'ancien contenu du fichier csv
import os
import csv
import requests
from bs4 import BeautifulSoup

# D'ABORD, ON CRÉE UNE VARIABLE AVEC NOTRE URL DE DÉPART
url1 = "http://w03.international.gc.ca/dc/index_fa-ae.aspx?lang=fra&p=3&r=51"

# ON CRÉÉ AUSSI UNE VARIABLE AVEC LE NOM DE NOTRE FUTUR FICHIER CSV
# DANS LEQUEL ON VA CONFINER LE RÉSULTAT DE NOTRE MOISSON
fich = "affaires-etrangeres.csv"

# ICI AUSSI, ON EST POLI
entetes = {
    "User-Agent":"Je m'appelle Frederique Tavernier je suis dans un cours de journalisme web",
    "From":"frederique.tavernierlabrie@gmail.com"  
}

# ON DEMANDE ENSUITE À REQUESTS D'ÉTABLIR UNE CONNEXION AVEC CET URL
# ET DE PLACER LE CONTENU DANS UNE VARIABLE QU'ON VA APPELER, METTONS, contenu
contenu = requests.get(url1, headers=entetes)

# PUIS, ON DEMANDE À BEAUTIFULSOUP DE PRENDRE LE TEXTE DE CE CONTENU,
# DU TEXTE HTML, ET DE LE «PARSER» (L'ANALYSER), ET DE METTRE LE RÉSULTAT
# DE CETTE ANALYSE DANS UNE VARIABLE QU'ON VA APPELER page
page = BeautifulSoup(contenu.text,"html.parser")

# ON CRÉE UN COMPTEUR POUR ÉVITER DE RAMASSER L'INFO
# DES ENTÊTES DE TABLEAU
i = 0

# OS.REMOVE() ENLEVE L'ANCIEN CONTENU DU FICHIER CSV
os.remove(fich)
achille = open(fich,"a")
talon = csv.writer(achille)
# INSERE NOS ENTETES DANS LA PREMIERE LIGNE DU FICHIER CSV
talon.writerow(["Nom du vendeur", "Numéro de référence", "Date d'attribution du contrat","Devis descriptif",
               "Durée du contrat", "Valeur du contrat", "Commentaires"]);

# L'INFO QU'ON CHERCHE EST DANS UN IMMENSE TABLEAU
# CHAQUE LIGNE DE CE TABLEAU EST DANS UN ÉLÉMENT HTML <tr>
# ON UTILISE .find_all POUR LES RÉUNIR TOUS DANS UNE IMMENSE LISTE
# ON UTILISE UNE BOUCLE POUR CONSULTER CHACUN DES ÉLÉMENTS DE CETTE LISTE
for ligne in page.find_all("tr"):
    
    # SI i == 0, ON EST À LA PREMIÈRE LIGNE, L'ENTÊTE,
    # QUI NE NOUS EST PAS UTILE, ALORS ON L'ESCAMOTE
    if (i != 0):
        # TOUT CE QUI NOUS INTÉRESSE DANS CETTE LIGNE
        # C'EST L'HYPERLIEN VERS LA SOUS-PAGE QUI CONTIENT
        # PLUS D'INFOS SUR LE CONTRAT, ALORS ON RECUEILLE
        # CET HYPERLIEN
        lien = ligne.a.get("href")

        
        # IL N'EST PAS COMPLET, ALORS ON LE COMPLÈTE
        hyperlien = "http://w03.international.gc.ca/dc/" + lien

        # ON RÉPÈTE MAINTENANT NOTRE RECETTE DE SOUPE
        # POUR ALLER CHERCHER LES INFOS RELATIVES AU CONTRAT
        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
        # ON CRÉE UNE LISTE VIDE DANS LAQUELLE ON VA METTRE
        # LES INFOS RELATIVES AU CONTRAT
        contrat = []
        
        # PREMIER ITEM QU'ON MET DANS NOTRE LISTE:
        # L'HYPERLIEN (POUR FAIRE DES VÉRIFICATIONS ULTÉRIEUREMENT)
        contrat.append(hyperlien)
        
        # CHAQUE PAGE DE CONTRAT EST UN PETIT TABLEAU
        # ON VA EN CHERCHER TOUS LES ÉLÉMENTS tr QU'ON MET DANS UNE LISTE
        # GRÂCE À .find_all
        # PUIS ON CRÉE UNE AUTRE BOUCLE DANS LAQUELLE VA ALLER CHERCHER
        # CHACUN DES ITEMS DU TABLEAU
        for item in page2.find_all("tr"):
            
            # IL ARRIVE QUE DES CELLULES DU TABLEAU SOIENT VIDES,
            # CE QUI FAIT PLANTER NOTRE PROGRAMME
            # ALORS ON MET LA CONDITION SUIVANTE:
            # SI LA CELLULE N'EST PAS DU NÉANT («None»), INSÈRE SON CONTENU
            # DANS NOTRE LISTE contrat
            if item.td is not None:
                contrat.append(item.td.text)
            
            # SINON (SI C'EST DU NÉANT), AJOUTE «None» À NOTRE LISTE
            else:
                contrat.append(None)
        
        
        # ET COMME ON L'A FAIT AVEC L'API
        # ON INSCRIT NOTRE LISTE CONTRAT DANS UNE NOUVELLE LIGNE
        # D'UN FICHIER CSV
        talon.writerow(contrat)
        
    # ON AUGMENTE NOTRE COMPTEUR DE 1
    i += 1