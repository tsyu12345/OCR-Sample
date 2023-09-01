from __future__ import annotations
from typing import Final as const, Any
from dataclasses import dataclass
from enum import Enum
from PIL import Image
from json import JSONDecodeError
import json
import requests
from requests.models import Response

"""Interface"""
@dataclass
class AuthData:
    id: int
    key: str
    domain: str
    registerDate: str
    expirationDate: str


@dataclass
class WorkFlowSettingData:
    """_summary\n
    ワークフロー設定取得APIのレスポンスデータ
    """
    workflowId: str
    revision: int
    applicationType: int
    ocrKindType: int 
    atypicalModelName: Any
    dataCheck: bool
    dataProcessing: bool
    outputcharCode: str

@dataclass
class SearchWokrFlowResponse:
    workflowId: str
    folderId: str
    name: str

@dataclass
class RegisterPOST:
    files: str
    unitName: str
    departmentId: str

@dataclass
class RegisterResponse:
    unitId: str
    unitName: str


@dataclass
class SearchUnitParam:
    folderId: str
    workflowId: str
    unitId: str
    unitName: str
    status: str
    createdFrom: str
    createdTo: str

@dataclass
class SearchUnitResponse:
    unitId: str
    unitName: str
    status: int
    dataProcessingStatus: int
    daatCheckStatus: int
    dataCompareStatus: int
    csvDownloadStatus: int
    csvFileName: str
    folderId: str
    workflowId: str
    workflowName: str
    createdAt: str
""""""
class RequestType(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATCH"


class DXSuiteAPI:
    """
    DXSuiteのAPIを叩くクラス
    APIリファレンス: https://drive.google.com/file/d/1O6bDu07jbzhzVjQ_7XAVHH-AMgzq3XPB/view
    """

    BASE_URL: str

    def __init__(self, auth: AuthData):
        self.auth: const[AuthData] = auth
        self.header = {
            "apikey": self.auth.key,
        }
        self.BASE_URL = f"https://{auth.domain}.dx-suite.com/wf/api/standard/v2/"


    def __request(self, method: RequestType, uri: str, body=None) -> Response:
        """_summary_
        リクエスト用補助関数
        Args:
            method (str): HTTPメソッド
            uri (str): リクエスト先URI
            body (_type_, optional): リクエストボディ. Defaults to None.
        Raises:
            Exception: リクエストエラー時に発生 != 200

        Returns:
            Any: レスポンスデータ
        """
        response = requests.request(method.value, uri, headers=self.header, json=body)

        if response.status_code != 200:
            print(response.json())
            raise Exception(f"request error code: {response.status_code}")
        
        return response




    def get_workflow_setting(self, workflowId: str, revision: int) -> WorkFlowSettingData:
        """_summary_
        ワークフロー設定取得API
        Args:
            workflowId (str): ワークフローID
            revision (int): ワークフローのリビジョン.ワークフローのリビジョンは1以上の整数です。ワークフローのリビジョンは「(10)読取ユニット状態取得API」にて取得できます。

        Returns:
            WorkFlowSettingData: ワークフロー設定データ
        """
        uri = f"{self.BASE_URL}/workflows/{workflowId}/revisions/{revision}/configuration"
        data = self.__request(RequestType.GET, uri)
        
        return data.json()
    


    def search_workflow(self, folderId: str, workflowName: str) -> dict[str, list[SearchWokrFlowResponse]]:
        """_summary_
        ワークフロー検索API\n
        Args:\n
            folderId (str): フォルダID.指定したフォルダ内のワークフローを検索します.\n
            workflowName (str): ワークフロー名.指定した文字列に完全一致するワークフローを検索します。1〜128文字まで指定できます。日本語で設定する場合は、URLエンコードして設定します。\n

        Returns:\n
            dict[str, list[SearchWokrFlowResponse]]: 以下のJSONデータを返します。\n
            { \n
                "workflows": [ \n
                    { \n
                        "workflowId": "string", \n
                        "folderId": "string", \n
                        "name": "string" \n
                    } \n
                ] \n
            } \n
        """
        uri = f"{self.BASE_URL}/workflows?folderId={folderId}&searchName={workflowName}"
        
        res = self.__request(RequestType.GET, uri)
        return res.json()
            
    
    def register_unit(self, workflowId: str, body: dict) -> Any:
        """_summary_
        読み取りユニット登録API
        Args:
            workflowId (str): ワークフローID
            body (dict): リクエストボディ

        Returns:
            Any: レスポンス
        """
        uri = f"{self.BASE_URL}/workflows/{workflowId}/units"

        response = self.__request(RequestType.POST, uri, body)
        return response
    
    
    def search_unit(self, param: SearchUnitParam) -> SearchUnitResponse:
        """_summary_
        読み取りユニット検索API
        Args:
            param (SearchUnitParam): リクエストパラメータ

        Returns:
            SearchUnitResponse: レスポンス
        """
        uri = f"{self.BASE_URL}/units?folderId={param.folderId}&workflowId={param.workflowId}&unitId={param.unitId}&unitName={param.unitName}&status={param.status}&createdFrom={param.createdFrom}&createdTo={param.createdTo}"
        data = self.__request(RequestType.GET, uri)
        return data
    

    def download_csv(self, unitId: str) -> Any:
        """_summary_
        CSVダウンロードAPI
        Args:
            unitId (str): ユニットID

        Returns:
            Any: レスポンス
        """
        uri = f"{self.BASE_URL}/units/{unitId}/csv"
        data = self.__request(RequestType.GET, uri)
        return data






if __name__ == "__main__":
    #単体テスト
    with open("./Auth.json", "r") as f:
        a = json.load(f)[0]
        auth = AuthData(
            key=a["key"], 
            id=a["id"], 
            domain=a["domain"], 
            registerDate=a["registerDate"], 
            expirationDate=a["expirationDate"])


    api = DXSuiteAPI(auth)
    data = api.get_workflow_setting("b3cc8d27-6fdc-4509-944b-686bec461974", 1)
    print(data)

    csv = api.download_csv('adbd7341-31ac-4915-b938-a62374142c8b')
    print(csv)