import os
import sys

def create_env_file():
    """Create a .env file with the required API keys"""
    env_content = """# OpenAI API Key (required for CrewAI to work)
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other API keys you might need
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# GOOGLE_API_KEY=your_google_api_key_here
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Please edit the .env file and replace 'your_openai_api_key_here' with your actual OpenAI API key")
        print("🔗 Get your API key from: https://platform.openai.com/api-keys")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_env_setup():
    """Check if environment is properly set up"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OpenAI API key is set!")
        return True
    else:
        print("❌ OpenAI API key not found or not set properly")
        print("💡 Please set your OpenAI API key in the .env file")
        return False

if __name__ == "__main__":
    print("🚀 Setting up environment for Autonomous Multi Agent Task Bot")
    print("=" * 60)
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        create_env_file()
    else:
        print("📁 .env file already exists")
    
    print("\n🔍 Checking environment setup...")
    check_env_setup()
    
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Run: uvicorn main:app --reload")
    print("3. Open http://127.0.0.1:8000 in your browser") 