import pandas as pd
import matplotlib.pyplot as plt 
import os
import re

def get_data(date,workspace=r'C:\Users\chris\Documents\software\throttleStop\logs\\', from_txt=0):
    print('Getting Data...')
    txtpath=workspace+date+'.txt'
    pklpath=workspace+date+'.pkl'
    tmppath=workspace+'tmp.txt'
    if not os.path.isfile(pklpath) or from_txt:
        with open(txtpath, 'r') as log: lines=log.readlines()
        with open(tmppath,'w+') as log:
            if not lines[0].strip().endswith('LIM'): lines[0]=lines[0].replace('\n','   LIM\n')
            for line in lines: log.write(line)
        df = pd.read_csv(tmppath, sep ='\s+', index_col=False, parse_dates=[['DATE','TIME']])
        from_txt=1
    else: df = pd.read_pickle(pklpath)
    df=df.fillna(value=0)
    df.loc[df['LIM']!=0, 'LIM']=100
    df=df.groupby(by=['DATE_TIME']).mean().reset_index()
    print('DONE')
    return df


def clean_data(data, cont_signals=dict(), log_signals=dict(), clean_cont=1, clean_log=1, L=50):
    print('Cleaning Data...')
    df=data.fillna(value=0)
    print('Setting string to 100...')
    for signal in log_signals.keys():
        df.loc[df[signal]!=0, signal]=100
    print('Cleaning signals...')
    df_rolled=df.rolling(L, min_periods=1, center=True, win_type='triang').mean()#
    df_rolled.insert(0,'DATE_TIME',df['DATE_TIME'])
    #for signal in cont_signals.keys():
    #    df[signal]=df[signal].rolling(window=L, center=True, min_periods=1).sum()
    #print('Continous Signals Clean')

    #for signal in log_signals.keys():
    #    df[signal]=df[signal].replace('PL2',100).replace('PL1',100)
    #    df.loc[df[signal]==r'(PL1|PL2)', signal]=100 ## AQUI NO SE ME ESTAN CONVIRTIENDO A NUMEROS
    #    df[signal]=df[signal].rolling(L, center=False, win_type='triang', min_periods=1).mean()
    #print('Logic Signals Clean')
    print('DONE')
    return df_rolled

def save_data(df, date='date',workspace=r'C:\Users\chris\Documents\software\throttleStop\logs\\'):
    print('Saving Data...')
    pklpath=workspace+date+'.pkl'
    df.to_pickle(pklpath)
    print('DONE')
    return

def plot_data(df, cont_signals=dict(), log_signals=dict()):
    print('Plotting Data...')
    ax = plt.gca()
    for signal in cont_signals.keys():
        df.plot(kind='line',x='DATE_TIME',y=signal, color=cont_signals[signal], ax=ax)
    for signal in log_signals.keys():
        df.plot(kind='line',x='DATE_TIME',y=signal, color=log_signals[signal], ax=ax)

    plt.title("log throttlestop")
    plt.legend(loc='upper right')
    plt.show()
    print('DONE')
    return