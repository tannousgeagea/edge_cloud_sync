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
            raise HTTPException(
               status_code=status.HTTP_409_CONFLICT,
                detail=f"Event with event_id '{event_id}' already exists."
            )
            
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
):
    try:
        media = MediaFile(
            event=event
        )
        
        media.save()        
        return media
    except Exception as err:
        raise ValueError(f"Error getting model: {err}")