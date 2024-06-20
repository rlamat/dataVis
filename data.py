import pandas as pd
import plotly.express as px
import re
import chardet
from typing import List
import numpy as np



def getDatasFromTDFFinishers():
    file_path = 'tdf_finishers.csv'
    df = pd.read_csv(file_path, header=None)
    # Nommer les colonnes grace à la premiere ligne
    df.columns = df.iloc[0]
    df = df[1:]  # Enlever la première ligne qui contient les noms des colonnes
    # Nettoyer les colonnes si nécessaire
    df['Time'] = df['Time'].str.replace('"', '')
    df['Team'] = df['Team'].str.strip()
    return df


def getDatasFromTDFStages():
    file_path = 'tdf_stages.csv'
    df = pd.read_csv(file_path, header=None)
    # Nommer les colonnes grace à la premiere ligne
    df.columns = df.iloc[0]
    df = df[1:]  # Enlever la première ligne qui contient les noms des colonnes
    df['Distance'] = df['Distance'].str.extract(r'(\d+)').astype(int)
    return df


def extract_distance_km(distance_str):
    match = re.search(r'(\d+) km', distance_str)
    if match:
        return int(match.group(1))
    else:
        return None


def deleteCaracter(string):
    string = string.replace(',', '')
    return string


def getDatasFromTDFTours():
    # Détection de l'encodage du fichier CSV
    with open('tdf_tours.csv', 'rb') as f:
        result = chardet.detect(f.read())

    # Charger le fichier CSV en utilisant l'encodage détecté
    df = pd.read_csv('tdf_tours.csv', encoding=result['encoding'])
    df['Distance'] = df['Distance'].apply(deleteCaracter)
    df['Distance'] = df['Distance'].str.extract(r'(\d+)').astype(int)
    return df


