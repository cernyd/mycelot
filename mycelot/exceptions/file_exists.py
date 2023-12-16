class FileExistsInCatalogException(Exception):
    """File exists in catalog exception."""
    def __init__(self, filename: str):
        super().__init__(f"File '{filename}' already exists in catalog")
