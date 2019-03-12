#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Allow subs to create commands."""

# system libraries
import os
import sys
import re
import datetime
import codecs

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
Version = '0.6.1'

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

    # determine if it will work only on whisper or not
    if settings.msg_whisper:
        is_whisper = data.IsWhisper()
    else:
        is_whisper = True

    # see how many currency user has
    if is_whisper and data.Message == '!%s' % settings.name:
        reply = settings.msg_count
        reply = re.sub(r"\$\(user\)", str(data.User), reply)
        reply = re.sub(r"\$\(points\)", str(currency.get(data.User)), reply)
        reply = re.sub(r"\$\(currency\)", str(settings.name), reply)
        if settings.msg_whisper:
            Parent.SendStreamWhisper(data.User, reply)
        else:
            Parent.SendStreamMessage(reply)

    # caster can increment currency for a user
    elif is_whisper and re.search(r'^!%s-add' % settings.name, data.GetParam(0)) and \
            Parent.HasPermission(data.User, 'Caster', ''):

        if data.GetParamCount() == 3:
            user = str(data.GetParam(1)).lower()
            points = int(data.GetParam(2))

            currency.increment(user, points)
            current = currency.get(user)

            reply = settings.msg_increment
            reply = re.sub(r"\$\(user\)", user, reply)
            reply = re.sub(r"\$\(points\)", str(points), reply)
            reply = re.sub(r"\$\(currency\)", str(settings.name), reply)
            reply = re.sub(r"\$\(current\)", str(current), reply)

            if settings.msg_whisper:
                Parent.SendStreamWhisper(data.User, reply)
            else:
                Parent.SendStreamMessage(reply)

    # caster can decrement currency for a user
    elif is_whisper and re.search(r'^!%s-remove' % settings.name, data.GetParam(0)) and \
            Parent.HasPermission(data.User, 'Caster', ''):

        if data.GetParamCount() == 3:
            user = str(data.GetParam(1)).lower()
            points = int(data.GetParam(2))

            currency.decrement(user, points)
            current = currency.get(user)

            reply = settings.msg_decrement
            reply = re.sub(r"\$\(user\)", user, reply)
            reply = re.sub(r"\$\(points\)", str(points), reply)
            reply = re.sub(r"\$\(currency\)", str(settings.name), reply)
            reply = re.sub(r"\$\(current\)", str(current), reply)

            if settings.msg_whisper:
                Parent.SendStreamWhisper(data.User, reply)
            else:
                Parent.SendStreamMessage(reply)

    return


def Tick():
    """ [Required] Tick method (Gets called during every iteration even when there is no incoming data) """
    if not settings.quantity == 0:
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
    else:
        # if quantity is 0, no need to use a timer to gain currency
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


def export_and_view_currency():
    """Exports users' currency to a txt and view it."""
    Parent.Log('NewCurrency', "[%s] Exporting users' currency." % datetime.datetime.now())
    location = os.path.join(os.path.dirname(__file__), "exported_currency.txt")
    with codecs.open(location, encoding='utf-8-sig', mode='w+') as f:
        f.write("Generated at: %s\r\n" % datetime.datetime.now())
        for entry in currency.get_all():
            f.write(unicode(entry).encode('utf-8') + "\r\n")

    os.startfile(location)
    return
