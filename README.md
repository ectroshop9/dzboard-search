# 🔍 DZBoard Search - البحث بالصور للوحات الإلكترونية

نظام ذكاء اصطناعي للتعرف على اللوحات الإلكترونية وقطع الشاشات بمجرد رفع صورة.

## 🚀 الروابط

| الرابط | الوظيفة |
|--------|---------|
| `/` | صفحة هبوط 3D تفاعلية |
| `/uploadbytech` | صفحة الفحص للتقني |
| `/health` | فحص الحالة (UptimeRobot) |
| `/search-by-image` | API البحث بالصورة |
| `/generate-hashes` | API توليد البصمات |
| `/reload-cache` | API تحديث الذاكرة |

## 🛠️ التقنيات

- **Python** - FastAPI
- **Supabase** - قاعدة البيانات
- **Vercel** - الاستضافة (Serverless)
- **Three.js** - الواجهة ثلاثية الأبعاد
- **Pillow + ImageHash** - معالجة الصور والبصمات

## 📦 المتطلبات

```bash
fastapi
supabase
imagehash
pillow
python-multipart
httpx
mangum
⚙️ الإعداد
إنشاء قاعدة بيانات Supabase

إضافة الأعمدة:

sql
ALTER TABLE products 
ADD COLUMN phash TEXT,
ADD COLUMN dhash TEXT;
إضافة متغيرات البيئة في Vercel:

text
SUPABASE_URL=xxxx
SUPABASE_ANON_KEY=xxxx
📖 كيف يعمل
text
صورة اللوحة → معالجة (ضغط + تحسين) → بصمة (pHash + dHash) → مقارنة → النتيجة
🔄 التدفق
إضافة منتج في المتجر → /generate-hashes يحسب بصمته تلقائياً

بحث العميل → /search-by-image يقارن البصمات

النتيجة → اسم المنتج + رابط المتجر

📊 الإحصائيات
✅ 90+ منتج ببصماتهم

🎯 دقة 99%+

⚡ زمن استجابة < 3 ثواني

🔗 المشاريع المرتبطة
المتجر: DZBoard

البحث: DZBoard Search

© 2026 DZBoard - جميع الحقوق محفوظة
