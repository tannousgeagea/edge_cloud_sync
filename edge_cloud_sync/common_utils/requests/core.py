
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

class DeliveryRequest(BaseModel):
    tenant_domain: str
    delivery_id:str
    location: str
    delivery_start: datetime
    delivery_end: datetime

class DeliveryMediaRequest(BaseModel):
    delivery_id:str
    media_id:str
    media_name:str
    media_type:str
    media_url:str
    sensor_box_location:Optional[str] = None

class DeliveryFlagRequest(BaseModel):
    delivery_id:str
    flag_type:str
    severity_level:str
    event_uid:Optional[str] = None 
    
class AlarmRequest(BaseModel):
    tenant_domain: str
    location:str
    event_uid:str
    flag_type:str
    severity_level:int
    timestamp:datetime
    delivery_id:Optional[str]=None
    meta_info:Optional[Dict]=None

class AlarmMediaRequest(BaseModel):
    event_uid:str
    media_id:str
    media_name:str
    media_type:str
    media_url:str

class VideoArchiveRequest(BaseModel):
    tenant_domain: str
    location: str
    sensor_box_location: str
    camera_id: str
    video_id: str
    media_id: str
    media_name: str
    media_url: str
    media_type: str  # e.g., "video"
    start_time: Optional[str] = None
    end_time: Optional[str] = None

REQUESTS = {
    "delivery": DeliveryRequest,
    "delivery/flag": DeliveryFlagRequest,
    "delivery/media": DeliveryMediaRequest,
    "alarm": AlarmRequest,
    "alarm/media": AlarmMediaRequest,
    "video_archive": VideoArchiveRequest,
}
