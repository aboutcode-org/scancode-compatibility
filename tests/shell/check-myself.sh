#!/bin/bash

# SPDX-FileCopyrightText: 2026 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

make venv

exit_on_failure()
{
    if [ $1 -ne 0 ]
    then
        echo "ERROR $2"
        exit $1
    fi
}

source venv/bin/activate

pip install -r requirements.txt
exit_on_failure $? "pip install -r requirements.txt"

pip install .
exit_on_failure $? "pip install ."

scancode -clipe --license-text --license-text-diagnostics --classify --license-clarity-score --todo --license-diagnostics --summary -n 16  --license-compatibility GPL-3.0-or-later --license-compatibility-usecase library --license-compatibility-provisioning binary-distribution --json-pp src-scan.json src/compatibility_scancode  
exit_on_failure $? "scancode ...."

COMPATS=$(cat src-scan.json  | jq .files[].license_compatibility.compatibility | grep -v null | wc -l)
if [ $COMPATS -ne 2 ]
then
    echo "FAIL :("
    exit 1
else
    echo "Tests OK"
    exit 0
fi
    
