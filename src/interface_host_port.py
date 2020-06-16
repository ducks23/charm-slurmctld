from time import sleep
  
import logging

from ops.framework import (
    EventSource,
    EventBase,
    Object,
    ObjectEvents,
)

logger = logging.getLogger()


class HostPortAvailableEvent(EventBase):
    def __init__(self, handle, host, port):
        super().__init__(handle)
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

class HostPortEvents(ObjectEvents):
    host_port_available = EventSource(HostPortAvailableEvent)


class HostPortRequires(Object):
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
