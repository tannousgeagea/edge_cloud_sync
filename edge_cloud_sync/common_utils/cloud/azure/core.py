
import os
from typing import Optional, AnyStr
from azure.storage.blob import  (
    BlobServiceClient, 
    BlobClient, 
    ContainerClient,
)

from azure.core.exceptions import (
    ServiceRequestError, 
    AzureError,
)

def push(
    AzAccountUrl:AnyStr,
    AzAccountKey:AnyStr,
    media_file:AnyStr,
    blob_name:AnyStr,
    container_name:Optional[AnyStr]='.',
):
    try:
        
        if not os.path.exists(media_file):
            raise FileNotFoundError(f"Media File {media_file} does not exist")
        
        AzConnectionUrl = f"{AzAccountUrl}?{AzAccountKey}"
        blob_service_client = BlobServiceClient(account_url=AzConnectionUrl)
        blob_client = blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name,
            )

        if blob_client.exists():
            print(f"The file '{blob_name}' already exists in container '{container_name}'.")
            return

        with open(media_file, "rb") as data:
            blob_client.upload_blob(data)

        blob_url = f"{AzAccountUrl}/{container_name}/{blob_name}"

        print(f"Access the updated file at: {blob_url}")
        print(f"File '{media_file}' uploaded to Blob Storage as '{blob_name}' in container '{container_name}'.")

        return blob_url
    except ServiceRequestError as e:
        raise ServiceRequestError(f"Connection error: {e}")
    except AzureError as e:
        raise AzureError(f"Azure error: {e}")
    except Exception as e:
        raise ValueError(f"Value error: {e}")