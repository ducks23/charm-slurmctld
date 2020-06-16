#! /usr/bin/env python3
import logging

import sys

sys.path.append('lib')

from ops.charm import CharmBase

from ops.main import main

from ops.model import ActiveStatus, MaintenanceStatus

from interface_host_port import HostPort

from slurm_snap_instance_manager import SlurmSnapInstanceManager

from adapters.framework import FrameworkAdapter


class SlurmctldCharm(CharmBase):
    slurm_instance_manager_cls = SlurmSnapInstanceManager

    def __init__(self, *args):
        super().__init__(*args)
        self.slurm_snap = self.slurm_instance_manager_cls(self, "slurmdbd")
        self.fw_adapter = FrameworkAdapter(self.framework)
        self.hp = HostPort(self, "host-port")

        event_handler_bindings = {
            self.on.install: self._on_install,
            self.hp.on.host_port_available: self._on_host_port_available
        }
        for event, handler in event_handler_bindings.items():
            self.fw_adapter.observe(event, handler)


    def _on_install(self, event):
        handle_install(
            event,
            self.fw_adapter,
            self.slurm_snap,
        )
    def _on_host_port_available(self, event):
        pass

def handle_install(self, event, fw_adapter):
    slurm_snap.install()
    fw_adapter.set_unit_status(ActiveStatus("slurm snap installed"))



if __name__ == "__main__":
    main(SlurmctldCharm)
