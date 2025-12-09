import sys
import os
sys.path.append(os.getcwd())
from src.database import SessionLocal
from src.models.models import Session
import json

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return str(obj)

db = SessionLocal()
try:
    sessions = db.query(Session).order_by(Session.last_active_at.desc()).limit(5).all()
    print(f"Found {len(sessions)} sessions.")
    for s in sessions:
        print(f"ID: {s.id}")
        print(f"Created: {s.created_at}")
        print(f"Active: {s.last_active_at}")
        print(f"Metadata: {s.session_metadata}")
        print("-" * 20)
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
