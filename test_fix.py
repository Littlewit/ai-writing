import requests
import json

def test_streaming():
    print("Testing streaming endpoint...")

    thread_id = "test_thread_fix"
    message = "请写一条朋友圈，表达今天很高兴吃肯德基的心情"

    url = f"http://localhost:8000/stream/{thread_id}?message={message}"

    print(f"Sending request to: {url}")

    try:
        response = requests.get(url, stream=True)

        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type')}")

        if response.status_code == 200:
            print("\nStream response:")
            print("-" * 50)

            full_content = ""

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    try:
                        print(f"Received: {line}")
                    except UnicodeEncodeError:
                        # 移除emoji后打印
                        line_no_emoji = ''.join(c for c in line if ord(c) <= 0xFFFF)
                        print(f"Received: {line_no_emoji} (emoji removed)")

                    if line.startswith('data: '):
                        try:
                            data = json.loads(line.replace('data: ', ''))
                            if 'content' in data:
                                full_content += data['content']
                                try:
                                    print(f"\nContent: {data['content']}")
                                except UnicodeEncodeError:
                                    # 移除emoji后打印
                                    content_no_emoji = ''.join(c for c in data['content'] if ord(c) <= 0xFFFF)
                                    print(f"\nContent: {content_no_emoji} (emoji removed)")
                            elif 'status' in data:
                                print(f"\nStatus: {data['status']}")
                            elif 'error' in data:
                                print(f"\nError: {data['error']}")
                        except Exception as e:
                            if e.message != 'Unexpected end of JSON input':
                                print(f"Parse error: {e}")

            print("-" * 50)
            print(f"\nFull content:\n{full_content}")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_streaming()