#!/usr/bin/env python3

import os
import subprocess
import sys
import platform
import time
from pathlib import Path

# تحديد نظام التشغيل
IS_WINDOWS = platform.system() == 'Windows'
# المسار الرئيسي للمشروع
ROOT_DIR = Path(__file__).parent.absolute()

# ألوان الطباعة للتمييز في الطرفية
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# طباعة العناوين بلون مميز
def print_header(msg):
    print(f"{Colors.BLUE}{Colors.BOLD}[SUNA] {msg}{Colors.ENDC}")

# طباعة رسائل النجاح بلون أخضر
def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")

# طباعة التحذيرات بلون أصفر
def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.ENDC}")

# طباعة الأخطاء بلون أحمر
def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")

# التأكد من وجود ملفات البيئة الضرورية
def setup_env_files():
    # إعداد ملف البيئة للخادم الخلفي
    backend_env = ROOT_DIR / "backend" / ".env"
    if not backend_env.exists():
        print_warning("إنشاء ملف .env للخادم الخلفي...")
        with open(backend_env, "w") as f:
            f.write("""ENV_MODE=local
SUPABASE_URL=http://localhost:8090
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_SSL=false

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672

# مفتاح API وهمي لاختبار OpenAI
OPENAI_API_KEY=sk-demo-key-for-local-development
MODEL_TO_USE=gpt-3.5-turbo
""")
        print_success("تم إنشاء ملف .env للخادم الخلفي")

    # إعداد ملف البيئة للواجهة الأمامية
    frontend_env = ROOT_DIR / "frontend" / ".env.local"
    if not frontend_env.exists():
        print_warning("إنشاء ملف .env.local للواجهة الأمامية...")
        with open(frontend_env, "w") as f:
            f.write("""NEXT_PUBLIC_ENV_MODE="LOCAL"
NEXT_PUBLIC_SUPABASE_URL="http://localhost:8090"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
NEXT_PUBLIC_URL="http://localhost:3000"
OPENAI_API_KEY="sk-demo-key-for-local-development"
""")
        print_success("تم إنشاء ملف .env.local للواجهة الأمامية")

# تشغيل خدمات Docker الأساسية
def start_basic_services():
    print_header("تشغيل خدمات Redis وRabbitMQ الأساسية...")
    try:
        # إيقاف أي حاويات قيد التشغيل أولاً
        subprocess.run(["docker", "compose", "down"], 
                      shell=IS_WINDOWS, 
                      check=False)
        
        # تشغيل الحاويات الأساسية فقط
        result = subprocess.run(["docker", "compose", "up", "-d", "redis", "rabbitmq"],
                               shell=IS_WINDOWS,
                               capture_output=True,
                               text=True)
        
        if result.returncode == 0:
            print_success("تم تشغيل خدمات Redis وRabbitMQ بنجاح")
            return True
        else:
            print_error(f"فشل في تشغيل خدمات Redis وRabbitMQ: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"حدث خطأ أثناء تشغيل خدمات Redis وRabbitMQ: {str(e)}")
        return False

# تشغيل الخادم الخلفي بشكل محلي
def start_backend_local():
    print_header("تشغيل الخادم الخلفي...")
    backend_dir = ROOT_DIR / "backend"
    
    try:
        # تثبيت المكتبات المطلوبة إذا لزم الأمر
        pip_install = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=backend_dir,
            shell=IS_WINDOWS,
            capture_output=True,
            text=True
        )
        
        if pip_install.returncode != 0:
            print_warning(f"تحذير أثناء تثبيت متطلبات الخادم الخلفي: {pip_install.stderr}")
        
        # تشغيل الخادم الخلفي
        backend_cmd = [sys.executable, "-m", "uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
        print_success(f"جاري تشغيل الخادم الخلفي: {' '.join(backend_cmd)}")
        
        # استخدام Popen لتشغيل العملية في الخلفية
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=backend_dir,
            shell=IS_WINDOWS
        )
        
        # انتظار للتأكد من أن الخادم بدأ
        print_warning("انتظار بدء الخادم الخلفي...")
        time.sleep(3)
        
        return backend_process
    except Exception as e:
        print_error(f"فشل في تشغيل الخادم الخلفي: {str(e)}")
        return None

# تشغيل الواجهة الأمامية بشكل محلي
def start_frontend_local():
    print_header("تشغيل الواجهة الأمامية...")
    frontend_dir = ROOT_DIR / "frontend"
    
    try:
        # تثبيت حزم npm إذا لم تكن موجودة
        if not (frontend_dir / "node_modules").exists():
            print_warning("تثبيت مكتبات الواجهة الأمامية...")
            npm_install = subprocess.run(
                ["npm", "install"],
                cwd=frontend_dir,
                shell=IS_WINDOWS,
                capture_output=True,
                text=True
            )
            
            if npm_install.returncode != 0:
                print_error(f"فشل في تثبيت مكتبات الواجهة الأمامية: {npm_install.stderr}")
                return None
        
        # تشغيل الواجهة الأمامية
        print_success("جاري تشغيل الواجهة الأمامية...")
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            shell=IS_WINDOWS
        )
        
        return frontend_process
    except Exception as e:
        print_error(f"فشل في تشغيل الواجهة الأمامية: {str(e)}")
        return None

# الدالة الرئيسية
def main():
    print_header("بدء تشغيل مشروع سُنا بشكل مبسط...")
    
    # 1. إعداد ملفات البيئة
    setup_env_files()
    
    # 2. تشغيل خدمات الدعم الأساسية (Redis وRabbitMQ)
    services_running = start_basic_services()
    if not services_running:
        print_error("فشل في بدء الخدمات الأساسية. إنهاء العملية.")
        return
    
    # 3. تشغيل الخادم الخلفي محلياً
    backend_process = start_backend_local()
    if not backend_process:
        print_error("فشل في بدء الخادم الخلفي. الخدمات الأساسية لا تزال قيد التشغيل.")
        return
    
    # 4. تشغيل الواجهة الأمامية محلياً
    frontend_process = start_frontend_local()
    if not frontend_process:
        print_error("فشل في بدء الواجهة الأمامية. الخادم الخلفي والخدمات الأساسية لا تزال قيد التشغيل.")
        # إيقاف الخادم الخلفي
        if backend_process:
            backend_process.terminate()
        return
    
    # 5. عرض معلومات الوصول
    print_success("\n=================================")
    print_success("تم تشغيل مشروع سُنا بنجاح!")
    print_success("الواجهة الأمامية: http://localhost:3000")
    print_success("واجهة API الخلفية: http://localhost:8000")
    print_success("توثيق API: http://localhost:8000/docs")
    print_success("=================================\n")
    
    print("اضغط Ctrl+C لإيقاف جميع الخدمات...")
    
    try:
        # إبقاء السكريبت قيد التشغيل
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print_header("\nإيقاف الخدمات...")
        
        # إيقاف الواجهة الأمامية
        if frontend_process:
            frontend_process.terminate()
            print_success("تم إيقاف الواجهة الأمامية")
        
        # إيقاف الخادم الخلفي
        if backend_process:
            backend_process.terminate()
            print_success("تم إيقاف الخادم الخلفي")
        
        # إيقاف الخدمات الأساسية
        subprocess.run(["docker", "compose", "down"], shell=IS_WINDOWS)
        print_success("تم إيقاف الخدمات الأساسية")
        
        print_success("تم إيقاف جميع خدمات مشروع سُنا بنجاح!")

if __name__ == "__main__":
    main()
