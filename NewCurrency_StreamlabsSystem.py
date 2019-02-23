#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Allow subs to create commands."""

# system libraries
import os
import sys

# application libraries
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from settings import MySettings  # noqa: E402
from database import InstancedDatabase  # noqa: E402
from currency import Currency  # noqa: E402

# [Required] Script Information
ScriptName = 'NewCurrency'
Website = 'https://twitch.tv/eitch'
Description = 'Adds a new currency to your channel, independent of StreamLabs builtin one.'
Creator = 'Eitch'
Version = '0.5.0'

# Define Global Variables
database_file = os.path.join(os.path.dirname(__file__), 'Currency.db')
config_file = os.path.join(os.path.dirname(__file__), 'settings.json')


def Init():
    """ [Required] Initialize Data (Only called on load) """

    # settings initialization
    global settings
    settings = MySettings(config_file)
    settings.save()

    # database initialization
    global currency, db
    db = InstancedDatabase(database_file)
    currency = Currency(Parent, db, settings.name, settings.frequency*60, settings.quantity)
    currency.only_subs = settings.only_subs

    return


def Execute(data):
    """ [Required] Execute Data / Process messages """
    return


def Tick():
    """ [Required] Tick method (Gets called during every iteration even when there is no incoming data) """
    if Parent.IsLive():
        # always gain currency while live
        currency.start_timer()
    else:
        # gain currency while offline, if setting is enabled
        if settings.gain_offline:
            currency.start_timer()
        else:
            # offline, disable currency gain
            currency.stop_timer()

    return


def ReloadSettings(json_data):
    """ [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI) """
    settings.reload(json_data)
    settings.save()
    currency.name = settings.name
    currency.frequency = settings.frequency
    currency.quantity = settings.quantity
    currency.only_subs = settings.only_subs
    return


def Unload():
    """ [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff) """
    currency.stop_timer()
    db.close()
    return


def ScriptToggled(state):
    """ [Optional] ScriptToggled (Notifies you when a user disables your script or enables it) """
    if state:
        Init()
    else:
        Unload()
    return
