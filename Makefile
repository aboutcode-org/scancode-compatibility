# SPDX-FileCopyrightText: 2026 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

clean:
	-rm -fr src/scancode_compatibility.egg-info
	-rm -fr build
	-find . -name "*~" | xargs rm
	-rm src-scan.json

venv:
	if [ ! -d venv ] ; then python3 -m venv venv ; fi 


test:
	tests/shell/check-myself.sh
