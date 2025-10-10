"""
Simple FastAPI server to serve documentation links
Run with: uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import glob

app = FastAPI(
    title="ATAMS Documentation API",
    description="API to list all available documentation",
    version="1.0.0"
)

BASE_GITHUB_URL = "https://github.com/atams/adocs-api/blob/main/"


@app.get("/adocs")
async def get_docs():
    """
    Get all markdown documentation files from Backend and Frontend folders with GitHub links

    Returns:
        dict: List of documentation files with their GitHub URLs
    """
    # Get current directory
    current_dir = Path(__file__).parent

    # Folders to search for documentation
    doc_folders = ["Backend", "Frontend"]

    # Create list of documentation with GitHub URLs
    docs_list = []

    for folder_name in doc_folders:
        folder_path = current_dir / folder_name

        # Skip if folder doesn't exist
        if not folder_path.exists():
            continue

        # Find all .md files in folder
        md_files = glob.glob(str(folder_path / "*.md"))

        for file_path in md_files:
            file_path_obj = Path(file_path)
            filename = file_path_obj.name
            relative_path = f"{folder_name}/{filename}"

            docs_list.append({
                "name": filename.replace(".md", "").replace("-", " ").title(),
                "filename": relative_path,
                "url": f"{BASE_GITHUB_URL}{relative_path}"
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
    """Serve index.html"""
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
