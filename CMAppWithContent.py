import os
import json
import requests
import tempfile
from pathlib import Path
from datetime import datetime


def ExportCMAppWithContent(AppID, QlikClient=None, IncludeData=False, ExportScope=False):
    if not is_connected_to_qlik_sense(QlikClient):
        print("Warning: Please establish a connection to Qlik Sense before running 'ExportCMAppWithContent'")
        return None

    # Retrieve app and all objects for the specified AppID
    QSAppFull = GetQSApp(AppID)
    QSAppObjectsALL = GetQSAppObject(AppID)

    # Set up variables for temporary files that will be created during export process
    TimeStamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    TempPath = Path(tempfile.gettempdir()) / "CM2Cloud-AppMigrator"
    TempPath.mkdir(parents=True, exist_ok=True)
    TempFile = TempPath / f"{QSAppFull['id']}_{TimeStamp}.qvf"
    TempFileInfo = TempPath / f"{QSAppFull['id']}_{TimeStamp}_info.json"
    TempFileObjs = TempPath / f"{QSAppFull['id']}_{TimeStamp}_objects.json"

    write_utf8_file(TempFileInfo, QSAppFull)
    write_utf8_file(TempFileObjs, QSAppObjectsALL)

    if not ExportScope:
        PublishAndApproveObjects(QSAppObjectsALL)

    DownloadQSECMApp(QSAppFull['id'], TempFile, IncludeData, ExportScope)

    if not ExportScope:
        RestoreOriginalState(QSAppObjectsALL)

    return TempFile


def is_connected_to_qlik_sense(QlikClient):
    # Implementation to check Qlik Sense connection
    pass


def GetQSApp(AppID):
    # Implementation to get Qlik Sense app details
    pass


def GetQSAppObject(AppID):
    # Implementation to get Qlik Sense app objects
    pass


def write_utf8_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        if isinstance(content, dict):
            json.dump(content, f, ensure_ascii=False, indent=4)
        elif isinstance(content, list):
            json.dump(content, f, ensure_ascii=False, indent=4)
        else:
            f.write(content)


def PublishAndApproveObjects(QSAppObjectsALL):
    QSAppObjectsUC = [obj for obj in QSAppObjectsALL if obj['ObjectType'] in ['sheet', 'bookmark', 'story']]
    QSAppObjectsUCUA = [obj for obj in QSAppObjectsUC if not obj['approved']]
    UnpublishedUC = [obj for obj in QSAppObjectsUC if not obj['published']]

    PublishObjects(UnpublishedUC)

    if len(QSAppObjectsUCUA) > 0:
        ApproveObjects(QSAppObjectsUCUA)


def PublishObjects(UnpublishedUC):
    for obj in UnpublishedUC:
        try:
            UpdateQSAppObject(obj['id'], publish=True)
        except Exception as e:
            print(f"Error: {e}")


def ApproveObjects(QSAppObjectsUCUA):
    SelectionItems = [{"ObjectID": obj['id'], "Type": "App.Object"} for obj in QSAppObjectsUCUA]
    SelectionObj = {"Items": SelectionItems}
    selection = InvokeQSPost('/qrs/selection', SelectionObj)

    SyntheticProperties = [{"Name": "approved", "Value": True, "ValueIsDifferent": False, "ValueIsModified": True}]
    QSSyntheticRootEntity = {"Type": "App.Object", "Properties": SyntheticProperties,
                             "LatestModifiedDate": datetime.utcnow().isoformat()}

    try:
        InvokeQSPut(f"/selection/{selection['Id']}/App/Object/synthetic", QSSyntheticRootEntity)
    except Exception as e:
        print(f"Error: {e}")


def DownloadQSECMApp(AppID, TempFile, IncludeData, ExportScope):
    params = {
        "ID": AppID,
        "FileName": str(TempFile),
        "SkipData": not IncludeData
    }
    if ExportScope:
        params["ExportScope"] = "All"

    InvokeQSDownload(params)


def RestoreOriginalState(QSAppObjectsALL):
    QSAppObjectsUC = [obj for obj in QSAppObjectsALL if obj['ObjectType'] in ['sheet', 'bookmark', 'story']]
    QSAppObjectsUCUA = [obj for obj in QSAppObjectsUC if not obj['approved']]
    UnpublishedUC = [obj for obj in QSAppObjectsUC if not obj['published']]

    if len(QSAppObjectsUCUA) > 0:
        UnapproveObjects(QSAppObjectsUCUA)

    UnpublishObjects(UnpublishedUC)


def UnapproveObjects(QSAppObjectsUCUA):
    SelectionItems = [{"ObjectID": obj['id'], "Type": "App.Object"} for obj in QSAppObjectsUCUA]
    SelectionObj = {"Items": SelectionItems}
    selection = InvokeQSPost('/qrs/selection', SelectionObj)

    SyntheticProperties = [{"Name": "approved", "Value": False, "ValueIsDifferent": False, "ValueIsModified": True}]
    QSSyntheticRootEntity = {"Type": "App.Object", "Properties": SyntheticProperties,
                             "LatestModifiedDate": datetime.utcnow().isoformat()}

    try:
        InvokeQSPut(f"/selection/{selection['Id']}/App/Object/synthetic", QSSyntheticRootEntity)
    except Exception as e:
        print(f"Error: {e}")

    try:
        InvokeQSDelete(f"/qrs/selection/{selection['Id']}")
    except Exception as e:
        print(f"Error: {e}")


def UnpublishObjects(UnpublishedUC):
    for obj in UnpublishedUC:
        try:
            UpdateQSAppObject(obj['id'], publish=False)
        except Exception as e:
            print(f"Error: {e}")


def InvokeQSPost(endpoint, body):
    # Implementation to POST request to Qlik Sense API
    pass


def InvokeQSPut(endpoint, body):
    # Implementation to PUT request to Qlik Sense API
    pass


def InvokeQSDelete(endpoint):
    # Implementation to DELETE request to Qlik Sense API
    pass


def InvokeQSDownload(params):
    # Implementation to download app from Qlik Sense
    pass


def UpdateQSAppObject(obj_id, publish):
    # Implementation to update Qlik Sense app object
    pass


def TestCMExportScope():
    ExportScopeSupported = False
    try:
        OpenAPIRaw = InvokeQSGet('about/openapi/main')
        OpenAPI = json.loads(OpenAPIRaw)
        ExportScopeSupported = 'exportscope' in [param['name'] for param in
                                                 OpenAPI['paths']['/app/{id}/export/{token}']['post']['parameters']]
        if ExportScopeSupported:
            print('Verbose: Export Scope is supported')
        else:
            print('Verbose: Export Scope is not supported')
    except Exception as e:
        print('Error: Unable to Get OpenAPI Definition from Qlik Sense Server')
        print(f"Error: {e}")

    return ExportScopeSupported


def InvokeQSGet(endpoint):
    # Implementation to GET request from Qlik Sense API
    pass


# Sample usage
ExportCMAppWithContent(AppID='your-app-id', IncludeData=True, ExportScope=True)
