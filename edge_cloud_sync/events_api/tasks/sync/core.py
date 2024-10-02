import os
import cv2
import uuid
import django
django.setup()

import time
import logging
import numpy as np
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from common_utils.cloud import azure

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='media:sync_data')
def sync_data(self, data, media_file, **kwargs):
    
    results:dict = {}
    try:
        url = azure.core.push(
            AzAccountUrl=os.getenv('AzAccountUrl'),
            AzAccountKey=os.getenv('AzAccountKey'),
            media_file=media_file,
            blob_name=data.blob_name,
            container_name=data.container_name,
        )

        results.update(
            {
                "action": "done",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "results": f"Media file uploaded successfully! Access Point: {url}",
            }
        )
        
        
        return results
    
    except Exception as err:
        raise ValueError(f"Error syncing data! received data {data}: {err}")