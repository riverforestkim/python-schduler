#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

import os
import traceback

class MergeSchedulerMainApp:

    def __init__(self):
        pass

    def Initialize(self):

        return True

    def DoExternalScript(self, strShellScriptArgs):

        LOG().debug("start do external script")

        self.__RunExternalShellScript(strShellScriptArgs)

        LOG().debug("end do external script")
        return True

    def __RunExternalShellScript(self, strShellScriptArgs):

        if None != strShellScriptArgs and 0 < len(strShellScriptArgs):
            os.system(strShellScriptArgs)

        return True
