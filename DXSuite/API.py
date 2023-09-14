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
    お手元にAPIの認証情報(Auth.json)が必要です。
    """

    BASE_URL: str

    def __init__(self, auth: AuthData):
        self.auth: const[AuthData] = auth
        self.header = {
            "apikey": self.auth["key"],
        }
        self.BASE_URL = f"https://{auth['domain']}.dx-suite.com/wf/api/standard/v2"


    def __request(self, method: RequestType, uri: str, body: dict=None) -> Response:
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
        if body is None:
            body = {
                "files": None,
                "data": None,
            }

        response = requests.request(
            method.value, 
            uri, 
            headers=self.header, 
            files=body["files"])
        
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
        response = self.__request(RequestType.GET, uri)
        data = response.json()

        return WorkFlowSettingData(
            workflowId=data["workflowId"],
            revision=data["revision"],
            applicationType=data["applicationType"],
            ocrKindType=data["ocrKindType"],
            atypicalModelName= data["atypicalModelName"] if data["ocrKindType"]==2 else None,
            dataCheck=data["dataCheck"],
            dataProcessing=data["dataProcessing"],
            outputcharCode=data["outputCharCode"]
        )
    
    
    def register_unit(self, workflowId: str, param: RegisterPOST) -> RegisterResponse:
        """_summary_
        読み取りユニット登録API.
        指定のワークフローに対して読み取る画像ファイルを登録します。
        Args:
            workflowId (str): ワークフローID
            param (RegisterPOST): リクエストパラメータ
        Returns:
            dict[str, str]: {
                "unitId": 登録された読み取りユニットID,
                "unitName": 登録された読み取りユニット名
            }
        """
        uri = f"{self.BASE_URL}/workflows/{workflowId}/units"
        
        files: list[tuple] = []

        for file in param["files"]:
            files.append(('files', (file, open(file, "rb"))))
        
        body = {
            "files": files,
            "data": {}
        }
        response = self.__request(RequestType.POST, uri, body)
        data = response.json()

        return RegisterResponse(
            unitId=data["unitId"],
            unitName=data["unitName"]
        )
    

    def download_csv(self, unitId: str, save_path:str=None, overwrite:bool=False) -> Any:
        """_summary_
        CSVダウンロードAPI
        Args:
            unitId (str): 結果をダウンロードしたい読み取りユニットID
            save_path (str, optional): 保存先パス. Defaults to None.Noneの場合は保存せずにレスポンスを返します.
            overwrite (bool, optional): 保存先にファイルが存在する場合に上書きするかどうか. Defaults to False.
        Returns:
            Any: レスポンス
        """
        uri = f"{self.BASE_URL}/units/{unitId}/csv"
        response = self.__request(RequestType.GET, uri)

        #responseをcsv化して保存
        if save_path != None and overwrite:
            self.__save_csv(save_path, response)
            return {"save_path": save_path}
        elif save_path != None and overwrite == False:
            if os.path.exists(save_path):
                raise Exception("File already exists. if you want to overwrite, set overwrite=True")
            else:
                self.__save_csv(save_path, response)
                return {"save_path": save_path}
        else:
            return response


    def search_unit(self, param: SearchUnitParam) -> SearchUnitResponse:
        """_summary_
        NOTE:構築中
        TODO:返り値の型を修正
        読み取りユニット検索API
        Args:
            param (SearchUnitParam): リクエストパラメータ

        Returns:
            SearchUnitResponse: レスポンス
        """
        uri = f"{self.BASE_URL}/units?folderId={param.folderId}&workflowId={param.workflowId}&unitId={param.unitId}&unitName={param.unitName}&status={param.status}&createdFrom={param.createdFrom}&createdTo={param.createdTo}"
        data = self.__request(RequestType.GET, uri)
        return data
            
    def search_workflow(self, folderId: str, workflowName: str) -> dict[str, list[SearchWokrFlowResponse]]:
        """_summary_
        NOTE:構築中
        TODO:folderIdを複数指定できるようにする
        TODO:返り値の型を修正
        ワークフロー検索API\n
        Args:\n
            folderId (str): フォルダID.指定したフォルダ内のワークフローを検索します.\n
            workflowName (str): ワークフロー名.指定した文字列に完全一致するワークフローを検索します。1〜128文字まで指定できます。日本語で設定する場合は、URLエンコードして設定します。\n
        """
        uri = f"{self.BASE_URL}/workflows?folderId={folderId}&searchName={workflowName}"
        
        res = self.__request(RequestType.GET, uri)
        data = res.json()
        
        return 

    def __save_csv(self, path: str, response: Response) -> None:
        with open(path, "w") as f:
            f.write(response.text)
        



def load_auth_data() -> list[AuthData]:
    """_summary_
    Auth.jsonから認証情報を読み込む関数
    Returns:
        list[AuthData]: 認証情報
    """
    with open("./Auth.json", "r") as f:
        data:list[AuthData] = json.load(f)
    return data




if __name__ == "__main__":
    #単体テスト
    auths = load_auth_data()
    auth = auths[0]

    api = DXSuiteAPI(auth)
    
    data = api.get_workflow_setting("b3cc8d27-6fdc-4509-944b-686bec461974", 1)
    print("workflow data",data)

    csv = api.download_csv('adbd7341-31ac-4915-b938-a62374142c8b', "out/test.csv", True)
    print(csv)
    

    param: RegisterPOST = {
        "files": [
            "./samples/DSC_0461.jpg",
            "./samples/DSC_0462.jpg",
        ]
    }

    response = api.register_unit("b3cc8d27-6fdc-4509-944b-686bec461974", param)
    print(response)


