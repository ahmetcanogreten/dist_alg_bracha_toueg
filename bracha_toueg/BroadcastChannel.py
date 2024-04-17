from adhoccomputing.Experimentation.Topology import Event, EventTypes
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel


class BroadcastChannel(GenericChannel):
    """
    A class to represent a channel that broadcasts messages to all nodes in the system.
    """

    def on_message_from_top(self, eventobj: Event):
        """Handles messages received from the top layer, broadcasting them to all nodes in the system.

        Args:
            eventobj (Event): The event object containing the message to be broadcasted.
        """
        eventobj.event = EventTypes.MFRB
        self.send_up(eventobj)
