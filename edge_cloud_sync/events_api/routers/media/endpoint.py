
import os
import json
import time
import uuid
from pathlib import Path
from fastapi import Body
from fastapi import Request
from fastapi import HTTPException
from fastapi import File, UploadFile
from datetime import datetime
from pydantic import BaseModel
from fastapi.routing import APIRoute
from fastapi import status
from fastapi import FastAPI, Depends, Form, APIRouter, Request, Header, Response
from typing import Callable, Union, Any, Dict, AnyStr, Optional, List
from typing_extensions import Annotated
from tempfile import NamedTemporaryFile
from events_api.tasks.sync_media import core

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


class ApiResponse(BaseModel):
    status: str
    task_id: str
    data: Optional[Dict[AnyStr, Any]] = None


class ApiRequest(BaseModel):
    event_id:str = Form(...)
    source_id:str = Form(...)
    blob_name:str = Form(...)
    container_name:Optional[str] = Form('.')
    metadata:Optional[str] = Form(None)


router = APIRouter(
    prefix="/api/v1",
    tags=["Media"],
    route_class=TimedRoute,
    responses={404: {"description": "Not found"}},
)


@router.api_route(
    "/event/media", methods=["POST"], tags=["Media"]
)
async def sync_data(
    response:Response,
    media_file:UploadFile = File(...),
    data:ApiRequest = Depends(),
    x_request_id: Annotated[Optional[str], Header()] = None,
) -> dict:

    results = {}
    try:
        if not media_file:
            results['error'] = {
                'status_code': 'bad-request',
                'status_description': f'No files included in the request',
                'details': f'No files included in the request',
            }
            
            response.status_code = status.HTTP_400_BAD_REQUEST
            return results
        
        
        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(media_file.filename)[1]) as temp_file:
            temp_file.write(await media_file.read())
            temp_file_path = temp_file.name
            
        task = core.sync_data.apply_async(args=(data, temp_file_path), task_id=x_request_id)
        results = {"status": "received", "task_id": task.id, "data": {}}

    except Exception as err:
        results['error'] = {
            'status_code': 'server-error',
            "status_description": f"Internal Server Error",
            "detail": str(err),
        }
        
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
    
    return results



@router.api_route(
    "/event/media/{task_id}", methods=["GET"], tags=["Media"], response_model=ApiResponse
)
async def get_event_status(task_id: str, response: Response, x_request_id:Annotated[Optional[str], Header()] = None):
    result = {"status": "received", "task_id": str(uuid.uuid4()), "data": {}}

    return result
