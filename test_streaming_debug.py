import requests
import json

def test_streaming():
    print("Testing streaming endpoint with detailed logging...")

    thread_id = "test_thread_456"
    message = "请写一篇关于春天的短文"

    url = f"http://localhost:8000/stream/{thread_id}?message={message}"

    print(f"Sending request to: {url}\n")

    try:
        response = requests.get(url, stream=True)

        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type')}\n")

        if response.status_code == 200:
            print("Stream response:")
            print("=" * 60)

            message_count = 0
            full_content = ""

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    print(f"Raw: {line}")

                    if line.startswith('event:'):
                        print(f"Event: {line}")
                    elif line.startswith('data:'):
                        try:
                            data = json.loads(line.replace('data: ', ''))
                            if 'content' in data:
                                message_count += 1
                                full_content += data['content']
                                print(f"\n[MESSAGE {message_count}] {data['content']}")
                            elif 'status' in data:
                                print(f"\n[STATUS] {data['status']}")
                            elif 'error' in data:
                                print(f"\n[ERROR] {data['error']}")
                        except Exception as e:
                            print(f"Parse error: {e}")

            print("=" * 60)
            print(f"\nTotal messages received: {message_count}")
            print(f"Total content length: {len(full_content)}")
            print(f"Content preview: {full_content[:100]}...")

            if message_count > 0:
                print("\n✓ Streaming test PASSED!")
            else:
                print("\n✗ Streaming test FAILED - No messages received")

        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_streaming()