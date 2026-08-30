from fastapi import FastAPI
app = FastAPI(
    title="Web Scraper Automation Platform",
    description="A web scraping and data automation platform",
    version="1.0.0"
)
@app.get("/")
def moggli():
    return {"Pa khair raghlay"}