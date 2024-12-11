from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar los routers
from app.routes import products, player, efficiencies, projects, resources, events

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5173",  # Asegúrate de agregar el URL de tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes de este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Montar los routers
app.include_router(products.router)
app.include_router(player.router)
app.include_router(efficiencies.router)
app.include_router(projects.router)
app.include_router(resources.router)
app.include_router(events.router)