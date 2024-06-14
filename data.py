import pandas as pd
import plotly.express as px
import re
import chardet
from typing import List
import numpy as np


lastTime = 0


def getDatasFromTDFFinishers():

    # Lire le fichier CSV
    file_path = 'tdf_finishers.csv'
    df = pd.read_csv(file_path, header=None)

    # Nommer les colonnes grace à la premiere ligne
    df.columns = df.iloc[0]
    df = df[1:]  # Enlever la première ligne qui contient les noms des colonnes

    # Nettoyer les colonnes si nécessaire
    df['Time'] = df['Time'].str.replace('"', '')  # Enlever les guillemets des temps
    df['Team'] = df['Team'].str.strip()  # Enlever les espaces en trop dans les noms des équipes

    # Afficher les premières lignes pour vérifier
    #print(df.head())

    return df


def getDatasFromTDFStages():
    # Lire le fichier CSV
    file_path = 'tdf_stages.csv'
    df = pd.read_csv(file_path, header=None)

    # Nommer les colonnes grace à la premiere ligne
    df.columns = df.iloc[0]
    df = df[1:]  # Enlever la première ligne qui contient les noms des colonnes

    # Extraire le nombre de kilomètres de la colonne Distance et convertir en int
    df['Distance'] = df['Distance'].str.extract(r'(\d+)').astype(int)
 
    # Afficher les premières lignes pour vérifier
    #print(df.head())
    
    return df


def extract_distance_km(distance_str):
    # Utiliser une expression régulière pour extraire le nombre de kilomètres
    match = re.search(r'(\d+) km', distance_str)
    if match:
        return int(match.group(1))
    else:
        return None  # Gestion du cas où la distance n'est pas trouvée


def deleteCaracter(string):
    string = string.replace(',', '')
    return string


def getDatasFromTDFTours():
    # Lire le fichier CSV
    # Détection de l'encodage du fichier CSV
    with open('tdf_tours.csv', 'rb') as f:
        result = chardet.detect(f.read())

    # Charger le fichier CSV en utilisant l'encodage détecté
    df = pd.read_csv('tdf_tours.csv', encoding=result['encoding'])
     
    # Appliquer la fonction extract_distance_km à la colonne 'Distance'
    df['Distance'] = df['Distance'].apply(deleteCaracter)
    df['Distance'] = df['Distance'].str.extract(r'(\d+)').astype(int)

    # Afficher les premières lignes pour vérifier
    #print(df.head())

    return df


