# SPDX-FileCopyrightText: 2026 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

clean:
	-rm -fr src/scancode_compatibility.egg-info
	-rm -fr build
	-find . -name "*~" | xargs rm
	-rm src-scan.json
