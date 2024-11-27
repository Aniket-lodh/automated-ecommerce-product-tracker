import time
import models
from crud.routes import user_routes, product_routes
from helpers import confirm_otp, set_cookie
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from crud import add_tracked_product
from crud.schemas import TrackedProductsCreate, UsersSessionReqModel

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(product_routes)


@app.get("/")
def server():
    return JSONResponse(content={"message": "welcome to the server", "status": 200})


@app.post("/otp/verify")
def verify_otp(
    request_body: UsersSessionReqModel,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        token = confirm_otp(request_body, db)
        if not token:
            raise Exception("Error verifying otp, please try again later!")

        set_cookie(response, key="user_session", value=token)
        return JSONResponse(
            content={
                "message": "Verified OTP, redirecting to home page...",
                "status": 200,
            },
            headers=response.headers,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/track-product")
def track_product(data: TrackedProductsCreate, db: Session = Depends(get_db)):
    try:
        tracked_products = add_tracked_product(db=db, payload_data=data)
        return tracked_products
    except Exception as e:
        print("error in /track-products/")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                str(e)
                if str(e)
                else "Error adding product to track, please try again later!"
            ),
        )


@app.middleware("http")
async def add_process_time_header(req: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(req)
    process_time = time.perf_counter() - start_time
    response.headers["X-process-Time"] = str(process_time)
    return response
