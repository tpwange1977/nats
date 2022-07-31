from pynats import NATSClient

with NATSClient() as client:
    # Connect
    client.connect()

    # Subscribe
    def callback(msg):
        print(f"Received a message with subject {msg.subject}: {msg}")

    client.subscribe(subject="test-subject", callback=callback)

    # Publish a message
    client.publish(subject="test-subject", payload=b"test-payload")

    # wait for 1 message
    client.wait(count=1)