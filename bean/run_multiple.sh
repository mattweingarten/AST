#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RUN=$SCRIPT_DIR/run_experiment.sh

$RUN file_magic_fuzzer
# $RUN freetype2-2017
# $RUN lcms-2017-03-21
# $RUN libjpeg-turbo-07-2017
# $RUN harfbuzz-1.3.2
