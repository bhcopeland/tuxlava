# -*- coding: utf-8 -*-
#
# vim: set ts=4
#
# Copyright 2026-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from urllib.parse import unquote, urlparse

import yaml

from tuxlava.devices import Device
from tuxlava.devices.fvp import FVPDevice
from tuxlava.devices.qemu import QemuDevice
from tuxlava.exceptions import InvalidArgument


class LAVADevice(Device):
    real_device = False

    def validate(self, job_definition, **kwargs):
        if not job_definition:
            raise InvalidArgument("Missing argument --job-definition")
        parsed_url = urlparse(job_definition)
        job_definition = unquote(parsed_url.path)
        with open(job_definition, "r") as job_file:
            try:
                # Load yaml and dump data as string to verify that
                # lava job definition is valid
                yaml_data = yaml.dump(yaml.safe_load(job_file))
                self.job_definition = yaml_data
            except Exception:
                raise InvalidArgument("Unable to load LAVA job definition")
        return

    def default(self, options) -> None: ...  # noqa: E704

    def definition(self, **kwargs):
        return self.job_definition


class FVPLAVA(LAVADevice, FVPDevice):
    name = "fvp-lava"


class QemuLAVA(LAVADevice, QemuDevice):
    name = "qemu-lava"
