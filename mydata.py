import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
pd.options.display.float_format = "{:,.2f}".format

import xlwt
import numpy as np
from dash import Dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# ----------------------------------------------------------------------------------------------------------------------
# excel to dataframe
# dff = pd.read_excel(r'E:\tesi\tesi\apps\files\1.xls', index_col=0, header=0, sheet_name="Risultati")
# df1 = pd.read_excel(r'E:\tesi\tesi\apps\files\2.xls', index_col=0, header=0, sheet_name="Risultati")
# df2 = pd.read_excel(r'E:\tesi\tesi\apps\files\3.xls', index_col=0, header=0, sheet_name="Risultati")
# df3 = pd.read_excel(r'E:\tesi\tesi\apps\files\4.xls', index_col=0, header=0, sheet_name="Risultati")
# df4 = pd.read_excel(r'E:\tesi\tesi\apps\files\5.xls', index_col=0, header=0, sheet_name="Risultati")
# df5 = pd.read_excel(r'E:\tesi\tesi\apps\files\6.xls', index_col=0, header=0, sheet_name="Risultati")
# df6 = pd.read_excel(r'E:\tesi\tesi\apps\files\7.xls', index_col=0, header=0, sheet_name="Risultati")
# df7 = pd.read_excel(r'E:\tesi\tesi\apps\files\8.xls', index_col=0, header=0, sheet_name="Risultati")
# df8 = pd.read_excel(r'E:\tesi\tesi\apps\files\9.xls', index_col=0, header=0, sheet_name="Risultati")
# df9 = pd.read_excel(r'E:\tesi\tesi\apps\files\10.xls', index_col=0, header=0, sheet_name="Risultati")
# df10 = pd.read_excel(r'E:\tesi\tesi\apps\files\11.xls', index_col=0, header=0, sheet_name="Risultati")
# df11 = pd.read_excel(r'E:\tesi\tesi\apps\files\12.xls', index_col=0, header=0, sheet_name="Risultati")
# df12 = pd.read_excel(r'E:\tesi\tesi\apps\files\13.xls', index_col=0, header=0, sheet_name="Risultati")
# df13 = pd.read_excel(r'E:\tesi\tesi\apps\files\14.xls', index_col=0, header=0, sheet_name="Risultati")
# df14 = pd.read_excel(r'E:\tesi\tesi\apps\files\15.xls', index_col=0, header=0, sheet_name="Risultati")
# df15 = pd.read_excel(r'E:\tesi\tesi\apps\files\16.xls', index_col=0, header=0, sheet_name="Risultati")
# df16 = pd.read_excel(r'E:\tesi\tesi\apps\files\17.xls', index_col=0, header=0, sheet_name="Risultati")
# df17 = pd.read_excel(r'E:\tesi\tesi\apps\files\18.xls', index_col=0, header=0, sheet_name="Risultati")
# df18 = pd.read_excel(r'E:\tesi\tesi\apps\files\19.xls', index_col=0, header=0, sheet_name="Risultati")
# df19 = pd.read_excel(r'E:\tesi\tesi\apps\files\20.xls', index_col=0, header=0, sheet_name="Risultati")
# df20 = pd.read_excel(r'E:\tesi\tesi\apps\files\21.xls', index_col=0, header=0, sheet_name="Risultati")
# df21 = pd.read_excel(r'E:\tesi\tesi\apps\files\22.xls', index_col=0, header=0, sheet_name="Risultati")
# df22 = pd.read_excel(r'E:\tesi\tesi\apps\files\23.xls', index_col=0, header=0, sheet_name="Risultati")
# df23 = pd.read_excel(r'E:\tesi\tesi\apps\files\24.xls', index_col=0, header=0, sheet_name="Risultati")
# df24 = pd.read_excel(r'E:\tesi\tesi\apps\files\25.xls', index_col=0, header=0, sheet_name="Risultati")
# df25 = pd.read_excel(r'E:\tesi\tesi\apps\files\26.xls', index_col=0, header=0, sheet_name="Risultati")
# df26 = pd.read_excel(r'E:\tesi\tesi\apps\files\27.xls', index_col=0, header=0, sheet_name="Risultati")
# df27 = pd.read_excel(r'E:\tesi\tesi\apps\files\28.xls', index_col=0, header=0, sheet_name="Risultati")
# df28 = pd.read_excel(r'E:\tesi\tesi\apps\files\29.xls', index_col=0, header=0, sheet_name="Risultati")
# df29 = pd.read_excel(r'E:\tesi\tesi\apps\files\30.xls', index_col=0, header=0, sheet_name="Risultati")
# df30 = pd.read_excel(r'E:\tesi\tesi\apps\files\31.xls', index_col=0, header=0, sheet_name="Risultati")
# df31 = pd.read_excel(r'E:\tesi\tesi\apps\files\32.xls', index_col=0, header=0, sheet_name="Risultati")
# df32 = pd.read_excel(r'E:\tesi\tesi\apps\files\33.xls', index_col=0, header=0, sheet_name="Risultati")
# df33 = pd.read_excel(r'E:\tesi\tesi\apps\files\34.xls', index_col=0, header=0, sheet_name="Risultati")
# df34 = pd.read_excel(r'E:\tesi\tesi\apps\files\35.xls', index_col=0, header=0, sheet_name="Risultati")
# df35 = pd.read_excel(r'E:\tesi\tesi\apps\files\36.xls', index_col=0, header=0, sheet_name="Risultati")
# df36 = pd.read_excel(r'E:\tesi\tesi\apps\files\37.xls', index_col=0, header=0, sheet_name="Risultati")
# df37 = pd.read_excel(r'E:\tesi\tesi\apps\files\38.xls', index_col=0, header=0, sheet_name="Risultati")
# df38 = pd.read_excel(r'E:\tesi\tesi\apps\files\39.xls', index_col=0, header=0, sheet_name="Risultati")
# df39 = pd.read_excel(r'E:\tesi\tesi\apps\files\40.xls', index_col=0, header=0, sheet_name="Risultati")
# df40 = pd.read_excel(r'E:\tesi\tesi\apps\files\41.xls', index_col=0, header=0, sheet_name="Risultati")
# df41 = pd.read_excel(r'E:\tesi\tesi\apps\files\42.xls', index_col=0, header=0, sheet_name="Risultati")
# df42 = pd.read_excel(r'E:\tesi\tesi\apps\files\43.xls', index_col=0, header=0, sheet_name="Risultati")
# df43 = pd.read_excel(r'E:\tesi\tesi\apps\files\44.xls', index_col=0, header=0, sheet_name="Risultati")
# df44 = pd.read_excel(r'E:\tesi\tesi\apps\files\45.xls', index_col=0, header=0, sheet_name="Risultati")
# df45 = pd.read_excel(r'E:\tesi\tesi\apps\files\46.xls', index_col=0, header=0, sheet_name="Risultati")
# df46 = pd.read_excel(r'E:\tesi\tesi\apps\files\47.xls', index_col=0, header=0, sheet_name="Risultati")
# df47 = pd.read_excel(r'E:\tesi\tesi\apps\files\48.xls', index_col=0, header=0, sheet_name="Risultati")
# df48 = pd.read_excel(r'E:\tesi\tesi\apps\files\49.xls', index_col=0, header=0, sheet_name="Risultati")
# df49 = pd.read_excel(r'E:\tesi\tesi\apps\files\50.xls', index_col=0, header=0, sheet_name="Risultati")
# df50 = pd.read_excel(r'E:\tesi\tesi\apps\files\51.xls', index_col=0, header=0, sheet_name="Risultati")
# df51 = pd.read_excel(r'E:\tesi\tesi\apps\files\52.xls', index_col=0, header=0, sheet_name="Risultati")
# df52 = pd.read_excel(r'E:\tesi\tesi\apps\files\53.xls', index_col=0, header=0, sheet_name="Risultati")
# df53 = pd.read_excel(r'E:\tesi\tesi\apps\files\54.xls', index_col=0, header=0, sheet_name="Risultati")
#


