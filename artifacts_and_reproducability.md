### Repositories and Code

The following repositories contain code for this project:

- https://github.com/mattweingarten/AST (1)
   - Benchmark scripts, plotting, ideation, postprocessing
  
- https://github.com/mattweingarten/fuzzbench/ (2)
  - In particular branch ast/o0_coverage, but overall all branches prefixed with ast*.
  - Fork of Fuzzbench with custom AFL fuzzers and modified coverage instrumentation (for oO baseline results)  
    
- https://github.com/mattweingarten/AFLplusplus/tree/stable-ast-modified (3)
  - Modified AFL++ implementation to influence compilation with compiler flags 
    
### Obtaining Fuzzing data

Benchmark data is obtained through several hour long fuzzing process (ca. 20 gb in size)
See scripts such as ./bean/run_experiment.sh (1).

The data is then postprocessed using tools:

./scripts/sancov_utils/sancov_utils.mjs (1)

This extracts SanitizerCoverage sancov coverage data from the fuzzing results,
which then subsequently can be analyzed and processed with tools:

in (1):
- ./scripts/*
- ./plots/fuzzbench_analysis/plots_all.py


### Polybox data
The ploybox data folder contains the output of several fuzzing compaign (from laptop 1 and laptop 2) which then susequently were postprocessed with the scripts listed above.
The reference binary (o0) is available in each experiment folder in ./coverage-binaries/coverage-build-experiment-name.tar.gz.
The corpus for each trial for every experiment is available under ./experiment-folders/<EXPERIMENT_NAME>/trial-<TRIAL_ID>/corpus/

Where each corpus-archrive-file represents the corpus at 15 minute intervals taken by the experiment.
