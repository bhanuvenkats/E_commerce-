import os
import uuid
from azure.storage.blob.aio import BlobServiceClient
from fastapi import UploadFile

async def upload_to_azure_blob(file: UploadFile) -> str:
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")
    blob_service_client = BlobServiceClient(
        f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )
    blob_name = f"{uuid.uuid4()}_{file.filename}"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    data = await file.read()
    await blob_client.upload_blob(data, overwrite=True)
    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
