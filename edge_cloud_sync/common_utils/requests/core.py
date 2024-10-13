
from datetime import datetime
from pydantic import BaseModel

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

class DeliveryFlagRequest(BaseModel):
    delivery_id:str
    flag_type:str
    severity_level:str
    
class AlarmRequest(BaseModel):
    tenant_domain: str
    location: str
    entity_uid:str
    flag_type:str
    severity_level:int
    timestamp:datetime
    delivery_id:str=None

class AlarmMediaRequest(BaseModel):
    event_uid:str
    media_id:str
    media_name:str
    media_type:str
    media_url:str


REQUESTS = {
    "delivery": DeliveryRequest,
    "delivery/flag": DeliveryFlagRequest,
    "delivery/media": DeliveryMediaRequest,
    "alarm": AlarmRequest,
    "alarm/media": AlarmMediaRequest,
}
