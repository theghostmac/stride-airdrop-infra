from fastapi import FastAPI
from api.routers import summary, staked, rewards, claim

app = FastAPI()

app.include_router(summary.router, prefix="/api")
app.include_router(staked.router, prefix="/api")
app.include_router(rewards.router, prefix="/api")
app.include_router(claim.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stride Airdrop API by MacBobby Chibuzor 🚀"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)