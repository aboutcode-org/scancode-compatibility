# SPDX-FileCopyrightText: 2026 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import logging

import attr
import click
import saneyaml

from commoncode.cliutils import PluggableCommandLineOption
from commoncode.cliutils import POST_SCAN_GROUP
from commoncode.filetype import is_file
from plugincode.post_scan import PostScanPlugin
from plugincode.post_scan import post_scan_impl

from licomp_toolkit.toolkit import ExpressionExpressionChecker

from flame.license_db import FossLicenses

TRACE = os.environ.get('SCANCODE_DEBUG_LICENSE_COMPATIBILITY', False)


def logger_debug(*args):
    pass


if TRACE:

    logger = logging.getLogger(__name__)

    import sys

    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(' '.join(isinstance(a, str) and a or repr(a) for a in args))

class CompatibilityValidator:

    arg_store = {}
    
    @staticmethod
    def store(name, value):
        CompatibilityValidator.arg_store[name] = value

    @staticmethod
    def arguments():
        return CompatibilityValidator.arg_store

    @staticmethod
    def argument(name):
        return CompatibilityValidator.arg_store[name]

    def validate():
        expr_checker = ExpressionExpressionChecker()
        flame = FossLicenses()
        outbound = CompatibilityValidator.arg_store['license_compatibility']
        outbound_normalised = Compatibility.flame.expression_license(outbound, update_dual=False)['identified_license']
        usecase = CompatibilityValidator.arg_store['license_compatibility_usecase']
        provisioning = CompatibilityValidator.arg_store['license_compatibility_provisioning']
        # Check if outbound is compatible with outbound (with usecase and provisioning).
        # If not, raise exception
        ret = expr_checker.check_compatibility(outbound_normalised,
                                               outbound_normalised,
                                               usecase,
                                               provisioning,
                                               resources=['licomp_osadl', 'licomp_reclicense'],
                                               detailed_report=True)
        if not ret['compatibility'] == 'yes':
            raise click.BadParameter(f'The combination of usecase: "{usecase}", provisioning: "{provisioning}" and outbound license: "{outbound_normalised}" is not supported')
        
        
def validate_compat(ctx, param, value):
    """
    Validate the ``value`` of the outbound license and use context
    """
    CompatibilityValidator.store(param.name, value)

    if len(CompatibilityValidator.arguments()) == 3:
        if not CompatibilityValidator.arguments()['license_compatibility']:
            # outbound license not set, so plugin not enabled
            return
        CompatibilityValidator.validate()
    return value


@post_scan_impl
class Compatibility(PostScanPlugin):
    """
    Add the "license_compatibility" attribute to a resouce if it contains a
    detected license key that is found in the license_policy.yml file
    """

    resource_attributes = dict(license_compatibility=attr.ib(default=attr.Factory(dict)))

    run_order = 10
    sort_order = 10

    options = [
        PluggableCommandLineOption(('--license-compatibility',),
            default=None,
            callback=validate_compat,
            type=click.STRING,
            help='Load a License Policy file and apply it to the scan at the '
                 'Resource level.',
            help_group=POST_SCAN_GROUP,
        ),
        PluggableCommandLineOption(('--license-compatibility-usecase',),
            required_options=['license_compatibility'],
            show_default=True,
            default='library',
            callback=validate_compat,
            help='Specify the usecase of your component. Default is \'library\'',
            help_group=POST_SCAN_GROUP,
        )
        ,
        PluggableCommandLineOption(('--license-compatibility-provisioning',),
            required_options=['license_compatibility'],
            default='binary-distribution',
            callback=validate_compat,
            type=click.STRING,
            help='Specify how you provision your component. Default is \'binary-distribution\'',
            help_group=POST_SCAN_GROUP,
        )
    ]

    expr_checker = ExpressionExpressionChecker()
    flame = FossLicenses()

    def __normalize_license(self, lic_name):
        return Compatibility.flame.expression_license(lic_name, update_dual=False)['identified_license']

    def __check_compatibility(self, outbound, inbound, usecase, provisioning):
        if not inbound:
            inbound = ''
        compatibilities = Compatibility.expr_checker.check_compatibility(self.__normalize_license(outbound),
                                                                         self.__normalize_license(inbound),
                                                                         usecase,
                                                                         provisioning,
#                                                                         resources=['licomp_osadl', 'licomp_reclicense'],
                                                                         detailed_report=True)
        return Compatibility.expr_checker.simplify(compatibilities)

    def is_enabled(self, license_compatibility, **kwargs):
        return license_compatibility

    def process_codebase(self, codebase, license_compatibility, **kwargs):
        """
        Populate a license_policy mapping with four attributes: license_key, label,
        icon, and color_code at the File Resource level.
        """

        if not self.is_enabled(license_compatibility):
            return

        outbound = license_compatibility
        usecase = CompatibilityValidator.argument('license_compatibility_usecase')
        provisioning = CompatibilityValidator.argument('license_compatibility_provisioning')
        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            compat = self.__check_compatibility(outbound, resource.detected_license_expression, usecase, provisioning)
            resource.license_compatibility = compat
            codebase.save_resource(resource)
            
