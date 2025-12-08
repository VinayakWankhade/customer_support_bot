"""
Database initialization script
Creates all tables and optionally seeds sample data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import engine, init_db
from src.models.models import Base, User
from sqlalchemy.orm import Session


def create_sample_user(db: Session):
    """Create a sample user for testing"""
    sample_user = User(
        name="Test User",
        email="test@example.com"
    )
    db.add(sample_user)
    db.commit()
    print(f"✅ Created sample user: {sample_user.id}")


def main():
    """Initialize database"""
    print("🔧 Initializing database...")
    
    # Create all tables
    init_db()
    print("✅ All tables created successfully")
    
    # Optionally create sample data
    create_sample = input("Create sample user? (y/n): ").lower() == 'y'
    if create_sample:
        with Session(engine) as db:
            create_sample_user(db)
            
    # Optionally seed FAQs
    seed_faqs = input("Seed sample FAQs? (y/n): ").lower() == 'y'
    if seed_faqs:
        from src.data.faq_loader import load_sample_data
        load_sample_data()
    
    print("✨ Database initialization complete!")


if __name__ == "__main__":
    main()
