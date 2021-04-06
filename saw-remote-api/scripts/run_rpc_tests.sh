#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd $DIR/../python

NUM_FAILS=0
function run_test {
    "$@"
    if (( $? != 0 )); then NUM_FAILS=$(($NUM_FAILS+1)); fi
}

echo "Setting up python environment for remote server clients..."
poetry install

export SAW_SERVER=$(which saw-remote-api)
if [[ ! -x "$SAW_SERVER" ]]; then
  echo "could not locate saw-remote-api executable - try executing with cabal v2-exec"
  exit 1
fi

echo "Running saw-remote-api tests..."
echo "Using server $SAW_SERVER"
run_test poetry run python -m unittest discover tests/saw
run_test poetry run python -m unittest discover tests/saw_low_level


popd

if [ $NUM_FAILS -eq 0 ]
then
  echo "All saw-remote-api tests passed"
  exit 0
else
  echo "Some saw-remote-api tests failed"
  exit 1
fi
