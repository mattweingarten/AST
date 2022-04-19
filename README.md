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
PYTHONPATH=. python3 experiment/run_experiment.py  --experiment-config $EXPERIMENT_CONFIG_FILE --benchmarks freetype2-2017 bloaty_fuzz_target --experiment-name $EXPERIMENT_NAME --fuzzers afl libfuzzer 
```


## Links
Fuzzbench_fork: https://github.com/mattweingarten/fuzzbench <br />
af++_fork: https://github.com/mattweingarten/AFLplusplus <br />
Fuzzbench: https://google.github.io/fuzzbench/ <br />
LLVM flags: https://llvm.org/docs/Passes.html#id97 <br />
CLANG code coverage: https://clang.llvm.org/docs/SourceBasedCodeCoverage.html#id7 <br />


## Notes

```
PYTHONPATH=. python3 experiment/run_experiment.py --experiment-config ../AST/experiment-config.yaml  --experiment-name run14  --fuzzers aflo0 aflo1 aflo2 aflo3  
```

### Docker cleanup
```
alias docker-cleanup='docker ps -a -q | xargs -I {} docker rm {} ; docker images -q -f dangling=true | xargs -I {} docker rmi -f {}; docker volume ls -qf dangling=true | xargs -I {} docker volume rm {}'

```