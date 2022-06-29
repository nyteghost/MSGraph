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
gcaEduTeam = os.getenv('gcaEduTeam')
ccmChat = os.getenv('ccmChat')


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
            print('Fam_Lookup')
            Fam_Lookup_Query = "EXEC [uspFamilyLookUp] " + self.STID
            Fam_Lookup = pd.read_sql(Fam_Lookup_Query, self.conn)
            queryResult = Fam_Lookup

        if sqlCall == "unreturned":
            print('unreturned')
            unreturned_query = ("EXEC [uspFamUnreturnedDevCheck] " + self.STID)
            Unreturned = pd.read_sql(unreturned_query, self.conn)
            queryResult = Unreturned

        if sqlCall == "shipClearance":
            shipmentClearanceQuery = "EXEC [uspShipmentClearanceCheck] " + str(self.STID)
            shipmentClearance = pd.read_sql(shipmentClearanceQuery, self.conn)
            queryResult = shipmentClearance

        if sqlCall == "currentAssignments":
            currentAssignQuery = "EXEC [uspFamCurrentAssignByOrgID] " + str(self.STID)
            currentAssign = pd.read_sql(currentAssignQuery, self.conn)
            queryResult = currentAssign

        if sqlCall == "returns":
            returnsQuery = "EXEC [uspReturnsUsingLabelsSent2Fam] " + str(self.STID)
            returns = pd.read_sql(returnsQuery, self.conn)
            queryResult = returns

        if sqlCall == "ccmStock":
            ccmStockQuery = "EXEC CCMAssetMGMT.dbo.uspGenCCMAvailDevList;"
            ccmStockQuery = pd.read_sql(ccmStockQuery, self.conn)
            queryResult = ccmStockQuery

        return queryResult


df = pd.DataFrame(np.random.randint(0, 100, size=(15, 4)), columns=list('ABCD'))
if __name__ == '__main__':
    print('Running as Main')
    sqlProc = sqlConnect('2168548').callThatSQL('Fam_Lookup')
    teamchat = teamsChat(portal_posse)
    teamchat.sendTable(sqlProc)
