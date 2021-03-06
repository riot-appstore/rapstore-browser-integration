#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import errno
import os
import subprocess

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

from .browser import BrowserNotSupportedException

FIREFOX_EXTENSION_ID = 'rapstore.browser-integration@riot-apps.net'

CHROME_EXTENSION_ID = 'dlbaedkcgjohebkgillljbggndicfoej'
CHROME_EXTENSION_ID_DEVELOPMENT = 'omfbdeblphficlecofpbkdcchnghnkhc'


def get_target_dirs(home_dir, browser):
    """
    Get the target directories for installing native messaging host

    Parameters
    ----------
    home_dir: string
        Home directory of the user
    browser: Browser
        The browser to install the host

    Returns
    -------
    array_like
        target directories

    """
    if is_mac_os():
        if is_root_user():
            target_dirs = browser.get_root_install_path(True)

        else:
            target_dirs = browser.get_user_install_path(home_dir, True)

    else:
        # we are supposing it is linux
        if is_root_user():
            target_dirs = browser.get_root_install_path(False)

        else:
            target_dirs = browser.get_user_install_path(home_dir, False)

    if target_dirs is None:
        raise BrowserNotSupportedException(browser)

    return target_dirs


def get_allowed_attribute(browser):

    if browser.get_name() == 'chrome' or browser.get_name() == 'chromium':
        return '"allowed_origins": [ "chrome-extension://{0}/", "chrome-extension://{1}/" ]'.format(CHROME_EXTENSION_ID, CHROME_EXTENSION_ID_DEVELOPMENT)

    elif browser.get_name() == 'firefox':
        return '"allowed_extensions": [ "%s" ]' % FIREFOX_EXTENSION_ID

    else:
        raise BrowserNotSupportedException(browser.get_name())


def is_mac_os():

    output = subprocess.check_output(['uname', '-s'])
    return output.strip() == 'Darwin'


def is_root_user():

    output = subprocess.check_output(['whoami'])
    return output.strip() == 'root'


def create_directories(path):
    """
    Creates all directories on path

    Parameters
    ----------
    path: string
        Path to create

    Raises
    -------
    OSError
        Something fails creating directories, except directoy already exist

    """
    try:
        os.makedirs(path)

    except OSError as e:

        if e.errno != errno.EEXIST:
            raise
