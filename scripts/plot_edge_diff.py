import sys
import numpy as np
import pandas as pd
import seaborn as sns;
import matplotlib
import matplotlib.pyplot as plt
from util import *

def save_df_as_image(df, path):

    norm = matplotlib.colors.Normalize(-1,1)

    plot = sns.heatmap(df, annot=True,cmap='Blues', cbar=False, fmt=".2f",linewidths=.5, annot_kws={"fontsize":8})
    # plot = sns.heatmap(df,cmap='Blues', cbar=True,linewidths=.5, vmin=0.0, vmax = 1.0)
    fig = plot.get_figure()
    plot.xaxis.set_label_position('top') 
    plt.gcf().subplots_adjust(bottom=0.25, left=0.25)



    fig.savefig(path)


if(len(sys.argv) != 2):
    print("Add param to data file")


df = pd.read_csv(sys.argv[1])

benchmarks = np.unique(df['benchmark'].to_numpy())


fuzzers = np.unique(df['covered'].to_numpy())


normalized = []
for bench in benchmarks:
    df1 = df.loc[df['benchmark'] == bench]

    df1['edges'] = (df1['edges']-df1['edges'].min())/(df1['edges'].max()-df1['edges'].min())

    normalized.extend(df1.to_numpy())

new_df = pd.DataFrame(columns=df.columns.values, data=normalized)

print(new_df.to_string())
final = []
for covered in fuzzers:
    df1 = new_df.loc[new_df['covered'] == covered]
    for not_covered in fuzzers:
        df2 = df1.loc[df1['not_covered'] == not_covered]
        if(covered == 'afl_from_input_seed'):
            print(df2.to_string())
        final.append([cut_fuzz_name(covered),cut_fuzz_name(not_covered),df2['edges'].mean()])

final_df = pd.DataFrame(columns=['covered','not_covered', 'edges'], data=final)

final_df = final_df.pivot(index='covered', columns= 'not_covered',values='edges' )
save_df_as_image(final_df, "./plots/edge_diff.svg")

print(final_df)