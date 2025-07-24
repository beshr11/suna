#!/usr/bin/env python3
"""
سكريبت تشغيل مبسط جداً لمشروع سُنا - يقوم بمحاكاة الخدمات الأساسية
"""

import os
import sys
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import json
import socket
from pathlib import Path

# تعريف الألوان لطباعة نصوص ملونة في الطرفية
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg):
    print(f"{Colors.BLUE}{Colors.BOLD}[SUNA] {msg}{Colors.ENDC}")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")

def is_port_in_use(port):
    """التحقق مما إذا كان المنفذ قيد الاستخدام بالفعل"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# معالج HTTP بسيط لمحاكاة API
class MockAPIHandler(SimpleHTTPRequestHandler):
    """معالج بسيط لمحاكاة API الخلفية"""
    
    def do_GET(self):
        """معالجة طلبات GET"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>SUNA Mock API</h1><p>API is running</p></body></html>')
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "ok", "version": "0.1.0"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """معالجة طلبات POST"""
        if self.path == '/api/v1/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "id": "mock-response-1",
                "content": "هذه استجابة توضيحية من واجهة برمجة التطبيقات المحاكاة. SUNA معد للتشغيل، لكن يجب إعداد بيئة التطوير الكاملة للوصول إلى وظائفه الكاملة.",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """كتم السجلات القياسية"""
        return

