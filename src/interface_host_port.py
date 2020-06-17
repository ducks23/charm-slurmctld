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
    
    def __init__(self, handle, hp_info):
        super().__init__(handle)
        self._hp = hp_info
    
    @property
    def hp_info(self):
        return self._hp

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
        hp_info = HostPort(host, port)
        if port is not None and host is not None:
            logger.info(f"the port is : {port}")
            logger.info(f"the host is : {host}")
        else:
            logger.warning("port host is not in relation data")
        self.on.host_port_available.emit(hp_info)


class HostPort:
    def __init__(self, host, port):
        self.h = host
        self.p = port

    @property
    def host(self):
        return self.h
    
    @property
    def port(self):
        return self.p
