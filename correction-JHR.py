#   coding: utf-8

### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

### Très bon script qui va bel et bien moissonner des infos dans un site du gouvernement fédéral
### et qui pourrait très bien aller moissonner tous les contrats disponibles en changeant la ligne 48 par for j in range(1,52):
### La seule chose qui manque, c'est de l'adapter aux deux types de contrats qu'on peut rencontrer:
### Les contrats qui sont en fait des modifications à des contrats antérieurs, et ceux qui n'en sont pas
### Les premiers comptent 10 lignes, les autres 7.

### Cela peut être réglé de la façon suivante:
### On change ta ligne 107 par ceci:
### items = pageContrat.find_all("tr")
### Cela crée une liste appelée «items»
### Si la longueur de cette liste, len(items), est égale à 10, c'est qu'on est en présence d'une modification, et là tu vas chercher 10 éléments d'information
### Sinon, c'est un contrat qui contient 7 éléments d'information qu'on peut faire passer à 10 ainsi:
### «Numéro de modification» est égal à zéro
### «Valeur originale du contrat» est égal à la ligne «valeur du contrat»
### Et ce qu'ils appellent «Valeur du modification» (sic!) est égal à 0,00 $

#IMPORT Os : nous sert à supprimer l'ancien fichier csv
import os ### Bonne idée! Pour ne pas être obligée de le supprimer manuellement à chaque essai
import csv
import requests
from bs4 import BeautifulSoup

# D'ABORD, ON CRÉE UNE VARIABLE AVEC NOTRE URL DE DÉPART
url1 = "http://w03.international.gc.ca/dc/index_fa-ae.aspx?lang=fra&p=2&r=51"

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


# OS.REMOVE() SUPPRIME LE FICHIER CSV
# os.remove(fich)
achille = open(fich,"a")
talon = csv.writer(achille)
# INSERE NOS ENTETES DANS LA PREMIERE LIGNE DU FICHIER CSV
talon.writerow(["Trimestre 2016-2017","Nom du vendeur", "Numéro de référence", "Date d'attribution du contrat","Devis descriptif",
               "Durée du contrat", "Valeur du contrat", "Commentaires"]);
               

# On cree une boucle pour les URLS des trimestres, on ignore le 2e trimestre, car on a pas reussi a faire marcher
urls=[49,51]
for j in urls :
        # Comme fait precedemment, on recupere le contenu des pages suivantes
        lienTrimestre = "index_fa-ae.aspx?lang=fra&p=3&r=" + str(j) ### Cette ligne et la suivante peuvent être jumelées en une seule
        hyperlienTrimestre = "http://w03.international.gc.ca/dc/" + lienTrimestre
        print(hyperlienTrimestre)
        contenuTrimestre = requests.get(hyperlienTrimestre, headers=entetes)
        pageTrimestre = BeautifulSoup(contenuTrimestre.text, "html.parser")
        
        # On cree une boucle pour recuperer les informations du contrat
        i = 0
        for contrat in pageTrimestre.find_all("tr"):
            print(contrat)
            # SI i == 0, ON EST À LA PREMIÈRE LIGNE, L'ENTÊTE,
            # QUI NE NOUS EST PAS UTILE, ALORS ON L'ESCAMOTE
            if (i != 0):
                # TOUT CE QUI NOUS INTÉRESSE DANS CETTE LIGNE
                # C'EST L'HYPERLIEN VERS LA SOUS-PAGE QUI CONTIENT
                # PLUS D'INFOS SUR LE CONTRAT, ALORS ON RECUEILLE
                # CET HYPERLIEN
                lienContrat = contrat.a.get("href")

        
                # IL N'EST PAS COMPLET, ALORS ON LE COMPLÈTE
                hyperlienContrat = "http://w03.international.gc.ca/dc/" + lienContrat

                # ON RÉPÈTE MAINTENANT NOTRE RECETTE DE SOUPE
                # POUR ALLER CHERCHER LES INFOS RELATIVES AU CONTRAT
                contenuContrat = requests.get(hyperlienContrat, headers=entetes)
                pageContrat = BeautifulSoup(contenuContrat.text, "html.parser")
        
                # ON CRÉE UNE LISTE VIDE DANS LAQUELLE ON VA METTRE
                # LES INFOS RELATIVES AU CONTRAT
                Contrat = [] ### Il est généralement préférable d'éviter de commencer des noms de variables avec une majuscule
        
                # PREMIER ITEM QU'ON MET DANS NOTRE LISTE:
                # L'HYPERLIEN (POUR FAIRE DES VÉRIFICATIONS ULTÉRIEUREMENT)

                # On ajoute le numero de trimestre dans notre CSV
                if(j == 51):
                    StringTrimestre = "3"
                #elif(j == 50):
                #    StringTrimestre = "2"
                elif(j == 49):
                    StringTrimestre = "1"
                
                Contrat.append(StringTrimestre)
                Contrat.append(hyperlienContrat)
        
                # CHAQUE PAGE DE CONTRAT EST UN PETIT TABLEAU
                # ON VA EN CHERCHER TOUS LES ÉLÉMENTS tr QU'ON MET DANS UNE LISTE
                # GRÂCE À .find_all
                # PUIS ON CRÉE UNE AUTRE BOUCLE DANS LAQUELLE VA ALLER CHERCHER
                # CHACUN DES ITEMS DU TABLEAU
                for item in pageContrat.find_all("tr"):
            
                    # IL ARRIVE QUE DES CELLULES DU TABLEAU SOIENT VIDES,
                    # CE QUI FAIT PLANTER NOTRE PROGRAMME
                    # ALORS ON MET LA CONDITION SUIVANTE:
                    # SI LA CELLULE N'EST PAS DU NÉANT («None»), INSÈRE SON CONTENU
                    # DANS NOTRE LISTE contrat
                    if item.td is not None:
                        Contrat.append(item.td.text)
            
                    # SINON (SI C'EST DU NÉANT), AJOUTE «None» À NOTRE LISTE
                    else:
                        Contrat.append(None)
        
        
                # ET COMME ON L'A FAIT AVEC L'API
                # ON INSCRIT NOTRE LISTE CONTRAT DANS UNE NOUVELLE LIGNE
                # D'UN FICHIER CSV
                talon.writerow(Contrat)
        
            # ON AUGMENTE NOTRE COMPTEUR DE 1
            i += 1