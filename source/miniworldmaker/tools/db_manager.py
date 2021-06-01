import logging
import sqlite3


class DBManager():
    log = logging.getLogger("db_manager")

    def __init__(self, file):
        self.file = file
        try:
            self.connection = sqlite3.connect(self.file)
            self.cursor = self.connection.cursor()
        except:
            raise

    def insert(self, table: str, row: dict) -> bool:
        try:
            cols = ', '.join('{}'.format(col) for col in row.keys())
            vals = ""
            for col in row.values():
                if isinstance(col, str):
                    col = "'" + col + "'"
                vals = vals + str(col) + ","
            vals = vals[:-1]  # strip last character
            sql = 'INSERT INTO ' + table + '( ' + str(cols) + ') VALUES (' + str(vals) + ')'
            logging.info(sql)
            self.connection.execute(sql)
            return True
        except:
            self.close_connection()
            raise

    def close_connection(self):
        self.connection.close()

    def select_single_row(self, statement: str):
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def select_all_rows(self, statement: str):
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()
