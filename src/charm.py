#! /usr/bin/env python3
import logging, sys

sys.path.append('lib')

from ops.charm import CharmBase

from ops.main import main

from ops.model import ActiveStatus, MaintenanceStatus

from interface_host_port import HostPortRequires

from slurm_snap_instance_manager import SlurmSnapInstanceManager

from interface_munge import MungeProvides

from adapters.framework import FrameworkAdapter

logger = logging.getLogger()


class SlurmctldCharm(CharmBase):
    slurm_instance_manager_cls = SlurmSnapInstanceManager

    def __init__(self, *args):
        super().__init__(*args)

        self.dbd_requires = HostPortRequires(self, "slurmdbd-host-port")
        self.fw_adapter = FrameworkAdapter(self.framework)
        self.slurm_snap = self.slurm_instance_manager_cls(self, "slurmdctld")
        self.munge = MungeProvides(self, "munge")

        event_handler_bindings = {
            self.on.install: self._on_install,
            self.dbd_requires.on.host_port_available:
                self._on_dbd_host_port_available,

        }
        for event, handler in event_handler_bindings.items():
            self.fw_adapter.observe(event, handler)


    def _on_install(self, event):
        handle_install(
            event,
            self.fw_adapter,
            self.slurm_snap,
        )

    def _on_dbd_host_port_available(self, event):
        handle_dbd_host_port_available(
            event,
            self.fw_adapter,
        )

def handle_install(event, fw_adapter, slurm_snap):
    slurm_snap.install()
    fw_adapter.set_unit_status(ActiveStatus("slurm snap installed"))

def handle_dbd_host_port_available(event, fw_adapter, slurm_snap):
    host = event.host_port.host
    slurm_snap.write_config({
        'host': event.host_port.host,
    })
    fw_adapter.set_unit_status(ActiveStatus(f'host: {host}'))



if __name__ == "__main__":
    main(SlurmctldCharm)