# create a single dataframe made by all dataframes
# dff = dff.append(df1, ignore_index=True)
# dff = dff.append(df2, ignore_index=True)
# dff = dff.append(df3, ignore_index=True)
# dff = dff.append(df4, ignore_index=True)
# dff = dff.append(df5, ignore_index=True)
# dff = dff.append(df6, ignore_index=True)
# dff = dff.append(df7, ignore_index=True)
# dff = dff.append(df8, ignore_index=True)
# dff = dff.append(df9, ignore_index=True)
# dff = dff.append(df10, ignore_index=True)
# dff = dff.append(df11, ignore_index=True)
# dff = dff.append(df12, ignore_index=True)
# dff = dff.append(df13, ignore_index=True)
# dff = dff.append(df14, ignore_index=True)
# dff = dff.append(df15, ignore_index=True)
# dff = dff.append(df16, ignore_index=True)
# dff = dff.append(df17, ignore_index=True)
# dff = dff.append(df18, ignore_index=True)
# dff = dff.append(df19, ignore_index=True)
# dff = dff.append(df20, ignore_index=True)
# dff = dff.append(df21, ignore_index=True)
# dff = dff.append(df22, ignore_index=True)
# dff = dff.append(df23, ignore_index=True)
# dff = dff.append(df24, ignore_index=True)
# dff = dff.append(df25, ignore_index=True)
# dff = dff.append(df26, ignore_index=True)
# dff = dff.append(df27, ignore_index=True)
# dff = dff.append(df28, ignore_index=True)
# dff = dff.append(df29, ignore_index=True)
# dff = dff.append(df30, ignore_index=True)
# dff = dff.append(df31, ignore_index=True)
# dff = dff.append(df32, ignore_index=True)
# dff = dff.append(df33, ignore_index=True)
# dff = dff.append(df34, ignore_index=True)
# dff = dff.append(df35, ignore_index=True)
# dff = dff.append(df36, ignore_index=True)
# dff = dff.append(df37, ignore_index=True)
# dff = dff.append(df38, ignore_index=True)
# dff = dff.append(df39, ignore_index=True)
# dff = dff.append(df40, ignore_index=True)
# dff = dff.append(df41, ignore_index=True)
# dff = dff.append(df42, ignore_index=True)
# dff = dff.append(df43, ignore_index=True)
# dff = dff.append(df44, ignore_index=True)
# dff = dff.append(df45, ignore_index=True)
# dff = dff.append(df46, ignore_index=True)
# dff = dff.append(df47, ignore_index=True)
# dff = dff.append(df48, ignore_index=True)
# dff = dff.append(df49, ignore_index=True)
# dff = dff.append(df50, ignore_index=True)
# dff = dff.append(df51, ignore_index=True)
# dff = dff.append(df52, ignore_index=True)
# dff = dff.append(df53, ignore_index=True)



