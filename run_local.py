#!/usr/bin/env python3

import os
import platform
import subprocess
import sys
import time
import shutil
from pathlib import Path

IS_WINDOWS = platform.system() == 'Windows'
ROOT_DIR = Path(__file__).parent.absolute()

# يتحقق من وجود الأدوات المطلوبة
def check_requirements():
    print_header("التحقق من المتطلبات الأساسية...")
    
    # التحقق من وجود Python
    if sys.version_info < (3, 10):
        print_warning(f"إصدار Python الحالي {sys.version_info.major}.{sys.version_info.minor} أقدم من الإصدار الموصى به (3.10+)")
    else:
        print_success(f"Python {sys.version_info.major}.{sys.version_info.minor} موجود")
    
    # التحقق من وجود Docker
    docker_exists = shutil.which("docker") is not None
    if not docker_exists:
        print_error("Docker غير موجود. يرجى تثبيت Docker قبل المتابعة.")
        print_error("يمكنك تحميل Docker من: https://docs.docker.com/get-docker/")
        return False
    else:
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                shell=IS_WINDOWS
            )
            if result.returncode == 0:
                print_success(f"Docker موجود: {result.stdout.strip()}")
            else:
                print_warning("تم العثور على Docker ولكن هناك مشكلة في تشغيله")
        except Exception:
            print_warning("تم العثور على Docker ولكن هناك مشكلة في تشغيله")
    
    # التحقق من وجود Node.js و NPM
    npm_exists = shutil.which("npm") is not None
    node_exists = shutil.which("node") is not None
    
    if not (npm_exists and node_exists):
        print_error("Node.js و/أو NPM غير موجود. يرجى تثبيت Node.js قبل المتابعة.")
        print_error("يمكنك تحميل Node.js من: https://nodejs.org/")
        return False
    else:
        try:
            node_result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                shell=IS_WINDOWS
            )
            if node_result.returncode == 0:
                node_version = node_result.stdout.strip()
                print_success(f"Node.js موجود: {node_version}")
            
            npm_result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                text=True,
                shell=IS_WINDOWS
            )
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print_success(f"NPM موجود: {npm_version}")
        except Exception:
            print_warning("تم العثور على Node.js/NPM ولكن هناك مشكلة في تشغيله")
    
    return True

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message: str) -> None:
    print(f"{Colors.BLUE}{Colors.BOLD}[SUNA] {message}{Colors.ENDC}")

def print_success(message: str) -> None:
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str) -> None:
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")

def print_warning(message: str) -> None:
    print(f"{Colors.YELLOW}⚠ {message}{Colors.ENDC}")

def check_env_files():
    """Check and create necessary environment files if they don't exist."""
    print_header("Checking environment files...")
    
    # Check backend .env
    backend_env = ROOT_DIR / "backend" / ".env"
    if not backend_env.exists():
        backend_env_example = ROOT_DIR / "backend" / ".env.example"
        if backend_env_example.exists():
            print_warning("Backend .env file not found. Creating from .env.example...")
            with open(backend_env_example, "r") as example, open(backend_env, "w") as env:
                content = example.read()
                # Set minimal required values
                content = content.replace("ENV_MODE=", "ENV_MODE=local")
                content = content.replace("OPENAI_API_KEY=", "OPENAI_API_KEY=sk-demo-key-for-local-development")
                content = content.replace("MODEL_TO_USE=", "MODEL_TO_USE=gpt-3.5-turbo")
                env.write(content)
            print_success("Created backend .env file with minimal configuration")
        else:
            print_error("Backend .env.example not found. Cannot create .env file.")
    else:
        print_success("Backend .env file exists")
    
    # Check frontend .env.local
    frontend_env = ROOT_DIR / "frontend" / ".env.local"
    if not frontend_env.exists():
        frontend_env_example = ROOT_DIR / "frontend" / ".env.example"
        if frontend_env_example.exists():
            print_warning("Frontend .env.local file not found. Creating from .env.example...")
            with open(frontend_env_example, "r") as example, open(frontend_env, "w") as env:
                content = example.read()
                # Set minimal required values
                content = content.replace('NEXT_PUBLIC_ENV_MODE=""', 'NEXT_PUBLIC_ENV_MODE="LOCAL"')
                content = content.replace('NEXT_PUBLIC_BACKEND_URL=""', 'NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"')
                content = content.replace('NEXT_PUBLIC_URL=""', 'NEXT_PUBLIC_URL="http://localhost:3000"')
                content = content.replace('OPENAI_API_KEY=""', 'OPENAI_API_KEY="sk-demo-key-for-local-development"')
                env.write(content)
            print_success("Created frontend .env.local file with minimal configuration")
        else:
            print_error("Frontend .env.example not found. Cannot create .env.local file.")
    else:
        print_success("Frontend .env.local file exists")

