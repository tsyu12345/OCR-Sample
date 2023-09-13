from __future__ import annotations
from typing import Final as const, Any

from enum import Enum
import json
import requests
from requests.models import Response
import os

from Interfaces import *


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
        self.BASE_URL = f"https://{auth.domain}.dx-suite.com/wf/api/standard/v2"


    def __request(self, method: RequestType, uri: str, req_body: dict=None) -> Response:
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
        if req_body is None:
            req_body = {
                "files": None,
                "data": None,
            }

        response = requests.request(
            method.value, 
            uri, 
            headers=self.header, 
            files=[
                ('files', ("DSC_0456.png", open('DSC_0456.png', 'rb'))),
                ('files', ("DSC_0461.jpg", open('samples/DSC_0461.jpg', 'rb')))
            ])
        #FIXME : file format is unsupported
        if response.status_code != 200:
            error_code = response.json()["errors"][0]["errorCode"]
            message = response.json()["errors"][0]["message"]
            raise Exception(f"HTTP Status Code: {response.status_code}, \n Error Code : {error_code}, \n Message: {message}")
        
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
            
    
    def register_unit(self, workflowId: str, param: list[RegisterPOST]) -> Any:
        """_summary_
        読み取りユニット登録API.
        指定のワークフローに対して読み取る画像ファイルを登録します。
        Args:
            workflowId (str): ワークフローID
            body (dict): リクエストボディ

        Returns:
            Any: レスポンス
        """
        uri = f"{self.BASE_URL}/workflows/{workflowId}/units"
        
        files = {}
        data = {}
        for i, p in enumerate(param):
            files[f"file[{i}]"] = f"@{os.path.basename(p.file)}" #TODO:filesの指定形式がおかしい
            #file名は@test.pngの形式で送る
            data[f"unitName[{i}]"] = p.unitName
            data[f"departmentId[{i}]"] = p.departmentId

        body = {
            "files": files,
            "data": data,
        }

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


def load_auth_data() -> list[AuthData]:
    """_summary_
    Auth.jsonから認証情報を読み込む関数
    Returns:
        list[AuthData]: 認証情報
    """
    with open("./Auth.json", "r") as f:
        data = json.load(f)
        auths = []
        for a in data:
            auths.append(AuthData(
                key=a["key"], 
                id=a["id"], 
                domain=a["domain"], 
                registerDate=a["registerDate"], 
                expirationDate=a["expirationDate"]))
        return auths





if __name__ == "__main__":
    #単体テスト
    auths = load_auth_data()
    auth = auths[0]

    api = DXSuiteAPI(auth)
    """
    data = api.get_workflow_setting("b3cc8d27-6fdc-4509-944b-686bec461974", 1)
    print("workflow data",data)

    csv = api.download_csv('adbd7341-31ac-4915-b938-a62374142c8b')
    print(csv.text)
    """

    #次の画像ファイルパスが合っているか調べる
    target_img_path = "./samples/DSC_0456.jpg"
    if not os.path.exists(target_img_path):
        raise Exception("指定された画像ファイルが存在しません")

    param: list[RegisterPOST] = [
        RegisterPOST(file=target_img_path,)
    ]

    response = api.register_unit("b3cc8d27-6fdc-4509-944b-686bec461974", param)
    print(response.text)


