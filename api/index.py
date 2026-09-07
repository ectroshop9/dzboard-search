import io
import os
from PIL import Image, ImageEnhance, ImageOps
import imagehash
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dzboard-dz.vercel.app", "https://dzboard.vercel.app", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_ANON_KEY')
)

STORED_PRODUCTS_CACHE = None

def generate_board_hashes(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    img_resized = img.resize((512, 512), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Contrast(img_resized)
    img_final = enhancer.enhance(1.3)
    p_hash = imagehash.phash(img_final)
    d_hash = imagehash.dhash(img_final)
    return p_hash, d_hash

def load_cache():
    global STORED_PRODUCTS_CACHE
    try:
        response = supabase.table('products').select('id,name,phash,dhash').not_.is_('phash', 'null').execute()
        STORED_PRODUCTS_CACHE = response.data or []
    except Exception:
        STORED_PRODUCTS_CACHE = []

@app.get("/")
def landing():
    from fastapi.responses import HTMLResponse
    html_path = os.path.join(os.path.dirname(__file__), 'landing.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.get("/uploadbytech")
def uploadbytech():
    from fastapi.responses import HTMLResponse
    html_path = os.path.join(os.path.dirname(__file__), 'uploadbytech.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.post("/search-by-image")
async def search_by_image(file: UploadFile = File(...)):
    global STORED_PRODUCTS_CACHE
    if STORED_PRODUCTS_CACHE is None:
        load_cache()
    image_bytes = await file.read()
    user_p_hash, user_d_hash = generate_board_hashes(image_bytes)
    best_match = None
    lowest_distance = float("inf")
    for product in STORED_PRODUCTS_CACHE:
        db_p_hash = imagehash.hex_to_hash(product["phash"])
        db_d_hash = imagehash.hex_to_hash(product["dhash"])
        distance = (user_p_hash - db_p_hash) + (user_d_hash - db_d_hash)
        if distance < lowest_distance:
            lowest_distance = distance
            best_match = product
    if lowest_distance <= 25:
        product_url = f"https://dzboard-dz.vercel.app/store?q={best_match['name']}"
        return {
            "success": True,
            "product": best_match,
            "product_url": product_url,
            "confidence_score": round((1 - (lowest_distance / 128)) * 100, 2)
        }
    return {"success": False, "message": "لم يتم العثور على تطابق"}

@app.post("/generate-hashes")
async def generate_hashes(file: UploadFile = File(...)):
    image_bytes = await file.read()
    p_hash, d_hash = generate_board_hashes(image_bytes)
    return {"success": True, "phash": str(p_hash), "dhash": str(d_hash)}

@app.post("/reload-cache")
async def reload_cache():
    load_cache()
    return {"success": True, "message": "تم تحديث الذاكرة", "products": len(STORED_PRODUCTS_CACHE or [])}

handler = Mangum(app)