def run_backend_services():
    """Run the backend services using Docker Compose."""
    print_header("Starting backend services (Redis, RabbitMQ, and FastAPI)...")
    try:
        result = subprocess.run(
            ["docker", "compose", "up", "-d", "redis", "rabbitmq", "backend"], 
            shell=IS_WINDOWS,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success("Backend services started successfully")
            return True
        else:
            print_error(f"Failed to start backend services: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Error starting backend services: {str(e)}")
        return False

def install_backend_dependencies():
    """Install backend Python dependencies."""
    print_header("تثبيت مكتبات Python للخلفية...")
    backend_dir = ROOT_DIR / "backend"
    
    # Check if requirements.txt exists
    if not (backend_dir / "requirements.txt").exists():
        print_error("ملف requirements.txt غير موجود في مجلد backend")
        return False
    
    try:
        # Create virtual environment if it doesn't exist
        venv_dir = backend_dir / "venv"
        if not venv_dir.exists():
            print_warning("إنشاء بيئة افتراضية Python (venv)...")
            
            # Create venv
            if IS_WINDOWS:
                venv_cmd = [sys.executable, "-m", "venv", str(venv_dir)]
            else:
                venv_cmd = ["python3", "-m", "venv", str(venv_dir)]
            
            venv_result = subprocess.run(
                venv_cmd,
                capture_output=True,
                text=True,
                shell=IS_WINDOWS
            )
            
            if venv_result.returncode != 0:
                print_error(f"فشل إنشاء البيئة الافتراضية: {venv_result.stderr}")
                return False
            else:
                print_success("تم إنشاء البيئة الافتراضية")
        
        # Install dependencies
        print_warning("تثبيت مكتبات Python من requirements.txt...")
        
        # Build pip command
        if IS_WINDOWS:
            pip_cmd = [os.path.join(venv_dir, "Scripts", "pip")]
        else:
            pip_cmd = [os.path.join(venv_dir, "bin", "pip")]
            
        pip_cmd.extend(["install", "-r", "requirements.txt"])
        
        pip_result = subprocess.run(
            pip_cmd,
            cwd=backend_dir,
            capture_output=True,
            text=True,
            shell=IS_WINDOWS
        )
        
        if pip_result.returncode != 0:
            print_error(f"فشل تثبيت مكتبات Python: {pip_result.stderr}")
            return False
        else:
            print_success("تم تثبيت مكتبات Python بنجاح")
            return True
            
    except Exception as e:
        print_error(f"حدث خطأ أثناء تثبيت مكتبات Python: {str(e)}")
        return False

def run_frontend_local():
    """Run the frontend locally using npm."""
    print_header("تشغيل خادم التطوير للواجهة الأمامية...")
    frontend_dir = ROOT_DIR / "frontend"
    
    # Check if package.json exists
    if not (frontend_dir / "package.json").exists():
        print_error("ملف package.json غير موجود في مجلد frontend")
        return False
    
    if not os.path.exists(frontend_dir / "node_modules"):
        print_warning("مكتبات الواجهة الأمامية غير مثبتة. جاري التثبيت...")
        try:
            # First, try with --legacy-peer-deps if the Node.js version is newer
            npm_install = subprocess.run(
                ["npm", "install", "--legacy-peer-deps"], 
                cwd=frontend_dir,
                shell=IS_WINDOWS,
                capture_output=True,
                text=True
            )
            
            # If failed, try without --legacy-peer-deps
            if npm_install.returncode != 0:
                print_warning("محاولة تثبيت المكتبات بدون --legacy-peer-deps...")
                npm_install = subprocess.run(
                    ["npm", "install"], 
                    cwd=frontend_dir,
                    shell=IS_WINDOWS,
                    capture_output=True,
                    text=True
                )
            
            if npm_install.returncode != 0:
                print_error(f"فشل تثبيت مكتبات الواجهة الأمامية: {npm_install.stderr}")
                return False
            else:
                print_success("تم تثبيت مكتبات الواجهة الأمامية بنجاح")
        except Exception as e:
            print_error(f"حدث خطأ أثناء تثبيت مكتبات الواجهة الأمامية: {str(e)}")
            return False
    
    print_success("بدء تشغيل خادم تطوير الواجهة الأمامية...")
    try:
        # Use subprocess.Popen to run in background
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"], 
            cwd=frontend_dir,
            shell=IS_WINDOWS
        )
        print_success("تم بدء تشغيل خادم تطوير الواجهة الأمامية")
        return frontend_process  # Return process so we can terminate it later
    except Exception as e:
        print_error(f"حدث خطأ أثناء بدء تشغيل خادم الواجهة الأمامية: {str(e)}")
        return False

