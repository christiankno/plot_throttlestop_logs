## This file has been replaced by throttle_functions.py
import pandas as pd
import matplotlib.pyplot as plt 
import os
import re

def avg(lst): 
    return sum(lst) / len(lst) 

def get_data0(date,workspace=r'C:\Users\chris\Documents\software\throttleStop\logs\\', rewrite=0):
    p=rewrite
    txtpath=workspace+date+'.txt'
    pklpath=workspace+date+'.pkl'
    tmppath=workspace+'tmp.txt'
    if not os.path.isfile(pklpath) or rewrite:
        with open(txtpath, 'r') as log: lines=log.readlines()
        with open(tmppath,'w+') as log:
            if not lines[0].endswith('LIM'): lines[0]=lines[0].replace('\n','   LIM\n')
            for line in lines: log.write(line)
        data = pd.read_csv(tmppath, sep ='\s+', index_col=False, parse_dates=[['DATE','TIME']])
        rewrite=1
    else: data = pd.read_pickle(pklpath)
    return data, rewrite, pklpath

def myplot(dataf, plot=1, clean=0, L=50,bool_fall=50, save_path=None, plot_bools=1, clean_bool=1, clean_signal=1):
    df=dataf

    TO_PLOT={'MULTI':'green',
            'C0%':'red',
            'TEMP':'blue',
            'GPU':'yellow',
            'VID':'cyan',
            'POWER':'magenta'
            }
    BOOLS={'LIM':'black'}

    MOV_ARR={}
    for signal in TO_PLOT: MOV_ARR[signal]=[]
    df=df.fillna(value=0)

    if clean:
        PL=0
        for i in range(len(df.index)-1):
            if i%100==0: print('i=%s' % i)
            if clean_signal:
                for signal in TO_PLOT:
                    if i<L: MOV_ARR[signal].append(df.loc[i,signal])    # Increase moving array size
                    else: MOV_ARR[signal][i%L]=df.loc[i,signal]         # Replace existing value in moving array
                    df.loc[i,signal]=avg(MOV_ARR[signal])               # Replace value in Dataframe with average

            if re.match(r'(PL1|PL2|100)',str(df.loc[i,'LIM'])) and clean_bool: 
                df.loc[i,'LIM']=100
                PL=bool_fall
            elif PL>0 and clean_bool:
                PL=PL-1
                df.loc[i,'LIM']=100/bool_fall*PL
    
    if save_path is not None: df.to_pickle(save_path)

    if plot:
        ax = plt.gca()
        for signal in TO_PLOT:
            df.plot(kind='line',x='DATE_TIME',y=signal, color=TO_PLOT[signal], ax=ax)
        if plot_bools:
            for signal in BOOLS.keys():
                df.plot(kind='line',x='DATE_TIME',y=signal, color=BOOLS[signal], ax=ax)

        plt.title("log throttlestop")
        plt.legend()
        plt.show()
        print('success')

    return df
