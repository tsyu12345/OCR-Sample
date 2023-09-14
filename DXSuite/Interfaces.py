from __future__ import annotations
from typing import Final as const, Any, TypedDict
from dataclasses import dataclass


class AuthData(TypedDict):
    """_summary_
    DXSuite API の認証情報。Auth.jsonの要素の型定義
    """
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


class RegisterPOST(TypedDict, total=False):
    """
    読み取りユニット登録APIのリクエストボディ\n
    Args:\n
        files (list[str]): 読み取り対象の画像ファイルのパス\n
        unitName* (str): 読み取りユニット名\n
        departmentId* (str): 部門ID\n
    """
    files: list[str]
    unitName: str
    departmentId: str

@dataclass
class RegisterResponse:
    """
    読み取りユニット登録APIのレスポンスデータ
    """
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