import clr
import os
import datetime
import math

# noinspection PyBroadException
try:
    clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "StreamlabsEventReceiver.dll"))
    from StreamlabsEventReceiver import StreamlabsEventClient  # noqa: E402
except:
    pass


class SLNotifies:
    def __init__(self, stream, currency, bits_multiplier):
        self.stream = stream
        self.currency = currency
        self.bits_multiplier = bits_multiplier

        # noinspection PyBroadException
        try:
            self.enabled = True
            self.receiver = StreamlabsEventClient()
            self.receiver.StreamlabsSocketConnected += self._connected
            self.receiver.StreamlabsSocketDisconnected += self._disconnected
            self.receiver.StreamlabsSocketEvent += self._event
        except:
            self.enabled = False

    def connect(self, api_key):
        if self.enabled:
            if not self.receiver.IsConnected:
                self.receiver.Connect(api_key)

    def disconnect(self):
        if self.enabled:
            if self.receiver.IsConnected:
                self.receiver.Disconnect()

    def _connected(self, sender, args):
        self.stream.Log('NewCurrency', "[%s] Connected to Streamlabs API." % datetime.datetime.now())
        return True

    def _disconnected(self, sender, args):
        self.stream.Log('NewCurrency', "[%s] Disconnected from Streamlabs API." % datetime.datetime.now())
        return True

    def _event(self, sender, args):
        event_data = args.Data
        if event_data and event_data.For == 'twitch_account':
            if event_data.Type == 'bits':
                for message in event_data.Message:
                    currency_add = int(math.ceil(message.Amount*self.bits_multiplier))
                    self.currency.increment(message.Name.lower(), currency_add)
                    self.stream.Log(
                        'NewCurrency', "[%s] %s gained %d currency for cheering %d bits." % (datetime.datetime.now(),
                                                                                          message.Name,
                                                                                          currency_add,
                                                                                          message.Amount))

        return True
