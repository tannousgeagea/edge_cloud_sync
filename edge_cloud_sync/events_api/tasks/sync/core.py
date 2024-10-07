import os
import cv2
import uuid
import django
django.setup()

import json
import time
import logging
import numpy as np
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from common_utils.cloud import azure
from common_utils.models.common import (
    get_event,
    get_media
)

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='media:sync_data')
def sync_data(self, data, media_file, **kwargs):
    
    results:dict = {}
    try:
        
        metadata = None
        if data.metadata:
            metadata = json.loads(data.metadata)
            
        event_model = get_event(
            event_id=data.event_id,
            source_id=data.source_id,
            data=metadata,
        )
        
        media = get_media(event=event_model, file_path=media_file)
        
        url = azure.core.push(
            AzAccountUrl=os.getenv('AzAccountUrl'),
            AzAccountKey=os.getenv('AzAccountKey'),
            media_file=media_file,
            blob_name=data.blob_name,
            container_name=data.container_name,
        )

        
        if url:
            media.uploaded = True
        else:
            media.error_message = f"The file '{data.blob_name}' already exists in container '{data.container_name}'."
        
        results.update(
            {
                "action": "done",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "results": f"Media file uploaded successfully! Access Point: {url}",
            }
        )
        
        
        event_model.retry_count = self.request.retries
        event_model.status = "completed"
        event_model.save()
        media.save()
        
        return results
    
    except Exception as err:
        raise ValueError(f"Error syncing data! received data {data}: {err}")