import os
import django
django.setup()


import logging
from database.models import Event, MediaFile
from fastapi import HTTPException, status

def get_event(
    event_id:str,
    source_id:str=None,
    data:dict=None,
):
    try:
        if Event.objects.filter(event_id=event_id).exists():
            event = Event.objects.get(event_id=event_id)
            if data:
                if event.data:
                    event.data = {
                        **event.data,
                        **data,
                    }
                else:
                    event.data = data
                
            return event
            
        event = Event(
            event_id=event_id,
            source_id=source_id,
            data=data,
        )
        
        event.save()

        return event

    except Exception as err:
        raise ValueError(f"Error getting event: {err}")
        

def get_media(
    event:Event,
    file_path:str,
    media_id:str,
):
    try:
        media = MediaFile(
            event=event,
            file_path=file_path,
            media_id=media_id,
        )
        
        media.save()        
        return media
    except Exception as err:
        raise ValueError(f"Error getting model: {err}")