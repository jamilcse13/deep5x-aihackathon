# main.py
from fastapi import FastAPI
from typing import List, Optional, Dict, Any

# Create a FastAPI app instance
app = FastAPI(
    title="Product Search API",
    description="A simple API to search for products.",
    version="1.0.0"
)

# Sample product data (in-memory database)
# In a real application, this data would likely come from a database.
PRODUCTS = [
    {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 1200.00},
    {"id": 2, "name": "Mouse", "description": "Ergonomic wireless mouse", "price": 25.00},
    {"id": 3, "name": "Keyboard", "description": "Mechanical gaming keyboard", "price": 75.00},
    {"id": 4, "name": "Monitor", "description": "27-inch 4K monitor", "price": 300.00},
    {"id": 5, "name": "Webcam", "description": "1080p HD webcam", "price": 50.00},
    {"id": 6, "name": "LAPTOP", "description": "Case-insensitive test", "price": 1250.00} # Added for case-insensitive check demo
]

@app.get("/search", summary="Search for products", response_model=List[Dict[str, Any]])
async def search_products(name: Optional[str] = None):
    """
    Search for products by name.

    - If the **name** query parameter is provided, it returns a list containing
      the product(s) matching that name (case-insensitive).
    - If the **name** is not provided or no product matches the name,
      it returns the entire list of products.
    """
    if name:
        # Perform a case-insensitive search
        # Filter the PRODUCTS list to find items where the 'name' matches the query parameter (ignoring case)
        filtered_products = [
            product for product in PRODUCTS
            if product.get("name", "").lower() == name.lower()
        ]
        # If any products match the name, return the filtered list
        if filtered_products:
            return filtered_products
        # If name was provided but no match found, fall through to return all products (as per requirement)
        # Alternatively, you could return an empty list or a 404 here if desired:
        # return []
        # from fastapi import HTTPException
        # raise HTTPException(status_code=404, detail="Product not found")

    # If no name was provided, or if name was provided but no match was found, return all products
    return PRODUCTS
