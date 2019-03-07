# -*- coding: utf-8 -*-
import threading
import time
import datetime


class Currency(object):
    """ Currency handler """

    def __init__(self, stream, db, name, frequency, quantity):
        self.stream = stream
        self.db = db
        self.name = name
        self.frequency = frequency
        self.quantity = quantity
        self.is_running = False
        self.gain_offline = False
        self.thread = None
        self.only_subs = False
        self.exclude_users = ""

        db.execute('CREATE TABLE IF NOT EXISTS `currency` ('
                   '`user` TEXT PRIMARY KEY NOT NULL,'
                   '`quantity` INTEGER NOT NULL DEFAULT 0)'
                   )
        db.commit()

    def insert_all(self):
        result = self.stream.GetViewerList()  # type: list
        blacklist = self.exclude_users.split(',')

        for user in result:
            insert = False

            # skip if user on blacklist
            if user in blacklist:
                continue

            # sub-only mode
            if self.only_subs:
                if self.stream.HasPermission(user, "Subscriber", ""):
                    insert = True
            # everyone
            else:
                insert = True

            if insert:
                self.db.execute("INSERT OR IGNORE INTO `currency`(user, quantity) VALUES(?, 0)", (user,))
                self.db.commit()

    def insert(self, user):
        self.db.execute("INSERT OR IGNORE INTO `currency`(user, quantity) VALUES(?, 0)", (user,))
        self.db.commit()

    def increment_all(self, quantity):
        result = self.stream.GetViewerList()  # type: list
        blacklist = self.exclude_users.split(',')

        for user in result:
            insert = False

            # skip if user on blacklist
            if user in blacklist:
                continue

            # sub-only mode
            if self.only_subs:
                if self.stream.HasPermission(user, "Subscriber", ""):
                    insert = True
            # everyone
            else:
                insert = True

            if insert:
                self.db.execute("UPDATE `currency` SET `quantity` = `quantity` + ? WHERE `user` = ?", (quantity, user,))
                self.db.commit()

    def increment(self, user, quantity):
        self.db.execute("UPDATE `currency` SET `quantity` = `quantity` + ? WHERE user = ?", (quantity, user,))
        self.db.commit()

    def decrement(self, user, quantity):
        self.db.execute("UPDATE `currency` SET `quantity` = `quantity` - ? WHERE user = ?", (quantity, user,))
        self.db.commit()

    def reset_all(self):
        self.db.execute("DELETE FROM `currency`")
        self.db.commit()

    def reset(self, user):
        self.db.execute("DELETE FROM `currency` WHERE user = ?", (user,))
        self.db.commit()

    def get(self, user):
        sql_row = self.db.execute("SELECT quantity FROM `currency` WHERE `user` = ?", (user,)).fetchone()
        if sql_row is not None:
            return int(sql_row[0])
        else:
            return 0

    def get_all(self):
        sql_row = self.db.execute("SELECT user, quantity FROM `currency`").fetchall()
        if sql_row is not None:
            return sql_row
        else:
            return 0

    def start_timer(self):
        if not self.is_running:
            self.stream.Log('NewCurrency', "[%s] Starting currency timer." % datetime.datetime.now())
            self.is_running = True
            self.thread = threading.Thread(target=self._thread, args=()).start()

    def stop_timer(self):
        if self.is_running:
            self.stream.Log('NewCurrency', "[%s] Stopping currency timer." % datetime.datetime.now())
            self.is_running = False

    def _thread(self):
        while self.is_running:
            self.insert_all()
            self.increment_all(self.quantity)
            time.sleep(self.frequency)

        self.stop_timer()
