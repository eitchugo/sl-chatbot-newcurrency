# StreamLabs Chatbot Script - New Currency

Script for Streamlabs Chatbot for adding a new currency

# Installation and use

On Streamlabs Chatbot interface, go to `Scripts` and on the top right icons,
click on the `Import` button and chose the zip file containing this
repository. This will install the script itself.

# Currency Usage

On the settings page, configure the currency's name.

If you want users to gain currency while viewing your channel, set the how much currency gain
and at which interval they will gain it. If you want to only give currency manually yourself,
put `0` in the Currency gain field.

These are the only options needed. Check other options to further customize your currency. Help
tooltips will explain the options themselves.

## Checking your currency

Users can type `!<name>` in chat or whisper (depending on your settings) to view how many
currency they have. For a example, with a currency named `pennies`:

```
!pennies
```

If you want to check all users and their currency, use the `Export and view current` button on 
the Utilities Group Setting. A text file will be made and opened in your system. This text message
is only updated when you press the button.

## Adding or removing currency manually

The caster can manually add currency to a user. This is specially important if you deactivate 
automatic gain.

Use the following commands: 

```
# !<name>-add <description>
!pennies-add eitch 10
```

This will add 10 currency units to the user `eitch`.

And for removing:

```
# !<name>-remove <description>
!pennies-remove eitch 10
```

# Loot Usage

A loot/shop system can be used to spend the currency. The caster can add and remove items from
the shop and users can spend their currency to get it.

Currently, the base loot system will work only on whispering the bot.

These are the current commands:

To add a loot item, caster can be whisper the bot like this:

```
# !<name>-loot-add <cost> <loot> <description>
!pennies-loot-add 10 This-is-the-loot A description for the loot
```

This will add the loot: `A Description for the loot` costing 10 units of the currency. Only 
the description field supports space characters.

To list the loot, users can whisper:

```
# !<name>-loot-list
!pennies-loot-list
```

This will present a list with all the loot available and their costs. Each loot will be a
different whisper, so take care when managing a large shop. Users must be following the bot
so it does not appear to be spam.

Users can buy and obtain the loot whispering:

```
# !<name>-loot-get <description>
!pennies-loot-get A description for the loot
```
 
If the user has enough currency (in this example, 10 units), the bot will whipser the 
associated loot (`This-is-the-loot`), subtract the currency from the user and deactivate
the loot item.

To deactivate the loot manually, the caster can whisper:

```
# !<name>-loot-del <description>
!pennies-loot-del A description for the loot
```

This will search the database and deactivate the loot.

# Database

The script uses SQLite python library to create a local database file containing
all the users and their currencies. The database file location is the same as the
script itself. For example:

* C:\Users\\\<USER>\\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Scripts\sl-chatbot-newcurrency

Where `<USER>` is your local user. All databases used by this script will have
the `.db` extension.

# Change Log

## 0.7.2

* Increment and decrement will also try to add a user to the currency table first.

## 0.7.1

* Fixed a bug when sometimes the timer to gain currency are activated twice+.
* Fixed a bug when save settings was applying gain frequency wrongly.
* Fixed a bug when excluded users were being ignored from gaining currency.
* Added log message when adding currency on the configured interval.

## 0.7.0

* Loots added to the system. Users can spend the new currency to obtain loots from a "shop".

## 0.6.1

* Caster can now add currency
* Changed commands to `!<name>-add` and `!<name>-remove` for adding and removing currency.

## 0.6.0

* Export and view currency as text
* Caster can now remove currency
* Whisper-only messages settings

## 0.5.0

* Initial public release

# Author

* Hugo Cisneiros (Eitch)
* Website: https://twitch.tv/eitch