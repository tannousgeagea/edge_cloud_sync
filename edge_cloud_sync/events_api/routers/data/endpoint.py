
import os
import json
import time
import uuid
from pathlib import Path
from fastapi import Body
from fastapi import Request
from fastapi import HTTPException
from datetime import datetime
from pydantic import BaseModel
from fastapi.routing import APIRoute
from fastapi import status
from fastapi import FastAPI, Depends, Form, APIRouter, Request, Header, Response
from typing import Callable, Union, Any, Dict, AnyStr, Optional, List
from typing_extensions import Annotated
from events_api.tasks.data import core
from common_utils.requests.core import REQUESTS


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
    event_id:str
    source_id:str
    target:str
    data:Dict


router = APIRouter(
    prefix="/api/v1",
    tags=["Data"],
    route_class=TimedRoute,
    responses={404: {"description": "Not found"}},
)

@router.api_route(
    "/data", methods=["POST"], tags=["Data"]
)
async def sync_data(
    response:Response,
    data:ApiRequest = Body(...),
    x_request_id: Annotated[Optional[str], Header()] = None,
) -> dict:

    results = {}
    try:
        payload = REQUESTS.get(data.target)
        if not payload:
            raise HTTPException(
                status_code=400, detail=f"Invalid targed {data.target}"
            )
        
        payload = payload(**data.data)
        task = core.execute.apply_async(args=(data, payload), task_id=x_request_id)
        results = {
            "status": "received", 
            "task_id": task.id, 
            # "data": data.model_dump()
            }

    except Exception as err:
        results['error'] = {
            'status_code': 'server-error',
            "status_description": f"Internal Server Error",
            "detail": str(err),
        }
        
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
    
    return results

@router.api_route(
    "/event/data/{task_id}", methods=["GET"], tags=["Data"], response_model=ApiResponse
)
async def get_event_status(task_id: str, response: Response, x_request_id:Annotated[Optional[str], Header()] = None):
    result = {"status": "received", "task_id": str(uuid.uuid4()), "data": {}}

    return result