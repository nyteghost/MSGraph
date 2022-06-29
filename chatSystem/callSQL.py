from chat import teamsChat
import sqlalchemy as sa
from sqlalchemy import exc
from sqlalchemy.engine import URL
import pandas as pd
from doorKey import config
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

groupId = os.getenv('groupId')
channelID = os.getenv('channelID')
code_collab = os.getenv('code_collab')
portal_posse = os.getenv('portal_posse')
mainDataChat = os.getenv('mainDataChat')


class sqlConnect:
    def __init__(self, STID):
        self.conn = None
        self.STID = STID

    def connection(self):
        connection_string = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=" + (config["database"]["Server"]) + ";"
            "Database=isolatedsafety;"
            "UID=" + (config["database"]["UID"]) + ";"
            "PWD=" + (config["database"]["PWD"]) + ";"
        )
        connection_url = URL.create(
            "mssql+pyodbc", query={"odbc_connect": connection_string}
        )
        self.conn = sa.create_engine(connection_url)

    def callThatSQL(self, sqlCall):
        self.connection()
        queryResult = None
        if sqlCall == "Fam_Lookup":
            Fam_Lookup_Query = "EXEC [uspFamilyLookUp] " + self.STID
            Fam_Lookup = pd.read_sql(Fam_Lookup_Query, self.conn)
            queryResult = Fam_Lookup

        if sqlCall == "unreturned":
            unreturned_query = ("EXEC [uspFamUnreturnedDevCheck] " + self.STID)
            Unreturned = pd.read_sql(unreturned_query, self.conn)
            queryResult = Unreturned

        if sqlCall == "shipClearance":
            shipmentClearanceQuery = "EXEC [uspShipmentClearanceCheck] " + str(self.STID)
            shipmentClearance = pd.read_sql(shipmentClearanceQuery, self.conn)
            queryResult = shipmentClearance
        return queryResult


df = pd.DataFrame(np.random.randint(0, 100, size=(15, 4)), columns=list('ABCD'))

sqlProc = sqlConnect('2168548').callThatSQL('shipClearance')
teamchat = teamsChat(mainDataChat)
teamchat.sendTable(sqlProc)
