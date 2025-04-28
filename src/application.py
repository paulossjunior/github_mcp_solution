import uvicorn
import sys
import os

# Adiciona /app no caminho para o Python encontrar 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    uvicorn.run("src.mcp_server:app", host="0.0.0.0", port=3000, reload=True)
