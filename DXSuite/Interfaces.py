from __future__ import annotations
from typing import Final as const, Any
from dataclasses import dataclass

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
    """
    読み取りユニット登録APIのリクエストボディ
    """
    file: str
    unitName: str = None
    departmentId: str = None

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