from time import sleep

import logging

from ops.framework import (
    EventSource,
    EventBase,
    Object,
    ObjectEvents,
)

logger = logging.getLogger()

class HostPortAvailable(EventBase):
    def __init__(self, handle, host, port):
        super().__init__(handle)
        self.host = host
        self.port = port
    
    @property
    def host(self):
        return self.host

    @property
    def port(self):
        return self.port

class HostPortEvents(ObjectEvents):
    host_port_available = EventSource(HostPortAvailable)


class HostPort(Object):
    on = HostPortEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.framework.observe(
                charm.on[relation_name].relation_changed,
                self._on_relation_changed
            )

    def _on_relation_changed(self, event):
        host = event.relation.data[event.unit].get('host', None)
        port = event.relation.data[event.unit].get('port', None)
        if port is not None:
            logger.info(f"the port is : {port}")
        else:
            logger.warning("port is not in relation data")
        self.on.host_port_available.emit(host, port)
