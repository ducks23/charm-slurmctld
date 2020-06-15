from time import sleep
  
import logging

from ops.framework import (
    EventSource,
    EventBase,
    Object,
    ObjectEvents,
)

logger = logging.getLogger()


class HostPort(Object):
    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self.framework.observe(
                charm.on[relation_name].relation_joined,
                self._on_relation_joined
            )
        self.framework.observe(
                charm.on[relation_name].relation_changed,
                self._on_relation_changed
            )

    def _on_relation_joined(self, event):
        event.relation.data[self.model.unit].setdefault('port', '9999')
        event.relation.data[self.model.unit].setdefault('host', 'host')
