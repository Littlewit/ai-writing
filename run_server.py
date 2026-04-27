import uvicorn
import os
from api import app

if __name__ == "__main__":
    # Render 使用 PORT 环境变量，默认为 10000
    # 本地开发使用 8000
    port = int(os.environ.get("PORT", 8000))
    
    # 必须绑定到 0.0.0.0 才能接受外部连接
    host = "0.0.0.0"
    
    if port == 8000:
        print("Local development mode enabled.")
        print(f"Starting server on http://localhost:{port}")
    else:
        print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")