def main():
    print_header("بدء تشغيل مشروع سُنا (SUNA) في وضع التطوير المحلي...")
    
    # التحقق من المتطلبات الأساسية
    if not check_requirements():
        print_error("لم يتم استيفاء المتطلبات الأساسية. يرجى تثبيت البرامج المطلوبة ثم إعادة المحاولة.")
        return
    
    # التحقق من ملفات البيئة
    check_env_files()
    
    # تثبيت مكتبات الخلفية (اختياري، قد لا نحتاجه إذا كنا نعتمد على حاويات Docker)
    # install_backend_dependencies()
    
    # تشغيل خدمات الخلفية
    backend_running = run_backend_services()
    
    # تشغيل الواجهة الأمامية محلياً
    if backend_running:
        frontend_process = run_frontend_local()
        if frontend_process:
            print_success("=================================")
            print_success("تم تشغيل مشروع سُنا (SUNA) بنجاح:")
            print_success("واجهة برمجة التطبيقات (API): http://localhost:8000")
            print_success("الواجهة الأمامية: http://localhost:3000")
            print_success("=================================")
            print("اضغط Ctrl+C لإيقاف الخدمات...")
            try:
                # إبقاء السكريبت قيد التشغيل
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print_header("جاري إيقاف الخدمات...")
                # إيقاف عملية الواجهة الأمامية
                if frontend_process:
                    try:
                        if IS_WINDOWS:
                            subprocess.run(["taskkill", "/F", "/T", "/PID", str(frontend_process.pid)], shell=True)
                        else:
                            frontend_process.terminate()
                    except Exception:
                        pass
                # إيقاف حاويات Docker
                subprocess.run(["docker", "compose", "down"], shell=IS_WINDOWS)
                print_success("تم إيقاف جميع الخدمات بنجاح")
        else:
            print_error("فشل بدء تشغيل الواجهة الأمامية. خدمات الخلفية لا تزال قيد التشغيل.")
            print_warning("يمكنك إيقاف خدمات الخلفية باستخدام الأمر: docker compose down")
    else:
        print_error("فشل بدء تشغيل خدمات الخلفية. تم إلغاء عملية التشغيل.")

if __name__ == "__main__":
    main()
