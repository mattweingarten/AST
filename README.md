# AST


## Install
```
sudo apt-get install python3.8-dev python3.8-venv
sudo apt-get install rsync
make install-dependencies
make presubmit
make format
```




## Run Fuzzing
```
source .venv/bin/activate
```

```
PYTHONPATH=. python3 experiment/run_experiment.py python3 experiment/run_experiment.py --experiment-config experiment-config.yaml --benchmarks freetype2-2017 bloaty_fuzz_target --experiment-name $EXPERIMENT_NAME --fuzzers afl libfuzzer
```
