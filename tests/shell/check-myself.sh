#!/bin/bash

scancode -clipe --license-text --license-text-diagnostics --classify --license-clarity-score --todo --license-diagnostics --summary -n 16  --license-compatibility GPL-3.0-or-later --license-compatibility-usecase library --license-compatibility-provisioning binary-distribution --json-pp src-scan.json src/compatibility_scancode  
