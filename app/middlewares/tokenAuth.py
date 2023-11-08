
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

import os
load_dotenv()

database_url = os.getenv("DATABASE_URL")


async def check_bearer_token(request, call_next):
    try:
        api_token = request.query_params['api_token']
        if api_token != os.getenv("API_TOKEN"):
            return JSONResponse(
                content={"success": False, "message": "Token is not valid",
                         "errors": []},
                status_code=403,
            )
        response = await call_next(request)
        return response
    except KeyError:
        return JSONResponse(
            content={"success": False, "message": "Token is required to access this resource",
                     "errors": []},
            status_code=403,
        )