def convert_to_hours_float(time_str):
    match = re.match(r"(\d+)h\s*(\d+)'?\s*(\d+)\"?", time_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        total_hours = hours + minutes / 60 + seconds / 3600
        return total_hours
    else:
        raise ValueError(f"Format de temps invalide : {time_str}")
    
    
def keepOnlyNumberAndSpace(value):
    if isinstance(value, float):
        return str(value)
    return re.sub(r'[^\d\s]', '', value)


def graphNumberOfFinisher(df, startYear, endYear, compareStarters):
    df['Year'] = df['Year'].astype(int)
    df = df.loc[df['Year'] >= startYear]
    df = df.loc[df['Year'] <= endYear]
    df['StartersValid'] = df['Starters'].astype(int) - df['Finishers'].astype(int)
    if (compareStarters):
        fig = px.bar(df, x='Year', y=['Finishers', 'StartersValid'], title='Number of starters and finishers by year')
        fig.update_yaxes(title_text='Total number of participants')
    else:
        fig = px.bar(df, x='Year', y='Finishers', title='Number of finishers by year')
        fig.update_yaxes(title_text='Number of finishers')
    return fig

def graphTheAverageBetweenStartersAndFinishers(dfFinishers, startYear, endYear):
    dfFinishers['Year'] = dfFinishers['Year'].astype(int)
    dfFinishers = dfFinishers.loc[dfFinishers['Year'] >= startYear]
    dfFinishers = dfFinishers.loc[dfFinishers['Year'] <= endYear]
    dfFinishers['Finishers'] = dfFinishers['Finishers'].astype(int)
    dfFinishers['Starters'] = dfFinishers['Starters'].astype(int)
    dfFinishers['Average'] = dfFinishers['Finishers'] / dfFinishers['Starters']
    fig = px.line(dfFinishers, x='Year', y='Average', title='Average between starters and finishers by year')
    fig = fig.update_yaxes(title_text='Average (%)')
    return fig


def graphAverageSpeed(dfFinishers, dfTours, startYear, endYear):
    # Copie du DataFrame dfFinishers pour éviter de modifier l'original
    dfWinners = dfFinishers.copy()
    
    # Assurance que 'Rank' est numérique (converti si nécessaire)
    dfWinners['Rank'] = pd.to_numeric(dfWinners['Rank'], errors='coerce')
    
    # Filtrer
    df_filtered = dfWinners.loc[dfWinners['Rank'] == 1]
    dfWinners = df_filtered[['Year', 'Rider', 'Time']]
    
    # delete the line when the time is null
    dfWinners = dfWinners.dropna(subset=['Time'])
    
    dfWinners['Year'] = dfWinners['Year'].astype(int)
    dfWinners = dfWinners.loc[dfWinners['Year'] >= startYear]
    dfWinners = dfWinners.loc[dfWinners['Year'] <= endYear]
    
    # Convertir les temps en heures
    dfWinners['TimeInHours'] = dfWinners['Time'].apply(convert_to_hours_float)
    
    dfToursFiltered = dfTours[['Year', 'Distance']]
    dfToursFiltered = dfToursFiltered.drop_duplicates(subset='Year')
    dfToursFiltered['Year'] = dfToursFiltered['Year'].astype(int)
    dfWinners['Year'] = dfWinners['Year'].astype(int)
    
    dfWinners = pd.merge(dfWinners, dfToursFiltered, on='Year')
    dfWinners['AverageSpeed'] = dfWinners['Distance'] / dfWinners['TimeInHours']
    
    fig = px.line(dfWinners, x='Year', y='AverageSpeed', title='Average Speed of Tour de France Winners')
    fig.update_yaxes(title_text='Average Speed (km/h)')
    return fig    
    
def convert_to_hours(time_str):
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


def graphTimeOfFirst(dfFinishers, year, getFirst, getSecond, getThird, timeLadder):
    # Copie du DataFrame dfFinishers pour éviter de modifier l'original
    dfTop3 = dfFinishers.copy()
    
    # Assurez-vous que 'Rank' est numérique (convertissez si nécessaire)
    dfTop3['Rank'] = pd.to_numeric(dfTop3['Rank'], errors='coerce')
    
    dfTop3 = dfTop3.loc[dfTop3['Rank'] <= 3]
    if (getFirst == False):
        dfTop3 = dfTop3.loc[dfTop3['Rank'] != 1]
    if (getSecond == False):
        dfTop3 = dfTop3.loc[dfTop3['Rank'] != 2]
    if (getThird == False):
        dfTop3 = dfTop3.loc[dfTop3['Rank'] != 3]
    
    # delete the line when the time is null
    dfTop3 = dfTop3.dropna(subset=['Time'])
    
    # Convertir les temps en heures
    dfTop3['TimeInHours'] = dfTop3['Time'].apply(keepOnlyNumberAndSpace)
    dfTop3Time = dfTop3['Time']
    dfTop3TimeArray = np.array(dfTop3Time, dtype=str)
    taille = len(dfTop3TimeArray)
    firstTime = 0.0
    for i in range(taille):
        if (dfTop3TimeArray[i][0] == '+'):
            length = len(dfTop3TimeArray[i])
            time_str = dfTop3TimeArray[i][2:length]
            time = convert_to_hours(time_str) + firstTime
            dfTop3TimeArray[i] = time
        else:
            time = convert_to_hours(dfTop3TimeArray[i])
            dfTop3TimeArray[i] = time
            firstTime = time
            
    #retransform the array in a dataframe
    dfTop3['TimeInHours'] = dfTop3TimeArray
    dfTop3['TimeInHours'] = dfTop3['TimeInHours'].astype(float)
    
    dfTop3ForOneYear = dfTop3.copy()
    dfTop3ForOneYear['Year'] = dfTop3ForOneYear['Year'].astype(int)
    dfTop3ForOneYear = dfTop3ForOneYear.loc[dfTop3ForOneYear['Year'] == year]
    
    if timeLadder == 'minute':
        dfTop3ForOneYear['TimeInMin'] = dfTop3ForOneYear['TimeInHours'] * 60
        fig = px.bar(dfTop3ForOneYear, x='Rider', y='TimeInMin', color='Rank', title='Time of the first 3 of the Tour de France ' + str(year))
        fig.update_yaxes(range=[dfTop3ForOneYear['TimeInMin'].min()-3, 
                            dfTop3ForOneYear['TimeInMin'].max()+2])
    elif timeLadder == 'second':
        dfTop3ForOneYear['TimeInSec'] = dfTop3ForOneYear['TimeInHours'] * 3600
        fig = px.bar(dfTop3ForOneYear, x='Rider', y='TimeInSec', color='Rank', title='Time of the first 3 of the Tour de France ' + str(year))
        fig.update_yaxes(range=[dfTop3ForOneYear['TimeInSec'].min()-3, 
                            dfTop3ForOneYear['TimeInSec'].max()+2])
    else :
        fig = px.bar(dfTop3ForOneYear, x='Rider', y='TimeInHours', color='Rank', title='Time of the first 3 of the Tour de France ' + str(year))
        fig.update_yaxes(range=[dfTop3ForOneYear['TimeInHours'].min()-3, 
                            dfTop3ForOneYear['TimeInHours'].max()+2])
    return fig


def graphMultilineTimeOfFirst(dfFinishers, startYear, endYear, timeLadder):
    # Copie du DataFrame dfFinishers pour éviter de modifier l'original
    dfTop3 = dfFinishers.copy()
    
    # Assurance que 'Rank' est numérique (converti si nécessaire)
    dfTop3['Rank'] = pd.to_numeric(dfTop3['Rank'], errors='coerce')
    dfTop3 = dfTop3.loc[dfTop3['Rank'] <= 3]
    
    # delete the line when the time is null
    dfTop3 = dfTop3.dropna(subset=['Time'])
    
    # Convertir les temps en heures
    dfTop3['TimeInHours'] = dfTop3['Time'].apply(keepOnlyNumberAndSpace)
    dfTop3Time = dfTop3['Time']
    dfTop3TimeArray = np.array(dfTop3Time, dtype=str)
    taille = len(dfTop3TimeArray)
    firstTime = 0.0
    for i in range(taille):
        if (dfTop3TimeArray[i][0] == '+'):
            length = len(dfTop3TimeArray[i])
            time_str = dfTop3TimeArray[i][2:length]
            time = convert_to_hours(time_str) + firstTime
            dfTop3TimeArray[i] = time
        else:
            time = convert_to_hours(dfTop3TimeArray[i])
            dfTop3TimeArray[i] = time
            firstTime = time
            
    
    #retransform the array in a dataframe
    dfTop3['TimeInHours'] = dfTop3TimeArray
    dfTop3['TimeInHours'] = dfTop3['TimeInHours'].astype(float)
    
    dfTop3ForOneYear = dfTop3.copy()
    dfTop3ForOneYear['Year'] = dfTop3ForOneYear['Year'].astype(int)
    dfTop3ForOneYear = dfTop3ForOneYear.loc[dfTop3ForOneYear['Year'] >= startYear]
    dfTop3ForOneYear = dfTop3ForOneYear.loc[dfTop3ForOneYear['Year'] <= endYear]
    
    if timeLadder == 'minute':
        dfTop3ForOneYear['TimeInMin'] = dfTop3ForOneYear['TimeInHours'] * 60
        fig = px.line(dfTop3ForOneYear, x='Year', y='TimeInMin', color='Rank', title='Time of the first 3 of the Tour de France between ' + str(startYear) + ' and ' + str(endYear))
    elif timeLadder == 'second':
        dfTop3ForOneYear['TimeInSec'] = dfTop3ForOneYear['TimeInHours'] * 3600
        fig = px.line(dfTop3ForOneYear, x='Year', y='TimeInSec', color='Rank', title='Time of the first 3 of the Tour de France between ' + str(startYear) + ' and ' + str(endYear))
    else :
        fig = px.line(dfTop3ForOneYear, x='Year', y='TimeInHours', color='Rank', title='Time of the first 3 of the Tour de France between ' + str(startYear) + ' and ' + str(endYear))
    return fig
