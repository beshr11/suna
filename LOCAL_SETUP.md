# تشغيل مشروع سُنا (SUNA) محلياً

هذا الدليل سيساعدك على تشغيل مشروع سُنا (SUNA) على جهازك المحلي.

## المتطلبات الأساسية

1. **Docker وDocker Compose**
   - تأكد من تثبيت [Docker](https://docs.docker.com/get-docker/)
   - تأكد من تثبيت [Docker Compose](https://docs.docker.com/compose/install/)

2. **Node.js و npm**
   - يتطلب Node.js الإصدار 18+ [تحميل Node.js](https://nodejs.org/)

3. **Python 3.10+**
   - [تحميل Python](https://www.python.org/downloads/)

## طريقة التشغيل السريعة

لتشغيل المشروع بالطريقة المبسطة:

```bash
# تشغيل المشروع بالكامل (خدمات الخلفية والواجهة الأمامية)
python run_local.py
```

هذا السكريبت سيقوم بـ:
1. التحقق من وجود ملفات البيئة وإنشائها إذا لم تكن موجودة
2. تشغيل خدمات الخلفية (Redis, RabbitMQ, والخادم الخلفي) باستخدام Docker
3. تشغيل الواجهة الأمامية محلياً باستخدام npm

## الوصول للمشروع

بعد تشغيل المشروع بنجاح، يمكنك الوصول إلى:

- **واجهة المستخدم (الواجهة الأمامية)**: [http://localhost:3000](http://localhost:3000)
- **واجهة برمجة التطبيقات (API)**:  [http://localhost:8000](http://localhost:8000)

## التشغيل اليدوي

إذا كنت ترغب في تشغيل كل مكون بشكل منفصل:

### 1. تشغيل خدمات الخلفية

```bash
# تشغيل Redis و RabbitMQ والخادم الخلفي
docker compose up -d redis rabbitmq backend
```

### 2. تشغيل الواجهة الأمامية

```bash
# الانتقال إلى مجلد الواجهة الأمامية
cd frontend

# تثبيت اعتماديات Node.js
npm install

# تشغيل خادم التطوير
npm run dev
```

## إيقاف التشغيل

لإيقاف جميع الخدمات:

```bash
docker compose down
```

## استكشاف الأخطاء وإصلاحها

إذا واجهت أي مشاكل في التشغيل:

1. تأكد من أن Docker يعمل على جهازك
2. تأكد من وجود ملفات البيئة اللازمة:
   - `backend/.env`
   - `frontend/.env.local`
3. تحقق من سجلات Docker:
   ```bash
   docker compose logs -f
   ```
4. تحقق من سجلات الواجهة الأمامية في نافذة المحطة الطرفية
