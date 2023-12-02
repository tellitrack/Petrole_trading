from abc import ABC, abstractmethod


class MessagingInterface(ABC):

    @abstractmethod
    def send(self, recipient, message):
        """
        Send a message to the specified recipient.

        :param recipient: The identifier of the recipient (e.g., email address, phone number, chat ID).
        :param message: The message to be sent.
        """
        pass



