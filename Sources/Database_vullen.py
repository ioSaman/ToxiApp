## ---------------------------------------------------------------------------------------------------------------------------------
##    Auteur:       Teuntje Peeters Copyright 2014
##    Datum creatie: juni 2014
##    Versie:        1
##    Functionaliteit:
##    Bestand met stoffen doorlezen, opdelen in kolommen en de namen van de stoffen eruit halen en in een lijst plaatsten.
##    Connecteren met de mySQL connector database.
##    Dan zoekt deze pubmed door op zoek naar de stoffen uit het bestand en slaat deze op in de database.
##    Known bugs: 
## ---------------------------------------------------------------------------------------------------------------------------------

from Bio import Entrez
from Bio import Medline
import os
import mysql.connector

def main():
        Stoffen = Bestand_lezen() #Functie aanroepen om het bestand te lezen. Hier wordt de variabele Stoffen aan meegegeven. 

def Bestand_lezen():
        nieuwe_lijst = []
        bestand = open("Stoffenlijst.txt").readlines()
        for line in bestand:
            regel = line.split("\t")
            lijst = [regel[0].lower()]
            for i in lijst:
                if i not in nieuwe_lijst:
                    nieuwe_lijst.append(i)
        for i in nieuwe_lijst:
            Zoeken(i)
##            stof_invoeren(i, regel[1])
        
def Zoeken(Stoffen):
    try:
        conn = mysql.connector.connect(host = "127.0.0.1",
                                       user = "bi2_pg2",
                                       password = "blaat1234",
                                       db="bi2_pg2")
        
        Entrez.email = 'A.N.Other@example.com'
        MAX_COUNT = 20
        
        h = Entrez.esearch(db='pubmed', retmax=MAX_COUNT, term=Stoffen)
        result = Entrez.read(h)
        
        print('Total number of publications containing {0}: {1}'.format(Stoffen, result['Count']))
        ids = result['IdList']
##        if len(ids) == 0:
##            pass
        
        h = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text')
        records = Medline.parse(h)

        search_results = Entrez.read(Entrez.esearch(db="pubmed",
                                                term=Stoffen,
                                                reldate=365, datetype="pdat",
                                                usehistory="y"))

        count = int(search_results["Count"])

        cursor = conn.cursor ()
        for record in records:
            journal = record.get("TA", "?")
            datum = record.get("DA", "?")
            titel = record.get("TI", "?")
            abstract = record.get("AB", "?")
            Pubmed_ID = record.get("PMID", "?")
            
            add_artikel = ("INSERT INTO Artikel"
                       "(Journal, Datum, Titel, Abstract, Pubmed_ID)"
                       "VALUES(%s, %s, %s, %s, %s)")
            
            data_artikel = (str(journal),str(datum),str(titel),str(abstract),str(Pubmed_ID))
            cursor.execute(add_artikel, data_artikel)
            
        conn.commit()
        cursor.close()
        conn.close()
        print("Artikel toevoegen is gelukt")

    except UnicodeEncodeError:
          print("UnicodeEncodeError")
##    except mysql.connector.errors.IntegrityError:
##        continue
        

def stof_invoeren(Stof, id_nr):
    conn = mysql.connector.connect(host = "127.0.0.1",
                                       user = "bi2_pg2",
                                       password = "blaat1234",
                                       db="bi2_pg2")
    cursor = conn.cursor ()
    
    add_stof = ("INSERT INTO Stof"
                       "(Stof_id, Naam)"
                       "VALUES(%s, %s)")
     
    data_stof = (str(id_nr),str(Stof))
    cursor.execute(add_stof, data_stof)
    conn.commit()
    cursor.close()
    conn.close()
    print("Stof ingevoerd")
    
main()