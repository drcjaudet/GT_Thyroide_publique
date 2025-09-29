```python
import pandas

def ExtractTimeFrame(variable):
    vec=[]
    vec.append(variable.year)
    vec.append(variable.month)
    vec.append(variable.day)
    #vec.append(variable.hour)
    #vec.append(variable.minute)
    #vec.append(variable.second)
    return vec

def ChangeTimeFormat(variable):
    YYMMDD=(variable.year)*10000+variable.month*100+variable.day
    return YYMMDD

# Concatenation des deux fichiers excel avant analyse stat:
def ChangeTimeFormat(variable):
    YYMMDD=(variable.year-2000)*10000+variable.month*100+variable.day
    return YYMMDD

def main(adresse_receuil, adresse_analyseImage, adresse_resultat):
    # importation des données, un csv pour le receuil et un csv pour les données images
    df_recueil = pandas.read_csv(adresse_receuil, header=0, sep=";", encoding="ISO-8859-1")
    df_analyseImage = pandas.read_csv(adresse_analyseImage, header=0, sep=";")
    # mélange des deux tableaux en triant à partir de la colonne de nom
    tableau_donnee = pandas.merge(df_recueil, df_analyseImage, on="Nom_Fichier_DICOM", validate="many_to_one")
    # calcul de la sensibilité
    Sensibilite_cols = [col for col in tableau_donnee.columns if '(Cps/(MBq.s))' in col]
    Coups_cols = [col for col in tableau_donnee.columns if 'Coups Totaux(kCps)_F' in col]
    for i in range(len(Sensibilite_cols)-1):
        tableau_donnee[Sensibilite_cols[i]] = tableau_donnee[Coups_cols[i]] * 1000 / (tableau_donnee['A_acq_corr'] * tableau_donnee['ActualFrameDuration (s)'])
    # calcul pour SAM
    tableau_donnee.iloc[:,-1] = tableau_donnee.iloc[:,-2] * 1000 / (tableau_donnee['A_acq_corr'] * tableau_donnee['ActualFrameDuration (s)'])
    # sauvegarde des données dans un csv
    tableau_donnee.to_csv(adresse_resultat, header=True, sep=';')

# Exemple d'utilisation (à adapter selon vos chemins de fichiers)
# adresse_receuil = "/content/Recueil_global_V12_nettoyage2.csv"
# adresse_analyseImage = "/content/ExtractionImageData_23032022.csv"
# adresse_resultat = "/content/mergeTab.csv"
# main(adresse_receuil, adresse_analyseImage, adresse_resultat)
```
