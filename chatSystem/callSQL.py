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
conn = sa.create_engine(connection_url)

STID = ' 2168548'


def callThatSQL(sqlCall):
    if sqlCall == "Fam_Lookup":
        Fam_Lookup_Query = "EXEC [uspFamilyLookUp] " + STID
        Fam_Lookup = pd.read_sql(Fam_Lookup_Query, conn)
        return Fam_Lookup

    if sqlCall == "unreturned":
        unreturned_query = ("EXEC [uspFamUnreturnedDevCheck] " + STID)
        Unreturned = pd.read_sql(unreturned_query, conn)
        return Unreturned

    if sqlCall == "shipClearance":
        shipmentClearanceQuery = "EXEC [uspShipmentClearanceCheck] " + str(STID)
        shipmentClearance = pd.read_sql(shipmentClearanceQuery, conn)
        return shipmentClearance


sqlProc = callThatSQL('unreturned')
teamchat = teamsChat(portal_posse)
teamchat.sendImage(sqlProc)
