import os
import cv2
import uuid
import django
django.setup()

import json
import time
import logging
import requests
import numpy as np
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from common_utils.models.common import (
    get_event,
)

from common_utils.requests.core import REQUESTS

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='data:sync_data')
def execute(self, data, payload, **kwargs):
    event_model=None
    results:dict = {}
    try:
            
        event_model = get_event(
            event_id=data.event_id,
            source_id=data.source_id,
            data=data.data,
        )
    
        print(payload.model_dump())
        response = requests.post(
            url=f'http://10.10.0.7:19092/api/v1/{data.target}',
            data=json.dumps(payload.model_dump()),
        )
        
        print(response)
        results.update(
            {
                "action": "done",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        
        event_model.retry_count = self.request.retries
        event_model.status = "completed"
        event_model.save()
                
        return results
    
    except Exception as err:
        if event_model:
            event_model.error_message = f"{err}"
            event_model.save()
        
        raise ValueError(f"Error syncing data! received data {data}: {err}")