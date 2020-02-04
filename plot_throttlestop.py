
import pandas as pd
import matplotlib.pyplot as plt 
from functions import *
from throttle_functions import *
import os


def plot_log(date):
    sig_dict={'MULTI':'green',
                'C0%':'red',
                'TEMP':'blue',
                'GPU':'purple',
                'VID':'cyan',
                'POWER':'magenta'
                }
    log_dict={'LIM':'brown'
              }

    log_data=get_data(date, from_txt=1)
    log_data=clean_data(log_data, 
                      cont_signals=sig_dict, 
                      log_signals=log_dict, 
                      L=300)

    save_data(log_data, date=date)
    plot_data(log_data, cont_signals=sig_dict, log_signals=log_dict)


date='2020-02-02'
plot_log(date)


# used to lower the sample rate, but LIM has to be processed before this step, or else it gets removed and an error comes up
#log_df_groupby=log_df.groupby(by=['DATE_TIME'])
#log_df_mean=log_df_groupby.mean()
#log_df2=log_df_mean.reset_index()