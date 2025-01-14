#!/bin/bash

# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

test_name=$1

# run test
ut_log_name=/GenAIComps/.github/workflows/scripts/${test_name}_ut.log
cd /GenAIComps/tests
if [ $test_name = 'mega' ]; then
    echo "run mega test"
    cd mega
    find . -name "test*.py" | sed 's,\.\/,python -m pytest -vs --disable-warnings ,g' > run.sh
    bash run.sh 2>&1 | tee ${ut_log_name}
else
    echo "run other test"
    python -m pytest -vs --disable-warnings ./test_${test_name}*.py 2>&1 | tee ${ut_log_name}
fi

# clean the pytest cache
rm -rf /GenAIComps/.pytest_cache

# check test result
if [ $(grep -c '== FAILURES ==' ${ut_log_name}) != 0 ] || [ $(grep -c '== ERRORS ==' ${ut_log_name}) != 0 ] || [ $(grep -c ' passed' ${ut_log_name}) == 0 ]; then
    echo "Find errors in pytest case, please check the output..."
    echo "Please search for '== FAILURES ==' or '== ERRORS =='"
    exit 1
fi
echo "UT finished successfully! "