def create_demo_html():
    """إنشاء صفحة HTML توضيحية بسيطة"""
    html_content = """<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سُنا (SUNA) - واجهة توضيحية</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
            direction: rtl;
        }
        h1 {
            color: #0066cc;
            border-bottom: 2px solid #0066cc;
            padding-bottom: 10px;
        }
        h2 {
            color: #0099ff;
            margin-top: 30px;
        }
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background-color: white;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-input {
            display: flex;
            margin-top: 20px;
        }
        input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            margin-right: 10px;
            padding: 10px 15px;
            background-color: #0066cc;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0055aa;
        }
        .message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .user {
            background-color: #e6f2ff;
            border-right: 4px solid #0066cc;
        }
        .agent {
            background-color: #f0f0f0;
            border-right: 4px solid #666;
        }
        .actions {
            margin-top: 40px;
            display: flex;
            justify-content: space-between;
        }
    </style>
</head>
<body>
    <h1>سُنا (SUNA) - وكيل الذكاء الاصطناعي المفتوح المصدر</h1>
    <p>هذه واجهة توضيحية بسيطة لمشروع سُنا. للوصول إلى الوظائف الكاملة، يجب إعداد بيئة التطوير الكاملة.</p>
    
    <div class="chat-container">
        <h2>محادثة توضيحية</h2>
        <div id="chat-messages">
            <div class="message agent">
                <strong>سُنا:</strong> مرحبًا! أنا سُنا، وكيل الذكاء الاصطناعي المفتوح المصدر. كيف يمكنني مساعدتك اليوم؟
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="user-input" placeholder="اكتب رسالتك هنا..." />
            <button onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <div class="actions">
        <a href="https://github.com/Kortix-ai/Suna" target="_blank"><button>زيارة مستودع GitHub</button></a>
        <button onclick="showDocs()">عرض الوثائق</button>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            
            if (message) {
                // إضافة رسالة المستخدم
                const chatMessages = document.getElementById('chat-messages');
                const userDiv = document.createElement('div');
                userDiv.className = 'message user';
                userDiv.innerHTML = '<strong>أنت:</strong> ' + message;
                chatMessages.appendChild(userDiv);
                
                // محاكاة إرسال الرسالة إلى API
                fetch('http://localhost:8000/api/v1/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                })
                .then(response => response.json())
                .then(data => {
                    // إضافة رد الوكيل
                    const agentDiv = document.createElement('div');
                    agentDiv.className = 'message agent';
                    agentDiv.innerHTML = '<strong>سُنا:</strong> ' + data.content;
                    chatMessages.appendChild(agentDiv);
                })
                .catch(error => {
                    console.error('Error:', error);
                    // إضافة رسالة خطأ
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'message agent';
                    errorDiv.innerHTML = '<strong>سُنا:</strong> عذرًا، حدث خطأ في الاتصال بواجهة برمجة التطبيقات. تأكد من تشغيل الخادم الخلفي.';
                    chatMessages.appendChild(errorDiv);
                });
                
                // تفريغ حقل الإدخال
                input.value = '';
            }
        }
        
        function showDocs() {
            window.open('http://localhost:8000/docs', '_blank');
        }
        
        // السماح بإرسال الرسالة بالضغط على Enter
        document.getElementById('user-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""
    
    # إنشاء المجلدات اللازمة إذا لم تكن موجودة
    demo_dir = Path("demo_interface")
    demo_dir.mkdir(exist_ok=True)
    
    # كتابة ملف HTML
    with open(demo_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return str(demo_dir / "index.html")

def run_mock_api_server(port=8000):
    """تشغيل خادم API محاكي على المنفذ المحدد"""
    if is_port_in_use(port):
        print_error(f"المنفذ {port} مستخدم بالفعل. جاري المحاولة بمنفذ آخر...")
        port = 8080  # محاولة منفذ بديل
        
        if is_port_in_use(port):
            print_error(f"المنفذ {port} مستخدم أيضًا. يرجى إغلاق أي تطبيقات تستخدم هذه المنافذ.")
            return None
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockAPIHandler)
    
    print_success(f"تم تشغيل واجهة برمجة التطبيقات المحاكاة على المنفذ {port}")
    
    # تشغيل الخادم في مؤشر ترابط منفصل
    api_thread = threading.Thread(target=httpd.serve_forever)
    api_thread.daemon = True
    api_thread.start()
    
    return httpd, api_thread, port

def run_frontend_server(port=3000):
    """تشغيل خادم للواجهة الأمامية التوضيحية"""
    if is_port_in_use(port):
        print_error(f"المنفذ {port} مستخدم بالفعل. جاري المحاولة بمنفذ آخر...")
        port = 3001  # محاولة منفذ بديل
        
        if is_port_in_use(port):
            print_error(f"المنفذ {port} مستخدم أيضًا. يرجى إغلاق أي تطبيقات تستخدم هذه المنافذ.")
            return None
    
    # تغيير المجلد الحالي إلى مجلد العرض التوضيحي
    os.chdir("demo_interface")
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print_success(f"تم تشغيل الواجهة الأمامية التوضيحية على المنفذ {port}")
    
    # تشغيل الخادم في مؤشر ترابط منفصل
    frontend_thread = threading.Thread(target=httpd.serve_forever)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    return httpd, frontend_thread, port

def main():
    """الدالة الرئيسية لتشغيل العرض التوضيحي"""
    print_header("بدء تشغيل عرض توضيحي لمشروع سُنا")
    
    # إنشاء صفحة HTML توضيحية
    demo_page = create_demo_html()
    print_success(f"تم إنشاء صفحة العرض التوضيحي في: {demo_page}")
    
    # تشغيل واجهة برمجة التطبيقات المحاكاة
    api_result = run_mock_api_server()
    if not api_result:
        print_error("فشل تشغيل واجهة برمجة التطبيقات المحاكاة.")
        return
    
    api_server, api_thread, api_port = api_result
    
    # تشغيل خادم الواجهة الأمامية
    frontend_result = run_frontend_server()
    if not frontend_result:
        print_error("فشل تشغيل خادم الواجهة الأمامية.")
        api_server.shutdown()
        return
    
    frontend_server, frontend_thread, frontend_port = frontend_result
    
    # فتح المتصفح تلقائيًا
    demo_url = f"http://localhost:{frontend_port}"
    print_success(f"فتح العرض التوضيحي في المتصفح: {demo_url}")
    webbrowser.open(demo_url)
    
    print_header("\n=================================")
    print_success("تم تشغيل عرض توضيحي لمشروع سُنا بنجاح!")
    print_success(f"الواجهة الأمامية التوضيحية: http://localhost:{frontend_port}")
    print_success(f"واجهة برمجة التطبيقات المحاكاة: http://localhost:{api_port}")
    print_header("=================================\n")
    
    print("اضغط Ctrl+C لإيقاف العرض التوضيحي...")
    
    try:
        # إبقاء البرنامج قيد التشغيل
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print_header("\nإيقاف العرض التوضيحي...")
        
        # إيقاف الخوادم
        frontend_server.shutdown()
        api_server.shutdown()
        
        print_success("تم إيقاف جميع الخدمات بنجاح!")

if __name__ == "__main__":
    main()
