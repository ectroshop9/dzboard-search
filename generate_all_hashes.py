import requests
from supabase import create_client
import os
import time

supabase = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_ANON_KEY')
)

SEARCH_API = "https://dzboard-search-tau.vercel.app"

products = supabase.table('products').select('id,name,image').neq('image', None).execute()

total = 0
success = 0
failed = 0

for product in products.data or []:
    image_url = product.get('image')
    if not image_url:
        continue
    
    total += 1
    print("معالجة: " + str(product['name']) + " (ID: " + str(product['id']) + ")")
    
    try:
        img_response = requests.get(image_url, timeout=15)
        if img_response.status_code != 200:
            print("فشل تحميل الصورة")
            failed += 1
            continue
        
        files = {'file': ('image.jpg', img_response.content, 'image/jpeg')}
        hash_response = requests.post(SEARCH_API + "/generate-hashes", files=files, timeout=30)
        hash_data = hash_response.json()
        
        if hash_data.get('success'):
            supabase.table('products').update({
                'phash': hash_data['phash'],
                'dhash': hash_data['dhash']
            }).eq('id', product['id']).execute()
            
            print("تم!")
            success += 1
        else:
            print("فشل")
            failed += 1
        
        time.sleep(0.5)
        
    except Exception as e:
        print("خطأ: " + str(e))
        failed += 1

print("النتائج:")
print("نجح: " + str(success))
print("فشل: " + str(failed))
print("المجموع: " + str(total))
