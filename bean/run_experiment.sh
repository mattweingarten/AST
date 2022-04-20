#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $FUZZBENCH_HOME/.venv/bin/activate
name="exp-$(date +%Y-%m-%d-%H-%M-%S)"
echo $name

PYTHONPATH=$FUZZBENCH_HOME python3 $FUZZBENCH_HOME/experiment/run_experiment.py \
    --experiment-config $SCRIPT_DIR/experiment-config.bean.yaml  \
    --experiment-name "$name"  \
    --benchmarks curl_curl_fuzzer_http \
    --fuzzers aflo0 aflo1 aflo2 aflo3
