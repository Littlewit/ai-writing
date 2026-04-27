import requests
import json

response = requests.get(
    "http://localhost:8000/stream/test123?message=你好",
    stream=True
)

print(f"状态码: {response.status_code}")
print(f"内容类型: {response.headers.get('content-type')}")

if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode('utf-8')
                print(f"收到: {decoded}")
                if decoded.startswith('data:'):
                    data = json.loads(decoded[6:])
                    print(f"解析: {data}")
            except Exception as e:
                print(f"错误: {e}")
else:
    print(f"请求失败: {response.text}")