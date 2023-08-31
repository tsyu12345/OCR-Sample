from __future__ import annotations
from typing import Final as const
from dataclasses import dataclass
import json
import requests



@dataclass
class AuthData:
    id: int
    key: str
    domain: str
    registerDate: str
    expirationDate: str


@dataclass
class WorkFlowSettingData:
    workflowId: str
    revision: int
    applicationType: int
    ocrKind: int
    #TODO:残りを追加

class DXSuiteAPI:
    """
    DXSuiteのAPIを叩くクラス
    APIリファレンス: https://drive.google.com/file/d/1O6bDu07jbzhzVjQ_7XAVHH-AMgzq3XPB/view
    """

    BASE_URL: str

    def __init__(self, auth: AuthData):
        self.auth: const[AuthData] = auth
        BASE_URL = f"https://{auth.domain}.dx-suite.com/wf/api/standard/v2/"


    def get_workflow_setting(self, workflowId: str, revision: int) -> WorkFlowSettingData:
        uri = f"{self.BASE_URL}/workflows/{workflowId}/revisions/{revision}/configuration"
        response = requests.get(uri)
        print(f"get_workflow_setting: {response.status_code}")
        print(response.json())
        return response.json()


if __name__ == "__main__":
    #単体テスト
    with open("./Auth.json", "r") as f:
        auth = AuthData(**json.load(f))

    api = DXSuiteAPI(auth)
    api.get_workflow_setting("test", 1)