"""
Simple FastAPI server to serve documentation links
Run with: uvicorn main:app --reload
"""
from fastapi import FastAPI
from pathlib import Path
import glob

app = FastAPI(
    title="ATAMS Documentation API",
    description="API to list all available documentation",
    version="1.0.0"
)

BASE_GITHUB_URL = "https://github.com/atams/adocs-api/blob/main/BE/"


@app.get("/adocs")
async def get_docs():
    """
    Get all markdown documentation files from BE folder with GitHub links

    Returns:
        dict: List of documentation files with their GitHub URLs
    """
    # Get current directory and BE folder
    current_dir = Path(__file__).parent
    be_folder = current_dir / "BE"

    # Check if BE folder exists
    if not be_folder.exists():
        return {
            "success": False,
            "message": "BE folder not found",
            "total": 0,
            "data": []
        }

    # Find all .md files in BE folder
    md_files = glob.glob(str(be_folder / "*.md"))

    # Create list of documentation with GitHub URLs
    docs_list = []
    for file_path in md_files:
        filename = Path(file_path).name
        docs_list.append({
            "name": filename.replace(".md", "").replace("-", " ").title(),
            "filename": filename,
            "url": f"{BASE_GITHUB_URL}{filename}"
        })

    # Sort by filename
    docs_list.sort(key=lambda x: x["filename"])

    return {
        "success": True,
        "message": "Documentation files retrieved successfully",
        "total": len(docs_list),
        "data": docs_list
    }


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "ATAMS Documentation API",
        "endpoints": {
            "/adocs": "Get all documentation files from BE folder",
            "/docs": "Swagger UI documentation",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
