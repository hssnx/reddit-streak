#!/usr/bin/env python3

import random
import socket
import sys
import webbrowser
import praw

def receive_connection(port):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", port))
    sock.listen(1)
    client = sock.accept()[0]
    sock.close()
    return client

def send_html_response(client, message):
    html = f"""
    <html>
        <head><title>Authorization Complete</title></head>
        <body">
            <h1>Authorization Successful</h1>
            <p>{message}</p>
            <p>You may now close this window and return to the terminal.</p>
        </body>
    </html>
    """
    client.send(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html}".encode())
    client.close()

def main():
    print("Reddit Refresh Token Generator")
    client_id = input("Enter client_id: ").strip()
    client_secret = input("Enter client_secret: ").strip()
    port = 8080

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=f"http://localhost:{port}",
        user_agent="streak-bot-token-generator by u/yourusername"
    )

    state = str(random.randint(0, 65000))
    url = reddit.auth.url(scopes=["vote"], state=state, duration="permanent")

    print("\nOpening Reddit authorization in your default browser...")
    webbrowser.open(url, new=2)

    print("Waiting for Reddit authorization to complete...")
    client = receive_connection(port)

    data = client.recv(1024).decode()
    query = data.split(" ")[1].split("?", 1)[1]
    params = dict(pair.split("=") for pair in query.split("&"))

    if params.get("state") != state:
        send_html_response(client, "State mismatch. Authorization failed.")
        sys.exit("Error: State mismatch – possible CSRF detected. Aborting.")

    token = reddit.auth.authorize(params["code"])
    send_html_response(client, "Authorization successful.")

    print("\n ✅ Refresh token generated successfully:\n")
    print(token)
    print("\nStore this token securely. You will need it for GitHub Secrets.")

if __name__ == "__main__":
    main()
