#!/usr/bin/env python3
"""
Setup script for GEMINI integration
This script helps configure the GEMINI AI integration for StudyHub
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_env_file():
    """Check and update .env file"""
    print("\n🔧 Checking environment configuration...")

    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        return False

    # Read current .env content
    with open(env_path, 'r') as f:
        env_content = f.read()

    if "GEMINI_API_KEY" not in env_content:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False

    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  GEMINI_API_KEY is not configured")
        print("Please follow these steps:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Replace 'your_gemini_api_key_here' in .env with your actual API key")
        return False

    print("✅ GEMINI_API_KEY is configured")
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing package imports...")

    required_packages = [
        ('flask', 'Flask'),
        ('google.generativeai', 'Google Generative AI'),
        ('chromadb', 'ChromaDB'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests')
    ]

    all_imported = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            all_imported = False

    return all_imported

def test_gemini_connection():
    """Test GEMINI API connection"""
    print("\n🤖 Testing GEMINI API connection...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        import google.generativeai as genai

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("⚠️  GEMINI API key not configured, skipping connection test")
            return False

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Test with a simple prompt
        response = model.generate_content("Hello, please respond with 'GEMINI is working correctly'")

        if response and response.text:
            print("✅ GEMINI API connection successful")
            print(f"Response: {response.text.strip()}")
            return True
        else:
            print("❌ GEMINI API connection failed - no response")
            return False

    except Exception as e:
        print(f"❌ GEMINI API connection failed: {str(e)}")
        return False

def initialize_vector_db():
    """Initialize the vector database"""
    print("\n🗃️  Initializing vector database...")

    try:
        # Import here to ensure packages are installed
        from app.services.vector_service import vector_service

        # Test ChromaDB connection
        if hasattr(vector_service, 'client'):
            print("✅ ChromaDB initialized successfully")

            # Initialize with basic knowledge
            from init_knowledge_base import initialize_knowledge_base
            if initialize_knowledge_base():
                print("✅ Knowledge base initialized successfully")
                return True
            else:
                print("⚠️  Knowledge base initialization had some issues")
                return False
        else:
            print("❌ ChromaDB initialization failed")
            return False

    except Exception as e:
        print(f"❌ Vector database initialization failed: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 StudyHub GEMINI Integration Setup")
    print("="*50)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed: Could not install required packages")
        sys.exit(1)

    # Test imports
    if not test_imports():
        print("\n❌ Setup failed: Some packages could not be imported")
        sys.exit(1)

    # Check environment configuration
    env_configured = check_env_file()

    # Test GEMINI connection if configured
    gemini_working = False
    if env_configured:
        gemini_working = test_gemini_connection()

    # Initialize vector database
    vector_db_ready = initialize_vector_db()

    # Final status
    print("\n" + "="*50)
    print("📋 Setup Summary:")
    print(f"✅ Python version: Compatible")
    print(f"✅ Packages: Installed")
    print(f"{'✅' if env_configured else '⚠️ '} Environment: {'Configured' if env_configured else 'Needs API key'}")
    print(f"{'✅' if gemini_working else '⚠️ '} GEMINI API: {'Working' if gemini_working else 'Not configured'}")
    print(f"{'✅' if vector_db_ready else '❌'} Vector Database: {'Ready' if vector_db_ready else 'Failed'}")

    if env_configured and gemini_working and vector_db_ready:
        print("\n🎉 Setup completed successfully!")
        print("Your StudyHub AI assistant is ready to use.")
        print("\n🚀 To start the application:")
        print("python app.py")
    elif not env_configured:
        print("\n⚠️  Setup partially completed.")
        print("Please configure your GEMINI_API_KEY in the .env file to enable AI features.")
        print("The application will still work with limited functionality.")
    else:
        print("\n❌ Setup completed with errors.")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()