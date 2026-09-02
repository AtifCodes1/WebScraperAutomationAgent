from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.scraper.scraper import scrape_website
templates = Jinja2Templates(directory="app/templates")
class ScrapeRequest(BaseModel):
    url:str
app = FastAPI(
    title="Web Scraper Automation Platform",
    description="A web scraping and data automation platform",
    version="1.0.0"
)
@app.get("/",response_class=HTMLResponse)
def moggli(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request" : request}
    )
app.mount("/static",
          StaticFiles(directory="app/static"),
          name="static")
@app.post("/scrape")
def scrape(request: ScrapeRequest):
    books = scrape_website(request.url)
    return {
        "url": request.url,
        "books": books
    }