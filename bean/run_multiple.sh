#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RUN=$SCRIPT_DIR/run_experiment.sh

$RUN libhtp_fuzz_htp
# $RUN stb_stbi_read_fuzzer
# $RUN poppler_pdf_fuzzer
# $RUN vorbis-2017-12-11
# $RUN libpng-1.2.56
# $RUN aspell_aspell_fuzzer
# $RUN freetype2-2017
# $RUN lcms-2017-03-21
# $RUN libjpeg-turbo-07-2017
# $RUN harfbuzz-1.3.2
