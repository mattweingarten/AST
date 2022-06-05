import sys
import numpy as np
import pandas as pd
import seaborn as sns;
import matplotlib
import matplotlib.pyplot as plt
from util import *




def save_df_as_image(df, path):

    norm = matplotlib.colors.Normalize(-1,1)

    plot = sns.heatmap(df, annot=True,cmap='Blues', cbar=False, fmt="d",linewidths=.5, annot_kws={"fontsize":8})
    # plot = sns.heatmap(df,cmap='Blues', cbar=True,linewidths=.5, vmin=0.0, vmax = 1.0)
    fig = plot.get_figure()
    plot.xaxis.set_label_position('top') 
    plt.gcf().subplots_adjust(bottom=0.25, left=0.25)
    fig.savefig(path)


    
if(len(sys.argv) != 3):
    print("Add param and json config to data file")

bench_json = get_exp_json(sys.argv[2])



df = pd.read_csv(sys.argv[1])
df['fuzzer'] = df['fuzzer'].apply(lambda x : cut_fuzz_name(x))

df['benchmark'] = df['benchmark'].apply(lambda x : get_benchmark(x, bench_json['benchmarks']))

df = df.pivot(index='fuzzer', columns= 'benchmark',values='edges' )
df = df.fillna(0).astype(int)

df['total'] = df.sum(axis=1)

print(df)

save_df_as_image(df, "./plots/total_unique_edges.svg")