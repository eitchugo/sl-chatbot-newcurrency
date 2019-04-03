# -*- coding: utf-8 -*-
import codecs
import json


class MySettings(object):
    """ Settings handler """
    settings_file = None  # type: str
    name = 'pennies'  # type: str
    frequency = 10  # type: int
    quantity = 10  # type: int
    gain_offline = False  # type: bool
    only_subs = False  # type: bool
    exclude_users = ""  # type: str
    msg_whisper = True  # type: bool
    msg_count = "$(user), you currently have $(points) $(currency)."  # type: str
    msg_increment = "Added $(points) $(currency) to $(user). New amount: $(current)."  # type: str
    msg_decrement = "Removed $(points) $(currency) from $(user). New amount: $(current)."  # type: str
    streamlabs_apikey = None  # type: str
    streamlabs_bits = 1  # type: float
    loot_notification = None  # type: str

    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.name = MySettings.name
        self.frequency = MySettings.frequency
        self.quantity = MySettings.quantity
        self.gain_offline = MySettings.gain_offline
        self.only_subs = MySettings.only_subs
        self.exclude_users = MySettings.exclude_users
        self.msg_whisper = MySettings.msg_whisper
        self.msg_count = MySettings.msg_count
        self.msg_increment = MySettings.msg_increment
        self.msg_decrement = MySettings.msg_decrement
        self.streamlabs_apikey = MySettings.streamlabs_apikey
        self.streamlabs_bits = MySettings.streamlabs_bits
        self.loot_notification = MySettings.loot_notification

        try:
            with codecs.open(settings_file, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8')
        except IOError:
            pass

    def reload(self, json_data):
        self.__dict__ = json.loads(json_data, encoding='utf-8')

        return
    
    def save(self):
        try:
            self.quantity = int(self.quantity)
        except ValueError:
            self.quantity = MySettings.quantity

        try:
            self.frequency = int(self.frequency)
        except ValueError:
            self.frequency = MySettings.frequency

        try:
            self.streamlabs_bits = float(self.streamlabs_bits)
        except ValueError:
            self.streamlabs_bits = MySettings.streamlabs_bits

        self.exclude_users = self.exclude_users.lower()

        try:
            with codecs.open(self.settings_file, encoding='utf-8-sig', mode='w+') as f:
                f.write(json.dumps(self.__dict__, encoding='utf-8'))
            with codecs.open(self.settings_file.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write('var settings = {0};'.format(json.dumps(self.__dict__, encoding='utf-8')))
        except IOError:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return
