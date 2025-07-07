def check_env_file():
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Check for GROQ_API_KEY
        groq_lines = [line for line in content.split('\n') 
                     if line.startswith('GROQ_API_KEY=')]
        if not groq_lines:
            print("❌ GROQ_API_KEY not found in .env file")
            return False
            
        # Check for DEFAULT_MODEL
        model_lines = [line for line in content.split('\n') 
                      if line.startswith('DEFAULT_MODEL=')]
        if not model_lines:
            print("❌ DEFAULT_MODEL not found in .env file")
            return False
            
        return True
        
    except FileNotFoundError:
        print("❌ .env file not found")
        return False