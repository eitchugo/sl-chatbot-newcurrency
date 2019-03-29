# -*- coding: utf-8 -*-


class Loot(object):
    """ Currency handler """

    def __init__(self, stream, db):
        self.stream = stream
        self.db = db

        db.execute('CREATE TABLE IF NOT EXISTS `loot` ('
                   '`id` INTEGER PRIMARY KEY NOT NULL,'
                   '`cost` INTEGER NOT NULL DEFAULT 0,'
                   '`description` TEXT NOT NULL,'
                   '`link` TEXT,'
                   '`image` TEXT,'
                   '`loot` TEXT NOT NULL,'
                   '`active` BOOLEAN NOT NULL DEFAULT 1)'
                   )
        db.commit()

    def list(self):
        sql_row = self.db.execute(
            "SELECT cost, description FROM `loot` WHERE active = 1").fetchall()
        if sql_row is not None:
            return sql_row
        else:
            return False

    def insert(self, cost, description, link, image, loot):
        values = (cost, description, link, image, loot)
        self.db.execute("INSERT INTO `loot`(`cost`, `description`, `link`, `image`, `loot`) VALUES(?,?,?,?,?)",
                        values)
        result = self.db.commit()
        return result

    def delete(self, item_id):
        self.db.execute("UPDATE `loot` SET active = 0 WHERE `id` = ?", (item_id,))
        result = self.db.commit()
        return result

    def get(self, description):
        sql_row = self.db.execute("SELECT id, cost, loot FROM `loot` WHERE `description` = ? AND `active` = 1",
                                  (description,)).fetchone()
        if sql_row is not None:
            return sql_row
        else:
            return False
