import sys
import numpy as np
import pandas as pd
import seaborn as sns;
import matplotlib
import matplotlib.pyplot as plt
from util import *

sns.set_theme(style="whitegrid")

if(len(sys.argv) != 3):
    print("Add param and config to data file")

_COLOR_PALETTE = [
    '#1f77b4',
    '#98df8a',
    '#d62728',
    '#c7c7c7',
    '#ff7f0e',
    '#ff9896',
    '#e377c2',
    '#dbdb8d',
    '#2ca02c',
    '#c5b0d5',
    '#7f7f7f',
    '#9edae5',
    '#aec7e8',
    '#8c564b',
    '#c49c94',
    '#bcbd22',
    '#ffbb78',
    '#9467bd',
    '#f7b6d2',
    '#17becf',
]

_DEFAULT_TICKS_COUNT = 12
_DEFAULT_LABEL_ROTATION = 30
def get(axis, count):
    m = int(count / 4)
    n = count % 4
    print((m,n))
    return axis[m][n]

def get(count):
    m = int(count / 4)
    n = count % 4
    # print((m,n))
    return m,n


df = pd.read_csv(sys.argv[1])
bench_json = get_exp_json(sys.argv[2])

benchmarks = np.unique(df['benchmark'].to_numpy())

# fig, axis = plt.subplots(4,4,figsize=(50,50))

# axes1 = axis[0]
# print(axes1)
# print(axis)
fig = plt.figure(figsize= (30,10))
# print(fig)
count = 0
for bench in benchmarks:
    if(bench == "curl_curl_fuzzer_http"):
        continue

    if(bench == "jsoncpp_jsoncpp_fuzzer"):
        continue
    df1 = df.loc[df['benchmark'] == bench]
    df1 = df1.groupby(['benchmark','fuzzer']).mean().reset_index()
    df1 = df1.copy()
    m,n = get(count)
    print(bench)
    df1['fuzzer'] = df1['fuzzer'].apply(lambda x : cut_fuzz_name(x))
    plt.subplot(4,4,count + 1)
    plot = sns.barplot(x='fuzzer', y='edges',data=df1, dodge=True,palette=_COLOR_PALETTE, errwidth=0)
        # plt.gca().legend()
        # plt.gca().legend(
        # loc="upper center",
        # ncol=len(df['fuzzer']),
        # bbox_to_anchor=(0.5, 0.16),
        # bbox_transform=fig.transFigure,
        # frameon=False
        # )

    # print(df1)
    # df1 = df1.pivot(index='fuzzer', columns= 'benchmark',values='edges' )
    # sns.bar(x='benchmark', y='edges', )
    # plt.bar(df['fuzzer'], df['edges'], color=_COLOR_PALETTE)
    # print(df1)
    ax = plt.gca()
    ax.set_xlabel(bench)
    # # ax =get(axis,count)
    # print(ax)
    # # plt.sca(ax)
    plot.xaxis.set_label_position('top') 
    sns.despine(ax=ax, trim=True)
    plt.subplots_adjust(
                    wspace=0.2, 
                    hspace=0.9)
    plt.xticks(rotation=75)
    
    # print(get(axis,count))
    # sns.barplot(x='fuzzer', y='edges', hue='fuzzer', data=df,dodge=True,palette=_COLOR_PALETTE, errwidth=0, ax=ax) 

    # ax.get_legend().remove()
    count += 1
    # print(df1)
# print(count)
# plt.show()
plt.subplot(4,4,count)

plt.savefig("./plots/all.svg")


# print(axis)
# print(len(benchmarks))