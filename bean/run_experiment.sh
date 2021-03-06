#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source $FUZZBENCH_HOME/.venv/bin/activate
name="exp-$(date +%Y-%m-%d-%H-%M-%S)"
echo $name

fuzzers="aflplusplus_ast_o3 aflplusplus_ast_o2 aflplusplus_ast_o1 aflplusplus_ast_o0 aflplusplus_ast_f0 aflplusplus_ast_f1 aflplusplus_ast_opt_disable aflplusplus_ast_o3_native aflplusplus_ast_opt_l1 aflplusplus_ast_o3_lto"
# Limit concurrent builds: https://github.com/google/fuzzbench/pulpl/1212
#fuzzers="afl_from_input_seed"

PYTHONPATH=$FUZZBENCH_HOME python3 $FUZZBENCH_HOME/experiment/run_experiment.py \
    --allow-uncommitted-changes \
    --experiment-config $SCRIPT_DIR/experiment-config.bean.yaml  \
    --experiment-name "$name"  \
    --benchmarks vorbis-2017-12-11 freetype2-2017 libjpeg-turbo-07-2017 curl_curl_fuzzer_http \
    --fuzzers $fuzzers \
    --concurrent-builds 2
