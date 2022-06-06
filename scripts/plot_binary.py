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


df = pd.read_csv(sys.argv[1])
bench_json = get_exp_json(sys.argv[2])

df['benchmark'] = df['benchmark'].apply(lambda x : get_benchmark(x, bench_json['benchmarks']))


df['flags'] = df['flags'].apply(lambda x : cut_fuzz_name(x))

plot = sns.barplot(x='benchmark', y='edges', hue='flags', data=df,dodge=True,palette=_COLOR_PALETTE, errwidth=0) 

plt.gca().set_xticklabels(plt.gca().get_xticklabels(),
                            rotation=_DEFAULT_LABEL_ROTATION,
                            horizontalalignment='right')

sns.despine(ax=plt.gca(), trim=True)


# plt.xlabel('Benchmark')
plt.ylabel('Edges in CFG')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
# plt.gca().get_legend().remove()
fig = plot.get_figure()
fig.set_size_inches(25, 8)
fig.subplots_adjust(bottom=0.25)
plt.gca().grid(False)

plot.set(xlabel=None)

plt.gca().legend(
    loc="upper center",
    ncol=len(df['flags']),
    bbox_to_anchor=(0.5, 0.16),
    bbox_transform=fig.transFigure,
    frameon=False
)

print(df)
plt.savefig("./plots/binary.svg")