def convert_to_hours_float(time_str):
    # Utiliser une expression régulière pour extraire heures, minutes et secondes
    match = re.match(r"(\d+)h\s*(\d+)'?\s*(\d+)\"?", time_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        # Convertir en heures
        total_hours = hours + minutes / 60 + seconds / 3600
        return total_hours
    else:
        raise ValueError(f"Format de temps invalide : {time_str}")
    
    
def keepOnlyNumberAndSpace(value):
    # Vérifier si la valeur est un float
    if isinstance(value, float):
        return str(value)  # Convertir le float en chaîne de caractères
    
    # Utiliser une expression régulière pour garder uniquement les chiffres et les espaces
    return re.sub(r'[^\d\s]', '', value)


def graphNumberOfFinisher(df, startYear, endYear, compareStarters):
    #draw a graph who show the number of finishers by year
    #for each year count tne number of Rider where there is a value in the column 'Time'
    df['Year'] = df['Year'].astype(int)
    df = df.loc[df['Year'] >= startYear]
    df = df.loc[df['Year'] <= endYear]
    print(df)
    #do a graph with the number of starters and finishers by year
    if (compareStarters):
        fig = px.bar(df, x='Year', y=['Finishers', 'Starters'], title='Number of starters and finishers by year')
    else:
        fig = px.bar(df, x='Year', y='Finishers', title='Number of finishers by year')
    #fig.show()
    return fig


def graphAverageSpeed(dfFinishers, dfTours):
    # Copie du DataFrame dfFinishers pour éviter de modifier l'original
    dfWinners = dfFinishers.copy()
    
    # Assurez-vous que 'Rank' est numérique (convertissez si nécessaire)
    dfWinners['Rank'] = pd.to_numeric(dfWinners['Rank'], errors='coerce')
    
    # Filtrer les lignes où 'Rank' est égal à 1
    df_filtered = dfWinners.loc[dfWinners['Rank'] == 1]
    
    # Sélectionner les colonnes pertinentes (Year, Rider, Time)
    dfWinners = df_filtered[['Year', 'Rider', 'Time']]
    
    # delete the line when the time is null
    dfWinners = dfWinners.dropna(subset=['Time'])
    
    # Convertir les temps en heures
    dfWinners['TimeInHours'] = dfWinners['Time'].apply(convert_to_hours_float)
    
    dfToursFiltered = dfTours[['Year', 'Distance']]
    dfToursFiltered = dfToursFiltered.drop_duplicates(subset='Year')
    dfToursFiltered['Year'] = dfToursFiltered['Year'].astype(int)
    dfWinners['Year'] = dfWinners['Year'].astype(int)
    
    # Merge les deux dataframes
    dfWinners = pd.merge(dfWinners, dfToursFiltered, on='Year')
    
    # distance moyenne
    dfWinners['AverageSpeed'] = dfWinners['Distance'] / dfWinners['TimeInHours']
    
    # Afficher le résultat pour vérification
    print(dfWinners)
    
    #draw a graph who show the average speed by year
    fig = px.line(dfWinners, x='Year', y='AverageSpeed', title='Average Speed of Tour de France Winners')
    fig.show()
    
    
def convert_to_hours(time_str):
    # match = re.match(r"(\d+)h\s*(\d+)'?\s*(\d+)\"?", time_str)
    match = re.match(r"(?:(\d+)h\s*)?(?:(\d+)'\s*)?(\d+)\"?", time_str)
    hours = 0
    minutes = 0
    seconds = 0
    if match:
        if match.group(1):
            hours = int(match.group(1))
        if match.group(2):
            minutes = int(match.group(2))
        if match.group(3):
            seconds = int(match.group(3))
        total_hours = hours + minutes / 60 + seconds / 3600
        return total_hours
    else:
        return 0.0


def graphTimeOfFirst(dfFinishers, year=1913):
    # Copie du DataFrame dfFinishers pour éviter de modifier l'original
    dfTop3 = dfFinishers.copy()
    
    # Assurez-vous que 'Rank' est numérique (convertissez si nécessaire)
    dfTop3['Rank'] = pd.to_numeric(dfTop3['Rank'], errors='coerce')
    
    # Filtrer les lignes où 'Rank' est égal à 1
    dfTop3 = dfTop3.loc[dfTop3['Rank'] <= 3]
    
    # delete the line when the time is null
    dfTop3 = dfTop3.dropna(subset=['Time'])
    
    # Convertir les temps en heures
    dfTop3['TimeInHours'] = dfTop3['Time'].apply(keepOnlyNumberAndSpace)
    #dfTop3['Test'] = dfTop3['TimeInHours'].apply(convert_to_hours)d
    dfTop3Time = dfTop3['Time']
    dfTop3TimeArray = np.array(dfTop3Time, dtype=str)
    taille = len(dfTop3TimeArray)
    firstTime = 0.0
    #for time in dfTop3['Time']:
        #if (time[0] == '+'):
            #time = deleteCaracter(time)
            #time = convert_to_hours(time) + firstTime
            #dfTop3['TimeInHours'] = time
        #else:
            #time = convert_to_hours(time)
            #firstTime = time
            #dfTop3['TimeInHours'] = time
    for i in range(taille):
        if (dfTop3TimeArray[i][0] == '+'):
            length = len(dfTop3TimeArray[i])
            time_str = dfTop3TimeArray[i][2:length]
            #print("")
            #print("temps :", time_str)
            #print("convertion : ", convert_to_hours(time_str))
            #print("temps premier : ", firstTime)
            time = convert_to_hours(time_str) + firstTime
            dfTop3TimeArray[i] = time
            #print(time)
            
        else:
            #print("")
            time = convert_to_hours(dfTop3TimeArray[i])
            dfTop3TimeArray[i] = time
            #print(time)
            firstTime = time
            
    #retransform the array in a dataframe
    dfTop3['TimeInHours'] = dfTop3TimeArray
    dfTop3['TimeInHours'] = dfTop3['TimeInHours'].astype(float)
    
    dfTop3ForOneYear = dfTop3.copy()
    dfTop3ForOneYear['Year'] = dfTop3ForOneYear['Year'].astype(int)
    dfTop3ForOneYear = dfTop3ForOneYear.loc[dfTop3ForOneYear['Year'] == year]
    
    print(dfTop3ForOneYear)
    #draw a bar graph who show the time of the first 3 by year, the y origin is 0
    fig = px.bar(dfTop3ForOneYear, x='Rider', y='TimeInHours', color='Rank', title='Time of the first 3 of the Tour de France ' + str(year))
    #set the y origin to 0
    fig.update_yaxes(range=[dfTop3ForOneYear['TimeInHours'].min()-3, 
                            dfTop3ForOneYear['TimeInHours'].max()+2])
    fig.show()

  
dfFinishers = getDatasFromTDFFinishers()
dfStages = getDatasFromTDFStages()
dfTours = (getDatasFromTDFTours())