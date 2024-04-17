import random

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, EventTypes


class BTCCAMessage:
    """
    A class to represent a message used in the Bracha-Toueg crash consensus algorithm.

    Attributes:
        r (int): The round number of the message.
        value (int): The proposed value (0 or 1) in the consensus.
        weight (int): The weight of the message, representing its importance or trust level.
    """

    def __init__(self, r: int, value: int, weight: int):
        self.r = r
        self.value = value
        self.weight = weight


def can_decide_0(messages_for_round_r, total_nodes):
    """
    Determines if a decision of 0 can be made based on the received messages.

    Args:
        messages_for_round_r (list of BTCCAMessage): The messages received in round r.
        total_nodes (int): Total number of nodes in the system.

    Returns:
        bool: True if a decision of 0 can be made, False otherwise.
    """
    messages_voted_0 = filter(lambda x: x.value == 0, messages_for_round_r)

    messages_voted_0_with_large_weights = list(
        filter(lambda x: x.weight > total_nodes // 2, messages_voted_0)
    )

    if len(messages_voted_0_with_large_weights) > total_nodes // 2:
        return True


def can_decide_1(messages_for_round_r, total_nodes):
    """
    Determines if a decision of 1 can be made based on the received messages.

    Args:
        messages_for_round_r (list of BTCCAMessage): The messages received in round r.
        total_nodes (int): Total number of nodes in the system.

    Returns:
        bool: True if a decision of 1 can be made, False otherwise.
    """
    messages_voted_1 = list(filter(lambda x: x.value == 1, messages_for_round_r))

    messages_voted_1_with_large_weights = list(
        filter(lambda x: x.weight > total_nodes // 2, messages_voted_1)
    )

    if len(messages_voted_1_with_large_weights) > total_nodes // 2:
        return True


class BrachaTouegCrashConsensusAlgorithmComponentModel(GenericModel):
    """
    A component model for implementing the Bracha-Toueg crash consensus algorithm.

    Inherits from GenericModel and handles the message passing, round management, and decision making.

    Attributes:
        incoming_messages (dict): A dictionary storing lists of messages by their round numbers.
        current_round (int): The current round of the consensus algorithm.
        is_there_enough_messages (bool): Flag to check if enough messages have been received to proceed.
    """

    def __init__(
        self,
        componentname,
        componentinstancenumber,
        context=None,
        configurationparameters=None,
        num_worker_threads=1,
        topology=None,
    ):
        super().__init__(
            componentname,
            componentinstancenumber,
            context,
            configurationparameters,
            num_worker_threads,
            topology,
        )

        # incoming_mesages is a dictionary for each round
        self.incoming_messages = {}

        self.current_round = 0

    def on_init(self, eventobj: Event):
        """
        Initialization event for the component, setting initial values and starting the first round.

        Args:
            eventobj (Event): The event object containing event details.
        """
        self.b = random.randint(0, 1)
        self.w = 1
        self.r = 0

        self.is_there_enough_messages = False

        self.on_round(self.r)

    def on_message_from_bottom(self, eventobj: Event):
        """
        Handles messages received from lower layers, updates the message store, and checks if decisions can be made.

        Args:
            eventobj (Event): The event object containing the received message.
        """
        print(
            f"{self.componentinstancenumber} got message from bottom",
        )

        message: BTCCAMessage = eventobj.eventcontent

        print(
            f"{self.componentinstancenumber} got message <r={message.r},b={message.value},w={message.weight}> from {eventobj.eventsource_componentinstancenumber}",
            flush=True,
        )

        messages_for_round_r = self.incoming_messages.get(message.r, [])
        messages_for_round_r.append(message)
        self.incoming_messages[message.r] = messages_for_round_r

        total_nodes = len(self.topology.nodes)
        num_of_nodes_to_wait = total_nodes // 2 + 1

        messages_for_current_round = self.incoming_messages.get(self.r, [])

        if (
            len(messages_for_current_round) >= num_of_nodes_to_wait
            and not self.is_there_enough_messages
        ):
            self.is_there_enough_messages = True
            self.on_round_enough_message(self.r)

    def on_round(self, r: int):
        """
        Initiates and manages the actions for a given round of the consensus process.
        It sends a message with the current proposal and weight for the round.

        Args:
            r (int): The current round number to manage.

        Notes:
            This method generates a new message reflecting the component's current state (b and w),
            sends it to the lower layers, and logs the action for debugging purposes.
        """
        print(
            f"{self.componentinstancenumber} on round {r}  b={self.b},w={self.w}",
            flush=True,
        )
        message = BTCCAMessage(self.r, self.b, self.w)
        event = Event(self, EventTypes.MFRT, message)

        self.send_down(event)

        print(
            f"{self.componentinstancenumber} sent message <r={message.r},b={message.value},w={message.weight}>",
            flush=True,
        )

    def on_round_enough_message(self, r: int):
        """
        Processes the messages received in a round to decide the next steps in the consensus process.
        It evaluates if a decision can be made or if further messages are needed.

        Args:
            r (int): The round number for which messages are being evaluated.

        Notes:
            This method checks if a decision of 0 or 1 can be made based on the received messages' weight and value.
            If a decision is reached, it sends out the decision messages for the next two rounds. If no decision is
            made, it checks if the majority of the messages favor a particular value and sets the proposal for the next round accordingly.
        """
        print(
            f"{self.componentinstancenumber} on round {r} started",
            flush=True,
        )

        total_nodes = len(self.topology.nodes)
        messages_for_round_r = self.incoming_messages.get(r, [])

        if can_decide_0(messages_for_round_r, total_nodes):
            # decided 0
            self.b = 0
            m1 = BTCCAMessage(self.current_round + 1, self.b, total_nodes // 2 + 1)
            self.send_down(
                Event(
                    self,
                    EventTypes.MFRT,
                    m1,
                )
            )
            m2 = BTCCAMessage(self.current_round + 2, self.b, total_nodes // 2 + 1)
            self.send_down(
                Event(
                    self,
                    EventTypes.MFRT,
                    m2,
                )
            )
            print(
                f"{self.componentinstancenumber} sent message <r={m1.r},b={m1.value},w={m1.weight}>",
                flush=True,
            )
            print(
                f"{self.componentinstancenumber} sent message <r={m2.r},b={m2.value},w={m2.weight}>",
                flush=True,
            )
            print(
                f"{self.componentinstancenumber} decided 0",
                flush=True,
            )
            return

        if can_decide_1(messages_for_round_r, total_nodes):
            # decided 1
            self.b = 1
            m1 = BTCCAMessage(self.current_round + 1, self.b, total_nodes // 2 + 1)
            self.send_down(
                Event(
                    self,
                    EventTypes.MFRT,
                    m1,
                )
            )
            m2 = BTCCAMessage(self.current_round + 2, self.b, total_nodes // 2 + 1)
            self.send_down(
                Event(
                    self,
                    EventTypes.MFRT,
                    m2,
                )
            )
            print(
                f"{self.componentinstancenumber} sent message <r={m1.r},b={m1.value},w={m1.weight}>",
                flush=True,
            )
            print(
                f"{self.componentinstancenumber} sent message <r={m2.r},b={m2.value},w={m2.weight}>",
                flush=True,
            )
            print(
                f"{self.componentinstancenumber} decided 1",
                flush=True,
            )
            return

        messages_with_large_weights = list(
            filter(lambda x: x.weight > total_nodes // 2, messages_for_round_r)
        )

        if len(messages_with_large_weights) > 0:
            self.b = messages_with_large_weights[0].value
            self.w = messages_with_large_weights[0].weight

            self.r += 1
            self.is_there_enough_messages = False
            self.on_round(self.r)
            return

        messages_voted_0 = list(filter(lambda x: x.value == 0, messages_for_round_r))
        messages_voted_1 = list(filter(lambda x: x.value == 1, messages_for_round_r))

        if len(messages_voted_0) > len(messages_voted_1):
            self.b = 0
            self.w = len(messages_voted_0)
        else:
            self.b = 1
            self.w = len(messages_voted_1)

        self.r += 1
        self.is_there_enough_messages = False
        self.on_round(self.r)
