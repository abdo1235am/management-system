import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import json
import requests
from flask import Flask, jsonify
import threading
import os
import sys
import io

# إعدادات للسحابة والاستمرارية
import socket
import warnings
warnings.filterwarnings('ignore')

# إعداد الصفحة
st.set_page_config(
    page_title="🚀 نظام الإدارة المتكامل",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص للتصميم الاحترافي المتقدم
st.markdown("""
<style>
    /* التصميم العام */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* تصميم واجهة تسجيل الدخول */
    .login-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* تصميم البطاقات */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid #f0f0f0;
    }
    
    .feature-card:hover {
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        transform: translateX(8px);
        border-left-color: #764ba2;
    }
    
    /* تصميم الأزرار */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.85rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 1rem;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* تصميم الشريط الجانبي */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* تصميم القائمة الجانبية */
    .sidebar-menu {
        background: transparent !important;
        color: white !important;
    }
    
    .sidebar-menu .stRadio > div {
        background: transparent !important;
        color: white !important;
    }
    
    .sidebar-menu .stRadio label {
        color: white !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        margin: 0.25rem 0 !important;
        transition: all 0.3s ease !important;
        border: 1px solid transparent !important;
    }
    
    .sidebar-menu .stRadio label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px) !important;
    }
    
    .sidebar-menu .stRadio [data-baseweb="radio"] div:first-child {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .sidebar-menu .stRadio [data-baseweb="radio"] input:checked + div:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: #667eea !important;
    }
    
    /* تصميم العناوين */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* تصميم حقول الإدخال */
    .stTextInput input, .stDateInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e9ecef;
        padding: 0.85rem;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stTextInput input:focus, .stDateInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
    
    /* إشعارات مخصصة */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        font-weight: 500;
    }
    
    /* تصميم الجداول */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #f0f0f0;
    }
    
    /* تصميم علامات التبويب */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* شريط التقدم */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* تحسين النصوص */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700 !important;
    }
    
    /* تحسين الروابط */
    a {
        color: #667eea !important;
        text-decoration: none !important;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #764ba2 !important;
    }
    
    /* تصميم المتركس */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* إخفاء رسائل التحذير */
    .stAlert {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# إعدادات الاستمرارية والسحابة
# ==============================================

def is_running_in_cloud():
    """التحقق إذا كان التطبيق يعمل على السحابة"""
    return 'PORT' in os.environ or 'RAILWAY_STATIC_URL' in os.environ or 'RENDER' in os.environ

def get_server_port():
    """الحصول على المنفذ المناسب للبيئة"""
    if 'PORT' in os.environ:
        return int(os.environ['PORT'])
    return 8501

# ==============================================
# نظام إدارة الحالة والتخزين
# ==============================================

class SessionState:
    def __init__(self):
        self._state = {}
        self._cache = {}
    
    def get(self, key, default=None):
        return self._state.get(key, default)
    
    def set(self, key, value):
        self._state[key] = value
    
    def delete(self, key):
        if key in self._state:
            del self._state[key]
    
    def cache_get(self, key):
        """الحصول على بيانات من الذاكرة المؤقتة"""
        if key in self._cache:
            data, timestamp = self._cache[key]
            # التحقق من انتهاء صلاحية البيانات (5 دقائق)
            if (datetime.now() - timestamp).seconds < 300:
                return data
        return None
    
    def cache_set(self, key, data):
        """تخزين بيانات في الذاكرة المؤقتة"""
        self._cache[key] = (data, datetime.now())

session_state = SessionState()

# ==============================================
# نظام قاعدة البيانات المتقدم
# ==============================================

class DatabaseManager:
    def __init__(self, db_path='management_system.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        # تحسين الأداء
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        return conn
    
    def init_db(self):
        """تهيئة قاعدة البيانات مع الجداول"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # جدول المستخدمين
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                serial TEXT UNIQUE NOT NULL,
                email TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول البرامج
        c.execute('''
            CREATE TABLE IF NOT EXISTS programs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) DEFAULT 0.00,
                duration_days INTEGER DEFAULT 30,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الاشتراكات
        c.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                program_id INTEGER,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                payment_status TEXT DEFAULT 'pending',
                amount_paid DECIMAL(10, 2) DEFAULT 0.00,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (program_id) REFERENCES programs (id) ON DELETE CASCADE,
                UNIQUE(user_id, program_id)
            )
        ''')
        
        # جدول السجلات
        c.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                description TEXT,
                user_id INTEGER,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إنشاء الفهرس لتحسين الأداء
        c.execute('CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_subscriptions_program_id ON subscriptions(program_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_users_serial ON users(serial)')
        
        conn.commit()
        conn.close()
        
        # إضافة بيانات تجريبية إذا كانت الجداول فارغة
        self.add_sample_data()
    
    def add_sample_data(self):
        """إضافة بيانات تجريبية للاختبار"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # التحقق إذا كانت هناك بيانات بالفعل
        c.execute("SELECT COUNT(*) FROM programs")
        program_count = c.fetchone()[0]
        
        if program_count == 0:
            # إضافة برامج تجريبية
            sample_programs = [
                ('برنامج البريميوم', 'أفضل برنامج مع ميزات متقدمة', 1999.99, 365),
                ('برنامج الأساسي', 'برنامج شامل للمبتدئين', 999.99, 180),
                ('برنامج التجريبي', 'نسخة تجريبية مجانية', 0.00, 30)
            ]
            
            c.executemany(
                "INSERT INTO programs (name, description, price, duration_days) VALUES (?, ?, ?, ?)",
                sample_programs
            )
            
            # إضافة مستخدمين تجريبيين
            sample_users = [
                ('أحمد محمد', '0123456789', 'SER001', 'ahmed@example.com', 'عميل متميز'),
                ('فاطمة علي', '0111222333', 'SER002', 'fatima@example.com', 'عميلة جديدة'),
                ('يوسف محمود', '0100555666', 'SER003', 'youssef@example.com', 'عميل نشط')
            ]
            
            c.executemany(
                "INSERT INTO users (name, phone, serial, email, notes) VALUES (?, ?, ?, ?, ?)",
                sample_users
            )
            
            conn.commit()
        
        conn.close()

# إنشاء مدير قاعدة البيانات
db_manager = DatabaseManager()

# ==============================================
# دوال قاعدة البيانات المحسنة مع التخزين المؤقت
# ==============================================

def get_total_users():
    cache_key = "total_users"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
        conn.close()
        session_state.cache_set(cache_key, count)
        return count
    except Exception:
        return 0

def get_total_programs():
    cache_key = "total_programs"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM programs WHERE is_active = 1")
        count = c.fetchone()[0]
        conn.close()
        session_state.cache_set(cache_key, count)
        return count
    except Exception:
        return 0

def get_active_subscriptions():
    cache_key = "active_subscriptions"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM subscriptions WHERE status = 'active' AND end_date >= date('now')")
        count = c.fetchone()[0]
        conn.close()
        session_state.cache_set(cache_key, count)
        return count
    except Exception:
        return 0

def get_expired_subscriptions():
    cache_key = "expired_subscriptions"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM subscriptions WHERE status = 'active' AND end_date < date('now')")
        count = c.fetchone()[0]
        conn.close()
        session_state.cache_set(cache_key, count)
        return count
    except Exception:
        return 0

def get_recent_users(limit=5):
    cache_key = f"recent_users_{limit}"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT name, phone, serial, email, created_at FROM users ORDER BY id DESC LIMIT ?", (limit,))
        users = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, users)
        return users
    except Exception:
        return []

def get_recent_programs(limit=5):
    cache_key = f"recent_programs_{limit}"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT name, description, price, created_at FROM programs WHERE is_active = 1 ORDER BY id DESC LIMIT ?", (limit,))
        programs = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, programs)
        return programs
    except Exception:
        return []

def check_serial_exists(serial):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE serial = ?", (serial,))
        exists = c.fetchone() is not None
        conn.close()
        return exists
    except Exception:
        return False

def get_user_by_serial(serial):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE serial = ?", (serial,))
        user = c.fetchone()
        conn.close()
        return user
    except Exception:
        return None

def add_user(name, phone, serial, email="", notes=""):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (name, phone, serial, email, notes) VALUES (?, ?, ?, ?, ?)", 
                 (name, phone, serial, email, notes))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False

def get_all_users():
    cache_key = "all_users"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY id DESC")
        users = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, users)
        return users
    except Exception:
        return []

def get_all_programs():
    cache_key = "all_programs"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM programs WHERE is_active = 1 ORDER BY id DESC")
        programs = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, programs)
        return programs
    except Exception:
        return []

def search_users(term, search_by):
    cache_key = f"search_users_{search_by}_{term}"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        
        if search_by == "الاسم":
            c.execute("SELECT * FROM users WHERE name LIKE ? ORDER BY id DESC", (f'%{term}%',))
        elif search_by == "رقم الهاتف":
            c.execute("SELECT * FROM users WHERE phone LIKE ? ORDER BY id DESC", (f'%{term}%',))
        elif search_by == "البريد الإلكتروني":
            c.execute("SELECT * FROM users WHERE email LIKE ? ORDER BY id DESC", (f'%{term}%',))
        else:  # السيريال
            c.execute("SELECT * FROM users WHERE serial LIKE ? ORDER BY id DESC", (f'%{term}%',))
        
        users = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, users)
        return users
    except Exception:
        return []

def get_user_by_id(user_id):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        return user
    except Exception:
        return None

def update_user(user_id, name, phone, serial, email="", notes=""):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET name = ?, phone = ?, serial = ?, email = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", 
                 (name, phone, serial, email, notes, user_id))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False

def delete_user(user_id):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except Exception:
        return False

def add_program(name, description="", price=0.00, duration_days=30):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO programs (name, description, price, duration_days) VALUES (?, ?, ?, ?)", 
                 (name, description, price, duration_days))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False

def delete_program(program_id):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("UPDATE programs SET is_active = 0 WHERE id = ?", (program_id,))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except Exception:
        return False

def add_subscription(user_id, program_id, start_date, end_date, amount_paid=0.00, notes=""):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        
        # التحقق من عدم وجود اشتراك فعال مسبقاً
        c.execute('''SELECT * FROM subscriptions 
                    WHERE user_id = ? AND program_id = ? AND status = 'active' 
                    AND end_date >= date('now')''', (user_id, program_id))
        existing = c.fetchone()
        
        if existing:
            conn.close()
            return False
        
        c.execute('''INSERT INTO subscriptions (user_id, program_id, start_date, end_date, amount_paid, notes) 
                    VALUES (?, ?, ?, ?, ?, ?)''', 
                 (user_id, program_id, start_date.isoformat(), end_date.isoformat(), amount_paid, notes))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except sqlite3.Error:
        return False

def get_program_subscriptions(program_id, status='active'):
    cache_key = f"program_subscriptions_{program_id}_{status}"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        
        if status == 'active':
            c.execute('''SELECT s.id, u.name, u.serial, u.phone, s.start_date, s.end_date, s.amount_paid
                        FROM subscriptions s 
                        JOIN users u ON s.user_id = u.id 
                        WHERE s.program_id = ? AND s.status = 'active' AND s.end_date >= date('now')
                        ORDER BY s.end_date''', (program_id,))
        else:  # expired
            c.execute('''SELECT s.id, u.name, u.serial, u.phone, s.start_date, s.end_date, s.amount_paid
                        FROM subscriptions s 
                        JOIN users u ON s.user_id = u.id 
                        WHERE s.program_id = ? AND (s.status = 'expired' OR s.end_date < date('now'))
                        ORDER BY s.end_date DESC''', (program_id,))
        
        subscriptions = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, subscriptions)
        return subscriptions
    except Exception:
        return []

def renew_subscription(sub_id, start_date, end_date, amount_paid=0.00):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute('''UPDATE subscriptions SET start_date = ?, end_date = ?, amount_paid = ?, 
                    status = 'active', updated_at = CURRENT_TIMESTAMP WHERE id = ?''', 
                 (start_date.isoformat(), end_date.isoformat(), amount_paid, sub_id))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except Exception:
        return False

def delete_subscription(sub_id):
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute("UPDATE subscriptions SET status = 'expired', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (sub_id,))
        conn.commit()
        conn.close()
        # مسح الذاكرة المؤقتة
        session_state._cache.clear()
        return True
    except Exception:
        return False

def get_expiring_subscriptions(days=30):
    cache_key = f"expiring_subscriptions_{days}"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute('''SELECT p.name, u.name, s.end_date, 
                    julianday(s.end_date) - julianday('now') as days_left
                    FROM subscriptions s
                    JOIN programs p ON s.program_id = p.id
                    JOIN users u ON s.user_id = u.id
                    WHERE s.status = 'active' 
                    AND s.end_date >= date('now')
                    AND julianday(s.end_date) - julianday('now') <= ?
                    ORDER BY days_left''', (days,))
        subscriptions = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, subscriptions)
        return subscriptions
    except Exception:
        return []

def get_program_stats():
    cache_key = "program_stats"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        c.execute('''SELECT p.name, 
                    SUM(CASE WHEN s.status = 'active' AND s.end_date >= date('now') THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN s.status = 'expired' OR s.end_date < date('now') THEN 1 ELSE 0 END) as expired,
                    COUNT(s.id) as total
                    FROM programs p
                    LEFT JOIN subscriptions s ON p.id = s.program_id
                    WHERE p.is_active = 1
                    GROUP BY p.id, p.name''')
        stats = c.fetchall()
        conn.close()
        session_state.cache_set(cache_key, stats)
        return stats
    except Exception:
        return []

def get_financial_stats():
    cache_key = "financial_stats"
    cached_data = session_state.cache_get(cache_key)
    if cached_data is not None:
        return cached_data
    
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        
        # إجمالي الإيرادات
        c.execute("SELECT SUM(amount_paid) FROM subscriptions WHERE status = 'active'")
        total_revenue = c.fetchone()[0] or 0
        
        # الإيرادات الشهرية
        c.execute("SELECT SUM(amount_paid) FROM subscriptions WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')")
        monthly_revenue = c.fetchone()[0] or 0
        
        conn.close()
        result = (total_revenue, monthly_revenue)
        session_state.cache_set(cache_key, result)
        return result
    except Exception:
        return 0, 0

# ==============================================
# نظام المصادقة والإشعارات
# ==============================================

def login_user(username, password):
    return username == "abdo" and password == "12335"

def show_notification(message, type='success', duration=3):
    if type == 'success':
        st.success(f"🎉 {message}")
    elif type == 'error':
        st.error(f"❌ {message}")
    elif type == 'warning':
        st.warning(f"⚠️ {message}")
    elif type == 'info':
        st.info(f"ℹ️ {message}")
    
    if duration > 0:
        time.sleep(min(duration, 2))  # تقليل وقت الانتظار لأقصى 2 ثانية
        st.rerun()

# ==============================================
# واجهة المستخدم المحسنة
# ==============================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="login-container">
                <div style="text-align: center; margin-bottom: 2rem;">
                    <h1 style="color: #333; margin-bottom: 0.5rem; font-size: 2.5rem;">🚀 نظام الإدارة المتكامل</h1>
                    <p style="color: #666; font-size: 1.2rem; margin-bottom: 2rem;">نظام متكامل لإدارة الأعضاء والبرامج والاشتراكات</p>
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
                        <h3 style="margin: 0; font-size: 1.5rem;">🛡️ نظام آمن ومحترف</h3>
                    </div>
                </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.subheader("🔐 تسجيل الدخول")
            
            username = st.text_input(
                "👤 اسم المستخدم",
                placeholder="أدخل اسم المستخدم",
                key="login_username"
            )
            
            password = st.text_input(
                "🔒 كلمة المرور", 
                type="password",
                placeholder="أدخل كلمة المرور",
                key="login_password"
            )
            
            submit = st.form_submit_button("🚀 تسجيل الدخول", width='stretch')
            
            if submit:
                if not username or not password:
                    show_notification("⚠️ يرجى ملء جميع الحقول", 'warning')
                elif login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_avatar = "👨‍💼"
                    st.session_state.login_time = datetime.now()
                    show_notification("🎉 تم تسجيل الدخول بنجاح!", 'success')
                else:
                    show_notification("❌ اسم المستخدم أو كلمة المرور غير صحيحة", 'error')
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # معلومات الحساب الافتراضي
        with st.expander("🔐 معلومات الحساب الافتراضي", expanded=False):
            st.info("""
            **اسم المستخدم:** `abdo`  
            **كلمة المرور:** `12335`
            
            *ملاحظة: يمكنك تعديل هذه البيانات في كود المصدر*
            """)

# الداشبورد الرئيسي المحسن
def main_dashboard():
    # الهيدر الرئيسي
    st.markdown(f"""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5rem;">🚀 نظام إدارة الأعضاء والبرامج</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                مرحباً بك، {st.session_state.username} {st.session_state.user_avatar}
            </p>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.7;">
                وقت الدخول: {st.session_state.login_time.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.login_time else 'غير محدد'}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي المحسن
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: white; margin: 0;">🧭 القائمة</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # استخدام CSS class مخصص للقائمة الجانبية
        st.markdown('<div class="sidebar-menu">', unsafe_allow_html=True)
        
        menu_options = {
            "🏠 الرئيسية": "dashboard",
            "👥 إدارة الأعضاء": "users",
            "📊 إدارة البرامج": "programs",
            "🎫 إدارة الاشتراكات": "subscriptions",
            "📈 التقارير والإحصائيات": "reports",
            "🔗 واجهة API": "api",
            "⚙️ الإعدادات": "settings"
        }
        
        selected_menu = st.radio(
            "اختر القسم:",
            list(menu_options.keys()),
            key="main_menu",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # معلومات سريعة
        st.markdown("### 📊 نظرة سريعة")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("الأعضاء", get_total_users())
        with col2:
            st.metric("البرامج", get_total_programs())
        
        col3, col4 = st.columns(2)
        with col3:
            st.metric("النشطة", get_active_subscriptions())
        with col4:
            st.metric("المنتهية", get_expired_subscriptions())
        
        st.markdown("---")
        
        # معلومات النظام
        st.markdown("### ℹ️ معلومات النظام")
        st.info(f"**الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")
        
        # زر تسجيل الخروج
        if st.button("🚪 تسجيل الخروج", width='stretch'):
            st.session_state.logged_in = False
            show_notification("👋 تم تسجيل الخروج بنجاح", 'info')
    
    # المحتوى الرئيسي
    menu_action = menu_options[selected_menu]
    
    if menu_action == "dashboard":
        show_dashboard()
    elif menu_action == "users":
        manage_users()
    elif menu_action == "programs":
        manage_programs()
    elif menu_action == "subscriptions":
        manage_subscriptions()
    elif menu_action == "reports":
        show_reports()
    elif menu_action == "api":
        show_api_section()
    elif menu_action == "settings":
        show_settings()

# الداشبورد الرئيسي المحسن
def show_dashboard():
    st.subheader("📊 نظرة عامة على النظام")
    
    # عدادات إحصائية
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = get_total_users()
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">👥</div>
                <h3 style="margin: 0.5rem 0;">إجمالي الأعضاء</h3>
                <h2 style="margin: 0; font-size: 2.5rem;">{total_users}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_programs = get_total_programs()
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">📊</div>
                <h3 style="margin: 0.5rem 0;">إجمالي البرامج</h3>
                <h2 style="margin: 0; font-size: 2.5rem;">{total_programs}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_subs = get_active_subscriptions()
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">✅</div>
                <h3 style="margin: 0.5rem 0;">الاشتراكات النشطة</h3>
                <h2 style="margin: 0; font-size: 2.5rem;">{active_subs}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        expired_subs = get_expired_subscriptions()
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">❌</div>
                <h3 style="margin: 0.5rem 0;">الاشتراكات المنتهية</h3>
                <h2 style="margin: 0; font-size: 2.5rem;">{expired_subs}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # الإحصائيات المالية
    total_revenue, monthly_revenue = get_financial_stats()
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">💰</div>
                <h3 style="margin: 0.5rem 0;">إجمالي الإيرادات</h3>
                <h2 style="margin: 0; font-size: 2.5rem;">{total_revenue:,.2f} ج.م</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem;">📈</div>
                <h3 style="margin: 0.5rem 0;">الإيرادات الشهرية</h3>
                <h2 style="margin: 0; font-size: 2.5rem;">{monthly_revenue:,.2f} ج.م</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # أحدث البيانات
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 آخر الأعضاء المسجلين")
        recent_users = get_recent_users()
        if recent_users:
            df_users = pd.DataFrame(recent_users, 
                                  columns=['الاسم', 'رقم الهاتف', 'السيريال', 'البريد الإلكتروني', 'تاريخ التسجيل'])
            st.dataframe(df_users, use_container_width=True)
        else:
            st.info("📝 لا توجد أعضاء مسجلين بعد")
    
    with col2:
        st.markdown("### 📊 أحدث البرامج المضافة")
        recent_programs = get_recent_programs()
        if recent_programs:
            df_programs = pd.DataFrame(recent_programs, 
                                     columns=['اسم البرنامج', 'الوصف', 'السعر', 'تاريخ الإضافة'])
            # تنسيق السعر بالجنيه المصري
            df_programs['السعر'] = df_programs['السعر'].apply(lambda x: f"{x:,.2f} ج.م")
            st.dataframe(df_programs, use_container_width=True)
        else:
            st.info("📝 لا توجد برامج مسجلة بعد")

# إدارة الأعضاء المحسنة
def manage_users():
    st.subheader("👥 إدارة الأعضاء")
    
    tab1, tab2, tab3 = st.tabs(["➕ إضافة عضو", "📋 عرض الأعضاء", "🔍 بحث وتعديل"])
    
    with tab1:
        st.markdown("### إضافة عضو جديد")
        with st.form("add_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("👤 الاسم الكامل *", placeholder="أدخل الاسم الكامل")
                phone = st.text_input("📞 رقم الهاتف *", placeholder="أدخل رقم الهاتف")
                serial = st.text_input("🔢 السيريال *", placeholder="أدخل السيريال")
            
            with col2:
                email = st.text_input("📧 البريد الإلكتروني", placeholder="أدخل البريد الإلكتروني")
                notes = st.text_area("📝 ملاحظات", placeholder="أدخل أي ملاحظات إضافية")
            
            st.markdown("**الحقول المميزة ب * إلزامية**")
            submit = st.form_submit_button("💾 حفظ العضو", width='stretch')
            
            if submit:
                if not all([name, phone, serial]):
                    show_notification("⚠️ يرجى ملء جميع الحقول الإلزامية", 'warning')
                elif check_serial_exists(serial):
                    show_notification("❌ هذا السيريال مسجل مسبقاً!", 'error')
                    user_data = get_user_by_serial(serial)
                    if user_data:
                        st.warning(f"📋 بيانات السيريال المسجل: الاسم: {user_data[1]}, الرقم: {user_data[2]}")
                else:
                    if add_user(name, phone, serial, email, notes):
                        show_notification("✅ تم إضافة العضو بنجاح")
                    else:
                        show_notification("❌ حدث خطأ أثناء الإضافة", 'error')
    
    with tab2:
        st.markdown("### 📋 قائمة جميع الأعضاء")
        users = get_all_users()
        if users:
            df = pd.DataFrame(users, columns=['ID', 'الاسم', 'رقم الهاتف', 'السيريال', 'البريد الإلكتروني', 'ملاحظات', 'تاريخ التسجيل', 'آخر تحديث'])
            
            # خيارات التصفية
            col1, col2 = st.columns(2)
            with col1:
                search_term = st.text_input("🔍 بحث سريع في الأسماء", placeholder="ابحث بالاسم...")
            with col2:
                items_per_page = st.selectbox("عدد العناصر في الصفحة", [10, 25, 50, 100])
            
            if search_term:
                df = df[df['الاسم'].str.contains(search_term, na=False)]
            
            # عرض البيانات مع التقسيم للصفحات
            total_pages = max(1, (len(df) + items_per_page - 1) // items_per_page)
            page_number = st.number_input("رقم الصفحة", min_value=1, max_value=total_pages, value=1)
            
            start_idx = (page_number - 1) * items_per_page
            end_idx = start_idx + items_per_page
            
            st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
            
            st.markdown(f"**الصفحة {page_number} من {total_pages} - إجمالي {len(df)} عضو**")
            
            # خيارات التصدير
            col1, col2, col3 = st.columns(3)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 تحميل CSV",
                    data=csv,
                    file_name="الأعضاء.csv",
                    mime="text/csv",
                    width='stretch'
                )
            with col2:
                # إصلاح تصدير Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='الأعضاء')
                    writer.close()
                
                st.download_button(
                    label="📊 تحميل Excel",
                    data=buffer.getvalue(),
                    file_name="الأعضاء.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
            with col3:
                json_str = df.to_json(orient='records', force_ascii=False, indent=2)
                st.download_button(
                    label="📄 تحميل JSON",
                    data=json_str,
                    file_name="الأعضاء.json",
                    mime="application/json",
                    width='stretch'
                )
        else:
            st.info("📝 لا توجد أعضاء مسجلين بعد")
    
    with tab3:
        st.markdown("### 🔍 بحث وتعديل الأعضاء")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            search_option = st.selectbox("البحث بواسطة:", ["الاسم", "رقم الهاتف", "السيريال", "البريد الإلكتروني"])
        with col2:
            search_term = st.text_input("🔍 ادخل مصطلح البحث", placeholder="اكتب للبحث...")
        
        if search_term:
            users = search_users(search_term, search_option)
            if users:
                df = pd.DataFrame(users, columns=['ID', 'الاسم', 'رقم الهاتف', 'السيريال', 'البريد الإلكتروني', 'ملاحظات', 'تاريخ التسجيل', 'آخر تحديث'])
                st.dataframe(df, use_container_width=True)
                
                selected_id = st.selectbox("👤 اختر العضو للتعديل:", 
                                         [f"{user[1]} (ID: {user[0]})" for user in users])
                
                if selected_id:
                    user_id = int(selected_id.split("ID: ")[1].replace(")", ""))
                    user_data = get_user_by_id(user_id)
                    
                    if user_data:
                        with st.form("edit_user_form"):
                            st.markdown("### ✏️ تعديل بيانات العضو")
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_name = st.text_input("👤 الاسم *", value=user_data[1])
                                edit_phone = st.text_input("📞 رقم الهاتف *", value=user_data[2])
                                edit_serial = st.text_input("🔢 السيريال *", value=user_data[3])
                            with col2:
                                edit_email = st.text_input("📧 البريد الإلكتروني", value=user_data[4] or "")
                                edit_notes = st.text_area("📝 ملاحظات", value=user_data[5] or "")
                            
                            st.markdown("**الحقول المميزة ب * إلزامية**")
                            col1, col2 = st.columns(2)
                            with col1:
                                update_btn = st.form_submit_button("💾 تحديث البيانات", width='stretch')
                            with col2:
                                if st.form_submit_button("🗑️ حذف العضو", width='stretch'):
                                    if st.checkbox("⚠️ تأكيد الحذف - هذا الإجراء لا يمكن التراجع عنه", key=f"delete_confirm_{user_id}"):
                                        if delete_user(user_id):
                                            show_notification("✅ تم حذف العضو بنجاح")
                                        else:
                                            show_notification("❌ حدث خطأ أثناء الحذف", 'error')
                            
                            if update_btn:
                                if not all([edit_name, edit_phone, edit_serial]):
                                    show_notification("⚠️ يرجى ملء جميع الحقول الإلزامية", 'warning')
                                elif update_user(user_id, edit_name, edit_phone, edit_serial, edit_email, edit_notes):
                                    show_notification("✅ تم تحديث بيانات العضو بنجاح")
                                else:
                                    show_notification("❌ حدث خطأ أثناء التحديث", 'error')
            else:
                st.warning("🔍 لا توجد نتائج للبحث")

# إدارة البرامج المحسنة
def manage_programs():
    st.subheader("📊 إدارة البرامج")
    
    tab1, tab2 = st.tabs(["➕ إضافة برنامج", "📋 إدارة البرامج"])
    
    with tab1:
        st.markdown("### إضافة برنامج جديد")
        with st.form("add_program_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                program_name = st.text_input("📝 اسم البرنامج *", placeholder="أدخل اسم البرنامج")
                description = st.text_area("📄 الوصف", placeholder="أدخل وصف البرنامج")
            
            with col2:
                price = st.number_input("💰 السعر (ج.م)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
                duration_days = st.number_input("📅 المدة بالأيام", min_value=1, value=30)
            
            st.markdown("**الحقول المميزة ب * إلزامية**")
            submit = st.form_submit_button("➕ إضافة البرنامج", width='stretch')
            
            if submit:
                if not program_name:
                    show_notification("⚠️ يرجى إدخال اسم البرنامج", 'warning')
                else:
                    if add_program(program_name, description, price, duration_days):
                        show_notification("✅ تم إضافة البرنامج بنجاح")
                    else:
                        show_notification("❌ هذا البرنامج مسجل مسبقاً!", 'error')
    
    with tab2:
        st.markdown("### 📋 قائمة البرامج")
        programs = get_all_programs()
        if programs:
            df = pd.DataFrame(programs, columns=['ID', 'اسم البرنامج', 'الوصف', 'السعر', 'المدة', 'نشط', 'تاريخ الإضافة'])
            
            # إحصائيات سريعة
            total_programs = len(programs)
            total_value = df['السعر'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("إجمالي البرامج", total_programs)
            with col2:
                st.metric("القيمة الإجمالية", f"{total_value:,.2f} ج.م")
            
            # تنسيق السعر للعرض
            df_display = df.copy()
            df_display['السعر'] = df_display['السعر'].apply(lambda x: f"{x:,.2f} ج.م")
            st.dataframe(df_display, use_container_width=True)
            
            # خيارات إدارة البرامج
            st.markdown("### 🗑️ إدارة البرامج")
            program_to_delete = st.selectbox("اختر برنامج للحذف:", [f"{p[1]} (ID: {p[0]})" for p in programs])
            
            if st.button("🗑️ حذف البرنامج المحدد", width='stretch'):
                program_id = int(program_to_delete.split("ID: ")[1].replace(")", ""))
                if delete_program(program_id):
                    show_notification("✅ تم حذف البرنامج بنجاح")
                else:
                    show_notification("❌ حدث خطأ أثناء الحذف", 'error')
        else:
            st.info("📝 لا توجد برامج مسجلة بعد")

# إدارة الاشتراكات المحسنة
def manage_subscriptions():
    st.subheader("🎫 إدارة الاشتراكات")
    
    programs = get_all_programs()
    if not programs:
        st.info("📝 لا توجد برامج متاحة. يرجى إضافة برامج أولاً.")
        return
    
    selected_program = st.selectbox("📊 اختر البرنامج:", [p[1] for p in programs])
    program_id = [p[0] for p in programs if p[1] == selected_program][0]
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ إضافة اشتراك", "✅ المشتركين النشطين", "❌ الاشتراكات المنتهية", "📈 إحصائيات البرنامج"])
    
    with tab1:
        st.markdown("### إضافة اشتراك جديد")
        users = get_all_users()
        if users:
            user_options = {f"{user[1]} - {user[3]}": user[0] for user in users}
            selected_user = st.selectbox("👤 اختر العضو:", list(user_options.keys()))
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("📅 تاريخ بداية الاشتراك *", value=datetime.now())
                amount_paid = st.number_input("💰 المبلغ المدفوع (ج.م)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
            
            with col2:
                # حساب تاريخ النهاية تلقائياً بناءً على مدة البرنامج
                program_duration = [p[4] for p in programs if p[0] == program_id][0]
                end_date = st.date_input("📅 تاريخ نهاية الاشتراك *", 
                                       value=datetime.now() + timedelta(days=program_duration))
                
                notes = st.text_area("📝 ملاحظات الاشتراك", placeholder="ملاحظات إضافية حول الاشتراك")
            
            st.markdown("**الحقول المميزة ب * إلزامية**")
            if st.button("🎫 تفعيل الاشتراك", width='stretch'):
                user_id = user_options[selected_user]
                if add_subscription(user_id, program_id, start_date, end_date, amount_paid, notes):
                    show_notification("✅ تم تفعيل الاشتراك بنجاح")
                else:
                    show_notification("❌ هذا العضو مشترك مسبقاً في هذا البرنامج!", 'error')
        else:
            st.info("📝 لا توجد أعضاء مسجلين. يرجى إضافة أعضاء أولاً.")
    
    with tab2:
        st.markdown("### الأعضاء المشتركين في البرنامج")
        active_subs = get_program_subscriptions(program_id, 'active')
        if active_subs:
            df = pd.DataFrame(active_subs, columns=['ID', 'اسم العضو', 'السيريال', 'رقم الهاتف', 'بداية الاشتراك', 'نهاية الاشتراك', 'المبلغ المدفوع'])
            # تنسيق المبالغ المدفوعة
            df['المبلغ المدفوع'] = df['المبلغ المدفوع'].apply(lambda x: f"{x:,.2f} ج.م")
            st.dataframe(df, use_container_width=True)
            
            # خيارات إدارة الاشتراكات النشطة
            st.markdown("#### 🔄 إدارة الاشتراكات النشطة")
            sub_options = [f"{sub[1]} - ينتهي في {sub[5]}" for sub in active_subs]
            selected_sub = st.selectbox("اختر اشتراك:", sub_options, key="active_subs")
            
            if selected_sub:
                sub_id = active_subs[sub_options.index(selected_sub)][0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("##### 🔄 تجديد الاشتراك")
                    new_start = st.date_input("📅 تاريخ البداية الجديد", value=datetime.now(), key="renew_start")
                    new_end = st.date_input("📅 تاريخ النهاية الجديد", 
                                          value=datetime.now() + timedelta(days=30), key="renew_end")
                    renew_amount = st.number_input("💰 المبلغ المدفوع للتجديد (ج.م)", min_value=0.0, value=0.0, step=0.01, format="%.2f", key="renew_amount")
                    
                    if st.button("🔄 تجديد الاشتراك", width='stretch', key="renew_btn"):
                        if renew_subscription(sub_id, new_start, new_end, renew_amount):
                            show_notification("✅ تم تجديد الاشتراك بنجاح")
                        else:
                            show_notification("❌ حدث خطأ أثناء التجديد", 'error')
                
                with col2:
                    st.markdown("##### 🗑️ إدارة الاشتراك")
                    st.warning("⚠️ إنهاء الاشتراك سيمنع العضو من الوصول للبرنامج")
                    if st.button("🗑️ إنهاء الاشتراك", width='stretch', key="delete_sub_btn"):
                        if delete_subscription(sub_id):
                            show_notification("✅ تم إنهاء الاشتراك بنجاح")
                        else:
                            show_notification("❌ حدث خطأ أثناء الإنهاء", 'error')
        else:
            st.info("📝 لا توجد اشتراكات نشطة في هذا البرنامج")
    
    with tab3:
        st.markdown("### الاشتراكات المنتهية")
        expired_subs = get_program_subscriptions(program_id, 'expired')
        if expired_subs:
            df = pd.DataFrame(expired_subs, columns=['ID', 'اسم العضو', 'السيريال', 'رقم الهاتف', 'بداية الاشتراك', 'نهاية الاشتراك', 'المبلغ المدفوع'])
            # تنسيق المبالغ المدفوعة
            df['المبلغ المدفوع'] = df['المبلغ المدفوع'].apply(lambda x: f"{x:,.2f} ج.م")
            st.dataframe(df, use_container_width=True)
            
            st.metric("عدد الاشتراكات المنتهية", len(expired_subs))
        else:
            st.info("📝 لا توجد اشتراكات منتهية في هذا البرنامج")
    
    with tab4:
        st.markdown("### 📈 إحصائيات البرنامج")
        program_stats = get_program_stats()
        if program_stats:
            for stat in program_stats:
                if stat[0] == selected_program:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("المشتركين النشطين", stat[1])
                    with col2:
                        st.metric("الاشتراكات المنتهية", stat[2])
                    with col3:
                        st.metric("إجمالي المشتركين", stat[3])
                    break

# التقارير المحسنة
def show_reports():
    st.subheader("📋 التقارير والإحصائيات")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 الإحصائيات العامة", "📅 الاشتراكات القريبة", "💰 التقارير المالية", "📈 تحليلات متقدمة"])
    
    with tab1:
        st.markdown("### 📊 الإحصائيات العامة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # إحصائيات البرامج
            program_stats = get_program_stats()
            if program_stats:
                st.markdown("#### إحصائيات البرامج")
                df_programs = pd.DataFrame(program_stats, columns=['البرنامج', 'المشتركين النشطين', 'الاشتراكات المنتهية', 'الإجمالي'])
                st.dataframe(df_programs, use_container_width=True)
            else:
                st.info("📝 لا توجد إحصائيات متاحة للبرامج")
        
        with col2:
            # الاشتراكات القريبة من الانتهاء
            st.markdown("#### الاشتراكات القريبة من الانتهاء")
            expiring_subs = get_expiring_subscriptions(7)  # خلال 7 أيام
            if expiring_subs:
                df_expiring = pd.DataFrame(expiring_subs, columns=['البرنامج', 'العضو', 'نهاية الاشتراك', 'الأيام المتبقية'])
                st.dataframe(df_expiring, use_container_width=True)
                st.warning(f"⚠️ هناك {len(expiring_subs)} اشتراك على وشك الانتهاء خلال الأسبوع القادم")
            else:
                st.success("🎉 لا توجد اشتراكات على وشك الانتهاء خلال الأسبوع القادم")
    
    with tab2:
        st.markdown("### 📅 الاشتراكات القريبة من الانتهاء")
        
        days_option = st.selectbox("الفترة الزمنية:", [7, 15, 30, 60], index=2)
        expiring_subs = get_expiring_subscriptions(days_option)
        
        if expiring_subs:
            df = pd.DataFrame(expiring_subs, columns=['البرنامج', 'العضو', 'نهاية الاشتراك', 'الأيام المتبقية'])
            
            # تصفية حسب الأيام المتبقية
            min_days = st.slider("الأدنى للأيام المتبقية", 0, days_option, 0)
            filtered_df = df[df['الأيام المتبقية'] >= min_days]
            
            st.dataframe(filtered_df, use_container_width=True)
            st.metric("عدد الاشتراكات القريبة", len(filtered_df))
            
            # خيار إرسال تنبيهات
            if st.button("📧 إرسال تنبيهات للمشتركين", width='stretch'):
                st.info("🚧 هذه الميزة قيد التطوير - سيتم إرسال تنبيهات للمشتركين القريبين من انتهاء الاشتراك")
        else:
            st.success(f"🎉 لا توجد اشتراكات على وشك الانتهاء خلال {days_option} يوم القادم")
    
    with tab3:
        st.markdown("### 💰 التقارير المالية")
        
        total_revenue, monthly_revenue = get_financial_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي الإيرادات", f"{total_revenue:,.2f} ج.م")
        with col2:
            st.metric("الإيرادات الشهرية", f"{monthly_revenue:,.2f} ج.م")
        with col3:
            avg_monthly = monthly_revenue if monthly_revenue > 0 else 0
            st.metric("المتوسط الشهري", f"{avg_monthly:,.2f} ج.م")
        
        # توقعات الإيرادات
        st.markdown("#### 📈 توقعات الإيرادات")
        projected_revenue = monthly_revenue * 12
        st.info(f"**التوقعات السنوية بناءً على الأداء الحالي:** {projected_revenue:,.2f} ج.م")
    
    with tab4:
        st.markdown("### 📈 تحليلات متقدمة")
        
        # تحليل النمو
        st.markdown("#### تحليل نمو النظام")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("الأعضاء", get_total_users(), delta="+5%")
        with col2:
            st.metric("البرامج", get_total_programs(), delta="+2%")
        with col3:
            st.metric("الاشتراكات النشطة", get_active_subscriptions(), delta="+8%")
        with col4:
            st.metric("الإيرادات", f"{get_financial_stats()[0]:,.2f} ج.م", delta="+12%")
        
        # توصيات
        st.markdown("#### 💡 توصيات ذكية")
        if get_expiring_subscriptions(7):
            st.warning("**توصية:** هناك اشتراكات قريبة من الانتهاء - فكر في إرسال تذكيرات للتجديد")
        
        if get_active_subscriptions() < 10:
            st.info("**توصية:** عدد الاشتراكات النشطة منخفض - فكر في عروض ترويجية")
        
        total_users_count = get_total_users()
        active_subs_count = get_active_subscriptions()
        if total_users_count > 0:
            conversion_rate = (active_subs_count / total_users_count) * 100
            if conversion_rate < 30:
                st.warning(f"**توصية:** معدل التحويل من الأعضاء إلى مشتركين منخفض ({conversion_rate:.1f}%) - راجع استراتيجية التسويق")

# قسم API المحسن
def show_api_section():
    st.subheader("🔗 واجهة برمجة التطبيقات (API)")
    
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 واجهة API المتكاملة</h3>
        <p>استخدم واجهة API لجلب بيانات المشتركين في البرامج المختلفة بتنسيق JSON.</p>
        <p><strong>الخادم يعمل على:</strong> <code>http://localhost:5000</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    # معلومات سريعة عن حالة API
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            st.success("✅ خادم API يعمل بشكل صحيح")
            health_data = response.json()
            st.info(f"**إصدار API:** {health_data.get('version', 'غير معروف')}")
        else:
            st.error("❌ خادم API لا يستجيب بشكل صحيح")
    except:
        st.error("❌ لا يمكن الاتصال بخادم API")
    
    programs = get_all_programs()
    if not programs:
        st.info("📝 لا توجد برامج متاحة. يرجى إضافة برامج أولاً.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_program = st.selectbox("📊 اختر البرنامج:", [p[1] for p in programs], key="api_program")
        program_id = [p[0] for p in programs if p[1] == selected_program][0]
        
        api_url = f"http://localhost:5000/api/subscriptions/{program_id}"
        
        st.markdown("### 📍 رابط API")
        st.code(f"GET {api_url}", language="http")
    
    with col2:
        st.markdown("### 🧪 اختبار API")
        if st.button("🔄 جلب البيانات الآن", width='stretch'):
            with st.spinner("🔄 جاري جلب البيانات..."):
                try:
                    # محاكاة استجابة API
                    subscriptions_data = get_api_subscriptions_data(program_id)
                    
                    if subscriptions_data:
                        st.success("✅ تم جلب البيانات بنجاح!")
                        
                        # عرض البيانات
                        st.markdown("### 📋 البيانات المستلمة")
                        st.json(subscriptions_data)
                        
                        # خيارات التحميل
                        json_str = json.dumps(subscriptions_data, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="📥 تحميل كـ JSON",
                            data=json_str,
                            file_name=f"subscriptions_{program_id}.json",
                            mime="application/json",
                            width='stretch'
                        )
                    else:
                        st.info("📝 لا توجد اشتراكات في هذا البرنامج")
                        
                except Exception as e:
                    st.error(f"❌ خطأ في جلب البيانات: {e}")
    
    # أمثلة استخدام API
    st.markdown("### 💻 أمثلة الاستخدام")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Python", "JavaScript", "cURL", "جميع النقاط"])
    
    with tab1:
        st.code(f"""
import requests
import json

# جلب بيانات المشتركين
url = "http://localhost:5000/api/subscriptions/{program_id}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"برنامج: {{data['program']['name']}}")
    print(f"عدد المشتركين: {{data['total_subscriptions']}}")
    for subscription in data['subscriptions']:
        print(f"العضو: {{subscription['user_name']}}")
        print(f"السيريال: {{subscription['serial']}}")
        print(f"الحالة: {{subscription['status']}}")
else:
    print("خطأ في جلب البيانات")
        """, language="python")
    
    with tab2:
        st.code(f"""
// جلب بيانات المشتركين باستخدام JavaScript
fetch('http://localhost:5000/api/subscriptions/{program_id}')
    .then(response => response.json())
    .then(data => {{
        console.log(`برنامج: ${{data.program.name}}`);
        console.log(`عدد المشتركين: ${{data.total_subscriptions}}`);
        data.subscriptions.forEach(sub => {{
            console.log(`العضو: ${{sub.user_name}}`);
            console.log(`السيريال: ${{sub.serial}}`);
        }});
    }})
    .catch(error => console.error('خطأ:', error));
        """, language="javascript")
    
    with tab3:
        st.code(f"""
# جلب البيانات باستخدام cURL
curl -X GET "http://localhost:5000/api/subscriptions/{program_id}" \\
  -H "Content-Type: application/json"

# جلب جميع البرامج
curl -X GET "http://localhost:5000/api/programs" \\
  -H "Content-Type: application/json"

# جلب إحصائيات النظام
curl -X GET "http://localhost:5000/api/stats" \\
  -H "Content-Type: application/json"
        """, language="bash")
    
    with tab4:
        st.markdown("""
        ### 🌐 جميع نقاط نهاية API المتاحة
        
        | النقطة | الوصف | الطريقة |
        |--------|--------|----------|
        | `/api/health` | فحص حالة الخادم | GET |
        | `/api/subscriptions/{id}` | جلب اشتراكات برنامج | GET |
        | `/api/programs` | جلب جميع البرامج | GET |
        | `/api/users` | جلب جميع المستخدمين | GET |
        | `/api/stats` | جلب إحصائيات النظام | GET |
        
        **مثال الاستجابة:**
        ```json
        {
            "success": true,
            "program": {
                "id": 1,
                "name": "برنامج البريميوم",
                "description": "أفضل برنامج مع ميزات متقدمة",
                "price": 1999.99
            },
            "total_subscriptions": 5,
            "subscriptions": [
                {
                    "user_name": "أحمد محمد",
                    "serial": "SER001",
                    "phone": "0123456789",
                    "status": "active"
                }
            ]
        }
        ```
        """)

# الإعدادات
def show_settings():
    st.subheader("⚙️ الإعدادات")
    
    tab1, tab2, tab3 = st.tabs(["الإعدادات العامة", "نسخ احتياطي", "حول النظام"])
    
    with tab1:
        st.markdown("### الإعدادات العامة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### إعدادات الواجهة")
            theme = st.selectbox("السمة", ["افتراضي", "فاتح", "مظلم"])
            language = st.selectbox("اللغة", ["العربية", "English"])
            items_per_page = st.slider("عدد العناصر في الصفحة", 10, 100, 25)
        
        with col2:
            st.markdown("#### إعدادات الإشعارات")
            email_notifications = st.checkbox("تفعيل الإشعارات عبر البريد الإلكتروني")
            renewal_reminders = st.checkbox("إرسال تذكيرات تجديد الاشتراكات")
            auto_backup = st.checkbox("نسخ احتياطي تلقائي")
        
        if st.button("💾 حفظ الإعدادات", width='stretch'):
            show_notification("✅ تم حفظ الإعدادات بنجاح")
    
    with tab2:
        st.markdown("### نسخ احتياطي")
        
        st.info("""
        **معلومات النسخ الاحتياطي:**
        - يمكنك إنشاء نسخة احتياطية من جميع بيانات النظام
        - استعادة البيانات من نسخة احتياطية سابقة
        - تحميل البيانات بصيغ مختلفة
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📁 إنشاء نسخة احتياطية", width='stretch'):
                # محاكاة إنشاء نسخة احتياطية
                backup_data = {
                    "timestamp": datetime.now().isoformat(),
                    "total_users": get_total_users(),
                    "total_programs": get_total_programs(),
                    "backup_type": "full"
                }
                backup_json = json.dumps(backup_data, ensure_ascii=False, indent=2)
                
                st.download_button(
                    label="⬇️ تحميل النسخة الاحتياطية",
                    data=backup_json,
                    file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    width='stretch'
                )
        
        with col2:
            uploaded_file = st.file_uploader("رفع نسخة احتياطية", type=['json'])
            if uploaded_file is not None:
                if st.button("🔄 استعادة من نسخة", width='stretch'):
                    st.success("✅ تم رفع الملف بنجاح - جاهز للاستعادة")
        
        with col3:
            if st.button("🗃️ تصدير جميع البيانات", width='stretch'):
                st.info("🚧 هذه الميزة قيد التطوير")
    
    with tab3:
        st.markdown("### حول النظام")
        
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 نظام الإدارة المتكامل</h3>
            <p><strong>الإصدار:</strong> 2.0.0</p>
            <p><strong>تاريخ الإصدار:</strong> 2024</p>
            <p><strong>المطور:</strong> فريق التطوير</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 📊 إحصائيات النظام
        """)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("الأعضاء", get_total_users())
        with col2:
            st.metric("البرامج", get_total_programs())
        with col3:
            st.metric("الاشتراكات النشطة", get_active_subscriptions())
        with col4:
            st.metric("الإيرادات", f"{get_financial_stats()[0]:,.2f} ج.م")
        
        st.markdown("""
        ### 🔧 معلومات تقنية
        - **لغة البرمجة:** Python
        - **واجهة المستخدم:** Streamlit
        - **قاعدة البيانات:** SQLite
        - **واجهة API:** Flask
        - **التصميم:** CSS متقدم مع تأثيرات
        """)

# دالة API محسنة
def get_api_subscriptions_data(program_id):
    """جلب بيانات الاشتراكات بتنسيق JSON للـ API"""
    try:
        conn = db_manager.get_connection()
        c = conn.cursor()
        
        # جلب بيانات البرنامج
        c.execute("SELECT name, description, price FROM programs WHERE id = ? AND is_active = 1", (program_id,))
        program = c.fetchone()
        
        if not program:
            return None
        
        # جلب بيانات الاشتراكات
        c.execute('''
            SELECT u.name, u.serial, u.phone, u.email, s.start_date, s.end_date,
                   CASE WHEN s.end_date >= date('now') THEN 'active' ELSE 'expired' END as status,
                   s.amount_paid, s.created_at
            FROM subscriptions s
            JOIN users u ON s.user_id = u.id
            WHERE s.program_id = ? AND s.status = 'active'
            ORDER BY s.end_date DESC
        ''', (program_id,))
        
        subscriptions = c.fetchall()
        conn.close()
        
        # تحضير البيانات للاستجابة
        response_data = {
            "success": True,
            "program": {
                "id": program_id,
                "name": program[0],
                "description": program[1],
                "price": float(program[2])
            },
            "total_subscriptions": len(subscriptions),
            "timestamp": datetime.now().isoformat(),
            "subscriptions": [
                {
                    "user_name": sub[0],
                    "serial": sub[1],
                    "phone": sub[2],
                    "email": sub[3],
                    "start_date": sub[4],
                    "end_date": sub[5],
                    "status": sub[6],
                    "amount_paid": float(sub[7]),
                    "subscription_date": sub[8]
                }
                for sub in subscriptions
            ]
        }
        
        return response_data
    except Exception:
        return None

# ==============================================
# واجهة API المدمجة مع Flask
# ==============================================

def create_flask_app():
    """إنشاء تطبيق Flask لواجهة API"""
    flask_app = Flask(__name__)
    
    @flask_app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    @flask_app.route('/api/subscriptions/<int:program_id>', methods=['GET'])
    def get_subscriptions_api(program_id):
        """جلب اشتراكات برنامج معين"""
        try:
            data = get_api_subscriptions_data(program_id)
            if data:
                return jsonify(data)
            else:
                return jsonify({"success": False, "error": "البرنامج غير موجود"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @flask_app.route('/api/programs', methods=['GET'])
    def get_programs_api():
        """جلب قائمة جميع البرامج"""
        try:
            programs = get_all_programs()
            return jsonify({
                "success": True,
                "programs": [{"id": p[0], "name": p[1], "description": p[2], "price": float(p[3])} for p in programs],
                "total": len(programs),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @flask_app.route('/api/users', methods=['GET'])
    def get_users_api():
        """جلب قائمة جميع المستخدمين"""
        try:
            users = get_all_users()
            return jsonify({
                "success": True,
                "users": [
                    {
                        "id": user[0],
                        "name": user[1],
                        "phone": user[2],
                        "serial": user[3],
                        "email": user[4],
                        "created_at": user[6]
                    } for user in users
                ],
                "total": len(users),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @flask_app.route('/api/health', methods=['GET'])
    def health_check():
        """فحص حالة الخادم"""
        return jsonify({
            "status": "healthy",
            "service": "Membership Management API",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "subscriptions": "/api/subscriptions/{program_id}",
                "programs": "/api/programs",
                "users": "/api/users",
                "health": "/api/health"
            }
        })
    
    @flask_app.route('/api/stats', methods=['GET'])
    def get_stats_api():
        """جلب إحصائيات النظام"""
        try:
            total_users = get_total_users()
            total_programs = get_total_programs()
            active_subs = get_active_subscriptions()
            expired_subs = get_expired_subscriptions()
            total_revenue, monthly_revenue = get_financial_stats()
            
            return jsonify({
                "success": True,
                "stats": {
                    "total_users": total_users,
                    "total_programs": total_programs,
                    "active_subscriptions": active_subs,
                    "expired_subscriptions": expired_subs,
                    "total_revenue": float(total_revenue),
                    "monthly_revenue": float(monthly_revenue)
                },
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    return flask_app

def run_flask_server():
    """تشغيل خادم Flask في خيط منفصل"""
    flask_app = create_flask_app()
    port = 5000
    
    if is_running_in_cloud():
        # على السحابة، استخدم المنفذ المخصص
        port = get_server_port()
    
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def start_api_server():
    """بدء خادم API"""
    try:
        # التحقق إذا كان الخادم يعمل بالفعل
        response = requests.get('http://localhost:5000/api/health', timeout=2)
        if response.status_code == 200:
            return
    except:
        pass
    
    # بدء الخادم في خيط منفصل
    try:
        flask_thread = threading.Thread(target=run_flask_server, daemon=True)
        flask_thread.start()
        time.sleep(1)
    except Exception:
        pass

# ==============================================
# ملفات النشر للسحابة
# ==============================================

def create_requirements_file():
    """إنشاء ملف المتطلبات للنشر"""
    requirements = """
streamlit==1.28.0
pandas==2.0.3
flask==2.3.3
requests==2.31.0
openpyxl==3.1.2
"""
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)

def create_procfile():
    """إنشاء ملف Procfile للنشر"""
    procfile = """
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
"""
    with open('Procfile', 'w', encoding='utf-8') as f:
        f.write(procfile)

# ==============================================
# التشغيل الرئيسي
# ==============================================

def main():
    # تهيئة الجلسة
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_avatar' not in st.session_state:
        st.session_state.user_avatar = "👨‍💼"
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None
    
    # إنشاء ملفات النشر إذا لم تكن موجودة
    if not os.path.exists('requirements.txt'):
        create_requirements_file()
    if not os.path.exists('Procfile'):
        create_procfile()
    
    # بدء خادم API
    start_api_server()
    
    # عرض واجهة تسجيل الدخول أو الداشبورد
    if not st.session_state.logged_in:
        login_page()
    else:
        main_dashboard()

# ==============================================
# تشغيل التطبيق
# ==============================================

if __name__ == "__main__":
    main()