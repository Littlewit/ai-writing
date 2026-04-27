import requests
import json

def test_streaming():
    print("Testing streaming endpoint...")

    thread_id = "test_thread_123"
    message = "你好"

    url = f"http://localhost:8000/stream/{thread_id}?message={message}"

    print(f"Sending request to: {url}")

    try:
        response = requests.get(url, stream=True)

        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type')}")

        if response.status_code == 200:
            print("\nStream response:")
            print("-" * 50)

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    print(f"Received: {line}")

                    if 'data:' in line:
                        try:
                            data = json.loads(line.replace('data: ', ''))
                            if 'content' in data:
                                print(f"Content chunk: {data['content']}")
                        except:
                            pass

            print("-" * 50)
            print("Stream completed successfully!")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_streaming()