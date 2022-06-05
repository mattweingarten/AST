#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RUN=$SCRIPT_DIR/run_experiment.sh


$RUN vorbis-2017-12-11 # needs lto
$RUN freetype2-2017   # needs lto
$RUN libjpeg-turbo-07-2017

# $RUN harfbuzz-1.3.2
# $RUN bloaty_fuzz_target
# $RUN curl_curl_fuzzer_http
# $RUN jsoncpp_jsoncpp_fuzzer
# $RUN lcms-2017-03-21
# $RUN libpcap_fuzz_both
# $RUN libpng-1.2.56
# $RUN libxml2-v2.9.2
#
#$RUN openssl_x509
#$RUN openthread-2019-12-23
#$RUN proj4-2017-08-14
#
#
## done
#$RUN vorbis-2017-12-11
#$RUN libjpeg-turbo-07-2017
#$RUN harfbuzz-1.3.2



# vorbis-2017-12-11 & \\
# freetype2-2017 & \\
# libjpeg-turbo-07-2017 & \\
# harfbuzz-1.3.2 & \\
# bloaty_fuzz_target & \\
# curl_curl_fuzzer_http & \\
# jsoncpp_jsoncpp_fuzzer & \\
# lcms-2017-03-21 & \\
# libpcap_fuzz_both & \\
# libpng-1.2.56 & \\
# libxml2-v2.9.2 & \\
# openssl_x509 & \\
# openthread-2019-12-23 & \\
# proj4-2017-08-14 & \\
