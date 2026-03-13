from app.api import home, auth_routes, projects_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (good for testing)
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # allow custom headers
)


app.include_router(projects_routes.router)
app.include_router(home.router)
app.include_router(auth_routes.router)
