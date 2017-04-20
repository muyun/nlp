#!/bin/bash

# Predict with an existing MWE model.
# Usage: ./mwe_identify.sh model input

set -eu
set -o pipefail

input=$1 # word and POS tag on each line (tab-separated)

./simptext/sst/predict_sst.sh $input > $input.pred.tags

./simptext/sst/src/tags2sst.py -l $input.pred.tags > $input.pred.sst