# print("df: ", len(dff))

# ----------------------------------------------------------------------------------------------------------------------
# save and load df
# dff = pd.read_csv(r'E:\tesi\tesi\apps\files\data.csv')

# dff.to_csv(r'E:\tesi\tesi\apps\files\data.csv', index=False)
# #
# df = dff.copy()  # dataframe copy, i'm gonna use this in my calculations
# print(len(df))
# ----------------------------------------------------------------------------------------------------------------------
# CLEAR DATA
# dff = pd.read_csv(r'E:\tesi\tesi\apps\files\data.csv')
# df = dff.copy()
# print(len(df))
#
# df.drop(df.loc[df['Ragione sociale'] == ""].index, inplace=True)
# df.drop(df.loc[df['Partita IVA'] == 0].index, inplace=True)
# df.drop(df.loc[df['ATECO 2007\ncodice'] == 0].index, inplace=True)
# df.drop(df.loc[df['ATECO 2007\ndescrizione'] == ""].index, inplace=True)
# df.drop(df.loc[df['Indirizzo sede legale - Latitudine'] == ""].index, inplace=True)
# df.drop(df.loc[df['Indirizzo sede legale - Longitudine'] == ""].index, inplace=True)
# df.drop(df.loc[df['Ricavi delle vendite\nEUR\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Ricavi delle vendite\nEUR\n2019'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Ricavi delle vendite\nEUR\n2018'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Ricavi delle vendite\nEUR\n2017'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Ricavi delle vendite\nEUR\n2016'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Denaro in cassa\nEUR\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['DEBITI A BREVE\nEUR\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Indice di indebitam. a breve\n%\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Indice di indebitam. a lungo\n%\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Posizione finanziaria netta\nEUR\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Redditività di tutto il capitale investito (ROI) (%)\n%\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['Redditività di tutto il capitale investito (ROI) (%)\n%\n2020'] == "n.s."].index, inplace=True)
# df.drop(df.loc[df['EBITDA/Vendite (%)\n%\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['EBITDA/Vendite (%)\n%\n2020'] == "n.s."].index, inplace=True)
# df.drop(df.loc[df['EBITDA\nEUR\n2020'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['EBITDA\nEUR\n2019'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['EBITDA\nEUR\n2018'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['EBITDA\nEUR\n2017'] == "n.d."].index, inplace=True)
# df.drop(df.loc[df['EBITDA\nEUR\n2016'] == "n.d."].index, inplace=True)
#
# df.reset_index(inplace=True)
# df.drop("index", axis=1, inplace=True)
#
# print(len(df))
# df.to_csv(r'E:\tesi\tesi\apps\files\dataClean.csv', index=False)

# ----------------------------------------------------------------------------------------------------------------------
# QUANDO TUTTI EXCEL SONO CARICATI E CONVERTITI IN CSV USO QUESTO
dff = pd.read_csv(r'E:\tesi\tesi\apps\files\dataClean.csv')
df = dff.copy()
# df.to_excel(r'E:\tesi\tesi\apps\files\allDatas.xlsx', index = False, header=True)
# print("created (^-^)")

# count --> numero aziende in ateco                                              FATTO
# mean --> ROI                                                                   FATTO
# mean --> Ricavi delle vendite\nEUR\n2020,19,18,17,16
# sottraz --> 20-19, 19-18, 18-17, 17-16  --> trovo modo di considerare anno
# mean ascendente --> indice indebitam breve e lungo LEAVERAGE
# HHI --> NAH

atecoUnique = df.groupby(
    ['ATECO 2007\ncodice', 'ATECO 2007\ndescrizione'], as_index=False).agg(
    {'ATECO 2007\ncodice': 'count',
     'Redditività di tutto il capitale investito (ROI) (%)\n%\n2020': 'mean'}
)
atecoUnique.columns = ['ATECO', 'num aziende', 'ROI medio']
#print(atecoUnique)


def main():
    pass


if __name__ == "__main__":
    main()
