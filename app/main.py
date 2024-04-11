from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from .src.database import Base, engine
from .src.router.api import router

load_dotenv()

def create_application():
    app = FastAPI(title="Bigger Applications")
    
    # Create Tables
    from .src.domain.user.models import User 
    Base.metadata.create_all(bind=engine)
    
    # Include Routers
    app.include_router(router)
    
    # Add Modules
    
    return app


app = create_application()

@app.get("/")
async def home():
    return {"message": "Hello World"}


# Exception Handlers 

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    custom_error = []
    for error in details:
        custom_error.append(
            {
                "field": error['loc'],
                "message": error['msg']
            }
        )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": custom_error})
    )