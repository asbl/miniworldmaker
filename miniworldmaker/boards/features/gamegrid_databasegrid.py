import sqlite3 as lite

class DatabaseGrid():
    """
    Ein Grid mit Datenbank-Anbindung.

    Achtung: Die Funktionen müssen immer in folgender Reihenfolge ausgeführt werden:
    connect
    select/insert (beliebig viele)
    commit
    close
    """
    def connect(self, database):
        """
        Verbindet sich zu einer sqlite Datanbank
        Parameters
        ----------
        database
            Die Datenbank, zu der sich das Programm verbinden soll

        Returns
        -------

        """
        self.connection = lite.connect(database)
        self.cursor = self.connection.cursor()

    def insert(self, table, row):
        """
        Fügt Werte in die Datenbank ein.
        Parameters
        ----------
        table : str
            Die Tabelle, in die eingefügt werden soll.
        row : dict
            Die Zeile die eingefügt werden soll als Dictionary Spaltenname : Wert

        Returns
        -------

        """
        cols = ', '.join('{}'.format(col) for col in row.keys())
        vals = ""
        for col in row.values():
            if isinstance(col,str):
                col="'"+col+"'"
            vals = vals+str(col)+","
        vals=vals[:-1] # strip last character
        sql = 'INSERT INTO '+table+'( '+str(cols)+') VALUES ('+str(vals)+')'
        print(sql)
        self.connection.execute(sql)

    def close_connection(self):
        """
        Schließt die Verbindung zur Datenbank
        Returns
        -------

        """
        self.connection.close()

    def select_single_row(self, statement: str):
        """
        Gibt einen Datensätze einer SELECT-Abfrage als Liste ( zurück
        Parameters
        ----------
        statement: str
            Das SELECT Statement

        Returns
        -------
        list
            Der Datensatz als Liste von einzelnen Werten.
        """
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def select_all_rows(self, statement: str):
        """
        Gibt alle Datensätze einer SELECT-Abfrage als Liste (von Listen) zurück
        Parameters
        ----------
        statement: str
            Das SELECT Statement

        Returns
        -------
        list
            Die Datensätze als Liste von Listen
        """
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def commit(self):
        """
        Commited alle getätigten Änderungen

        Returns
        -------

        """
        self.connection.commit()




