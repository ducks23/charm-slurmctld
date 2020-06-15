#! /usr/bin/env python3
import logging

import sys

sys.path.append('lib')

from ops.charm import CharmBase

from ops.main import main

from ops.model import ActiveStatus, MaintenanceStatus

from interface_host_port import HostPort

class SlurmctldCharm(CharmBase):

    def __init__(self, *args):
        super().__init__(*args)

        self.hp = HostPort(self, "host-port")
        self.framework.observe(self.on.install, self.on_install)

    def on_install(self, event):
        pass

if __name__ == "__main__":
    main(SlurmctldCharm)
