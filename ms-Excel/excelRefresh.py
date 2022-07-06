from auth import getAuth
import requests
import json
ENDPOINT = 'https://graph.microsoft.com/v1.0'


def get_pretty_json_string(value_dict):
    return json.dumps(value_dict, indent=4, sort_keys=True, ensure_ascii=False)


def prettyJSON(res):
    sxJSON = get_pretty_json_string(res.json())
    print(sxJSON)


class excelAPI:
    def __init__(self):
        self.funcResult = getAuth()
        self.headers = {
                    'Accept': 'application/json',
                   'Authorization': 'Bearer '+self.funcResult['access_token'],
                   'Content-Type': 'application/json'
                    }

    def getDrive(self):
        suffixURL = "/me/drive"
        url = ENDPOINT+suffixURL
        res = requests.get(url, headers=self.headers)
        sxJSON = get_pretty_json_string(res.json())
        print(sxJSON)

    def getDriveRecent(self):
        suffix = "/me/drive/recent"
        url = ENDPOINT + suffix
        res = requests.get(url, headers=self.headers).json()
        print(get_pretty_json_string(res))

    def reqDriveSession(self, fileID):
        suffix = f"/me/drive/items/{fileID}/workbook/createSession"
        url = ENDPOINT + suffix
        payload = {
            'persistChanges': 'true'
        }
        res = requests.post(url, headers=self.headers, json=payload)
        prettyJSON(res)

    def getSite(self):
        suffixURL = "/sites/root"
        url = ENDPOINT + suffixURL
        res = requests.get(url, headers=self.headers)
        print(res.text)

    def getSiteChildren(self, siteID, itemID):
        suffixURL = f"/sites/{siteID}/drive/items/{itemID}/children"
        url = ENDPOINT + suffixURL
        res = requests.get(url, headers=self.headers)
        print(res.text)

    def reqSiteSession(self, siteID, listID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/273/driveitem/workbook/createSession"
        url = ENDPOINT + suffix
        payload = {
            'persistChanges': 'true'
        }
        res = requests.post(url, headers=self.headers, json=payload)
        prettyJSON(res)

    def fileSearch(self, query):
        suffix = "/search/query"
        url = ENDPOINT + suffix
        payload = {
                    "requests": [
                        {
                            "entityTypes": [
                                "driveItem"
                            ],
                            "query": {
                                "queryString": "CURRENT - CCM Inventory Report - test.xlsx"
                            },
                            "sortProperties": [
                                {
                                    "name": "lastModifiedDateTime",
                                    "isDescending": "true"
                                }
                            ]
                        }
                    ]
                }
        res = requests.post(url, headers=self.headers, json=payload).json()
        sxJSON = get_pretty_json_string(res)
        print(sxJSON)
        # print(res['value'][0])
        # print(res['value'][0]['hitsContainers'][0]['hits'][0])
        # for key, value in res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['parentReference'].items():
        #     print(key, value)
        print("File Name:", res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['name'])
        print("Last Modified User: ",res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['lastModifiedBy']['user']['displayName'])
        print("File ID:", res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['id'])
        print("Site ID:", res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['parentReference']['siteId'])
        print("List ID:", res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['parentReference']['sharepointIds']['listId'])
        print("listItemId:", res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['parentReference']['sharepointIds']['listItemId'])
        print("listItemUniqueId:", res['value'][0]['hitsContainers'][0]['hits'][0]['resource']['parentReference']['sharepointIds']['listItemUniqueId'])

    def getSiteStuff(self, site):
        suffix = f"/sites/{site}/"
        url = ENDPOINT+suffix
        res = requests.get(url, headers=self.headers)
        prettyJSON(res)

    def getSiteShit(self, siteID, listID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/273/driveitem/workbook"
        url = ENDPOINT+suffix
        res = requests.get(url, headers=self.headers)
        prettyJSON(res)

    def driveRefreshAll(self, fileID):
        excelFile = f"/me/drive/root/workbook/worksheets/{fileID}/pivotTables/refreshAll"
        url = ENDPOINT+excelFile
        res = requests.post(url, headers=self.headers)
        prettyJSON(res)

    def siteRefreshAll(self, siteID, listID, listItemID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/{listItemID}/driveitem/workbook/worksheets/pivotTables/refreshAll"
        url = ENDPOINT+suffix
        res = requests.post(url, headers=self.headers)
        prettyJSON(res)

    def getSiteExcelWorksheets(self, siteID, listID, listItemID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/{listItemID}/driveitem/workbook/worksheets/"
        url = ENDPOINT+suffix
        res = requests.get(url, headers=self.headers)
        prettyJSON(res)

    def getSiteExcelWorksheetTable(self, siteID, listID, listItemID, workSheetID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/{listItemID}/driveitem/workbook/worksheets/{workSheetID}/tables"
        url = ENDPOINT+suffix
        res = requests.get(url, headers=self.headers)
        prettyJSON(res)

    def getSiteExcelWorksheetPivotTable(self, siteID, listID, listItemID, workSheetID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/{listItemID}/driveitem/workbook/worksheets/{workSheetID}/pivotTables"
        url = ENDPOINT+suffix
        res = requests.get(url, headers=self.headers)
        prettyJSON(res)

    def site2RefreshAll(self, siteID, listID, listItemID, workSheetID):
        suffix = f"/sites/{siteID}/lists/{listID}/items/{listItemID}/driveitem/workbook/worksheets/{workSheetID}/tables/refreshAll"
        url = ENDPOINT+suffix
        res = requests.post(url, headers=self.headers)
        print(res)
        if res != 200 or res != 204:
            prettyJSON(res)


excelApp = excelAPI()
# excelApp.fileSearch('CURRENT - CCM Inventory Report - test.xlsx')
# excelApp.getSiteStuff('scaatlcloud.sharepoint.com,7e9431fd-b639-45ba-b499-4eba5ae6f941,53b2c865-3d29-4db7-b404-1dccd90421ba')
# excelApp.reqSiteSession('scaatlcloud.sharepoint.com,7e9431fd-b639-45ba-b499-4eba5ae6f941,53b2c865-3d29-4db7-b404-1dccd90421ba', '69c665ca-33c1-4444-9ed7-73257286ff81')
# excelApp.getSiteExcelWorksheets('scaatlcloud.sharepoint.com,7e9431fd-b639-45ba-b499-4eba5ae6f941,53b2c865-3d29-4db7-b404-1dccd90421ba', '69c665ca-33c1-4444-9ed7-73257286ff81', '1274',)
# excelApp.getSiteExcelWorksheetTable('scaatlcloud.sharepoint.com,7e9431fd-b639-45ba-b499-4eba5ae6f941,53b2c865-3d29-4db7-b404-1dccd90421ba', '69c665ca-33c1-4444-9ed7-73257286ff81', '1274', "Inventory Report")
excelApp.site2RefreshAll('scaatlcloud.sharepoint.com,7e9431fd-b639-45ba-b499-4eba5ae6f941,53b2c865-3d29-4db7-b404-1dccd90421ba', '69c665ca-33c1-4444-9ed7-73257286ff81', '1274', "Inventory Report")
