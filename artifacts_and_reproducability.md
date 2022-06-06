### Files

The following repositories contain code for this project:

- https://github.com/mattweingarten/AST
   - Benchmark scripts, plotting, ideation, postprocessing
  
- https://github.com/mattweingarten/fuzzbench/
  - In particular branch ast/o0_coverage, but overall all branches prefixed with ast*.
  - Fork of Fuzzbench with custom AFL fuzzers and modified coverage instrumentation (for oO baseline results)  
    
- https://github.com/mattweingarten/AFLplusplus/tree/stable-ast-modified
  - Modified AFL++ implementation to influence compilation with compiler flags 
    
### Obtaining fuzzing data

Benchmark data is obtained through several hour long fuzzing process (ca. 50 gb in size)
See scripts such as ./bean/run_experiment.sh

The data is then postprocessed using tools:

./scripts/sancov_utils/sancov_utils.mjs

This extracts SanitizerCoverage sancov coverage data from the fuzzing results,
which then subsequently can be analyzed and processed with tools:

- ./scripts/*
- ./plots/fuzzbench_analysis/plots_all.py


### Polybox data
The ploybox data folder contains the output of several fuzzing compaign, which then susequently were postprocessed with the scripts listed above.
The reference binary (o0) is available in each experiment folder in ./coverage-binaries/coverage-build-experiment-name.tar.gz.
