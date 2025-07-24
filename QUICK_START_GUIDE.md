# دليل سريع لبدء تشغيل SUNA بشكل مبسط

## 1. إعداد قاعدة البيانات Supabase المحلية

يعتمد مشروع SUNA على Supabase كقاعدة بيانات. أسهل طريقة للبدء هي تشغيل نسخة محلية من Supabase:

```bash
# تثبيت Supabase CLI
npm install -g supabase

# بدء Supabase محلياً
supabase start
```

انسخ عناوين URL ومفاتيح الوصول التي يعرضها لك Supabase بعد التشغيل، ستحتاجها في الخطوة التالية.

## 2. إعداد ملفات البيئة

### ملف البيئة للخادم الخلفي
أنشئ ملف `.env` في مجلد `backend` بهذا المحتوى:

```
ENV_MODE=local
SUPABASE_URL=http://localhost:8090  # استبدل بالعنوان المناسب من Supabase CLI
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1... # استبدل بالمفتاح من Supabase CLI
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1... # استبدل بالمفتاح من Supabase CLI

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_SSL=false

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672

# مفتاح لاختبار OpenAI (يمكن استخدام مفتاح وهمي للتطوير المحلي)
OPENAI_API_KEY=sk-demo-key-for-local-development
MODEL_TO_USE=gpt-3.5-turbo
```

### ملف البيئة للواجهة الأمامية
أنشئ ملف `.env.local` في مجلد `frontend` بهذا المحتوى:

```
NEXT_PUBLIC_ENV_MODE="LOCAL"
NEXT_PUBLIC_SUPABASE_URL="http://localhost:8090"  # استبدل بالعنوان المناسب من Supabase CLI
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1..." # استبدل بالمفتاح من Supabase CLI
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
NEXT_PUBLIC_URL="http://localhost:3000"
OPENAI_API_KEY="sk-demo-key-for-local-development"
```

## 3. تشغيل الخدمات الأساسية بشكل منفصل

### تشغيل خدمات Redis و RabbitMQ
```bash
docker compose up -d redis rabbitmq
```

### تشغيل الخادم الخلفي بشكل منفصل
```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### تشغيل الواجهة الأمامية بشكل منفصل
```bash
cd frontend
npm install
npm run dev
```

## 4. التحقق من الحالة

بعد تشغيل كل المكونات بنجاح، يمكنك الوصول إلى:

- الواجهة الأمامية: http://localhost:3000
- واجهة برمجة التطبيقات: http://localhost:8000/docs

## 5. استكشاف الأخطاء وإصلاحها

إذا واجهت مشكلات في أي خطوة:

1. تأكد من تثبيت جميع الاعتماديات (Node.js, Python, Docker)
2. تأكد من أن Supabase يعمل بشكل صحيح
3. تحقق من سجلات الأخطاء لكل مكون
4. جرب تشغيل كل مكون بشكل منفصل للتعرف على الخطأ بالضبط

## 6. تبسيط بيئة التطوير (اختياري)

إذا استمرت المشكلات في بيئة Docker، يمكنك تجربة تشغيل كل المكونات محلياً:

1. قم بتثبيت Redis وPostgreSQL محلياً
2. استخدم "npm run dev" للواجهة الأمامية
3. استخدم "uvicorn api:app --reload" للواجهة الخلفية

هذا النهج أبسط ويساعد في تحديد مصادر الأخطاء بشكل أفضل.
