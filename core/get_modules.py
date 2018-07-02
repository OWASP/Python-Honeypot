#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import os
import inspect

import lib
from core.compatible import is_windows
from core.alert import warn
from core.alert import messages


def load_all_modules():
    """
    load all available modules

    Returns:
        an array of all module names
    """
    # Search for Modules
    module_names = []
    for module in glob(os.path.dirname(inspect.getfile(lib)) + '/modules/*/*/__init__.py'):
        module_name = module.rsplit('\\' if is_windows() else '/')[-3] + '_' + \
                      module.rsplit('\\' if is_windows() else '/')[-2]
        if os.path.exists(module.rsplit('__init__.py')[0] + '/' + 'Dockerfile'):
            if module_name not in module_names:
                module_names.append(module_name)
        else:
            warn(messages("en", "module_not_available").format(module_name))
    return module_names
