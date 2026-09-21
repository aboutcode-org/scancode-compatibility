# scancode-compatibility

[Scancode Toolkit](https://github.com/aboutcode-org/scancode-toolkit) plugin to check compatibility between a user specified outbound license with the licenses in a scan report.

# Use case

Let's say you want to use an open source component, called C, in a program that you want to release under the outbound license, A.

To use the component you need to check if C's licenses are compatible with license A. To identify the licenses of the component C you need to scan the source code. A source code scan with scancode identifies, among other things, the license of each file.

With this plugin each file is checked for compatibility with the outbound license. 

# Using

When scanning with scancode and want to enable license compatibility checks you need to pass the following information:
* outbound license - the license of your program
* usecase - the way you use the scanned component (see [codeberg.org/software-compliance-org/licomp](https://codeberg.org/software-compliance-org/licomp). Default is `library`. 
* provisioning - the way you provide the scanned component to your users (see [codeberg.org/software-compliance-org/licomp](https://codeberg.org/software-compliance-org/licomp). Default is `binary-distribution`.

To enable the compatibility checks and set the outbound license `MIT` use `--license-compatibility MIT`.

To set the usecase to `snippet`, use  `--license-compatibility-usecase snippet`.

To set the provisioning to `source-code-distribution`, use  `--license-compatibility-provisioning source-code-distribution`.

Example scancode toolkit command line, with outbound license `GPL-3.0-or-later`:

```shell
scancode -clipe --license-text --license-text-diagnostics --classify --license-clarity-score --todo --license-diagnostics --summary -n 16  --license-compatibility GPL-3.0-or-later --license--json-pp  OUTOUT_FILE DIR_TO_SCAN
```

# Output explained

When using the plugin each file gets comptibility information attached in the scancode report. Here's an example:

```json
      "license_compatibility": {
        "outbound": "GPL-3.0-or-later",
        "inbound": "GPL-3.0-or-later",
        "usecase": "library",
        "provisioning": "binary-distribution",
        "compatibility": "yes",
        "resources": [
          "licomp_reclicense"
        ]
      },
```

In the `license_compatibility` object for a file we find the following variables:

* `outbound` - the outbound license (i.e. the license you specified)
* `inbound` - the license of the file (in the used component)
* `usecase` - the way you use the scanned component (see [codeberg.org/software-compliance-org/licomp](https://codeberg.org/software-compliance-org/licomp)
* `provisioning` - the way you provide the scanned component to your users (see [codeberg.org/software-compliance-org/licomp](https://codeberg.org/software-compliance-org/licomp)
* `compatibility` - the status of compatibility (see below)
* `resources` - the [licomp](https://codeberg.org/software-compliance-org/licomp) resources used to determine compatibility

Compatbility statuses:
* `yes` - the licenses are compatible
* `no` - the licenses are NOT compatible
* `unsupported` - the file's license is not supported by the tools examining compatiblity

# Installing

For now, installation needs to be done via the git repo:

```shell
git clone https://codeberg.org/hesa/scancode-compatibility.git
cd https://codeberg.org/hesa/scancode-compatibility.git
pip install .
```

# Tools used

* scancode toolkit
* licomp-toolkit
* flame
