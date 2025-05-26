import socket

def create_server():
    host = '192.168.0.15'  # 서버 주소
    port = 1510            # 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"서버가 {host}:{port}에서 클라이언트를 기다립니다...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"클라이언트 {client_address}가 연결되었습니다.")

        try:
            initial_response = bytes([
                0xAA, 0x00, 0x13, 0x7E, 0x1B, 0x43, 0x4F, 0x4E, 0x4E, 0x45,
                0x43, 0x54, 0x45, 0x44, 0x20, 0x53, 0x45, 0x52, 0x56, 0x45,
                0x52, 0x0A
            ])
            client_socket.sendall(initial_response)
            print("클라이언트 접속 시 초기 응답을 보냈습니다.")

            recv_buffer = bytearray()

            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"클라이언트 {client_address}가 연결을 종료했습니다.")
                    break

                recv_buffer.extend(data)

                while True:
                    if len(recv_buffer) < 3:
                        # 최소한 헤더 + 길이까지는 있어야 함
                        break

                    if recv_buffer[0] != 0xAA:
                        # 잘못된 시작 바이트 제거
                        recv_buffer.pop(0)
                        continue

                    # 패킷 길이 추출 (2바이트)
                    packet_length = (recv_buffer[1] << 8) | recv_buffer[2]

                    if len(recv_buffer) < 3 + packet_length:
                        # 아직 전체 패킷이 도착하지 않음
                        break

                    # 패킷 추출
                    full_packet = recv_buffer[:3 + packet_length]
                    del recv_buffer[:3 + packet_length]

                    print(f"완전한 패킷 수신: {full_packet.hex()}")

                    # 특정 명령에 대한 응답 처리
                    if full_packet == bytes([0xAA, 0x00, 0x02, 0x0B, 0x00]):
                        response = bytes([
                            0xAA, 0x00, 0x13, 0x7E, 0x1B, 0x43, 0x4F, 0x4E, 0x4E, 0x45,
                            0x43, 0x54, 0x45, 0x44, 0x20, 0x53, 0x45, 0x52, 0x56, 0x45,
                            0x52, 0x0A
                        ])
                        client_socket.sendall(response)
                        print("응답을 보냈습니다.")
                        
                    # 두 번째 요청: aa000500003b414b
                    elif full_packet == bytes([0xAA, 0x00, 0x05, 0x00, 0x00, 0x3B, 0x41, 0x4B]):
                        response = bytes([
                            0xAA, 0x00, 0x14, 0x00, 0x00, 0x00, 0x3B, 0x41, 0x4B,0x01, 0x0C,
                            *b'192.168.0.15'
                        ])
                        client_socket.sendall(response)
                        print("AK 요청에 대한 IP 응답을 보냈습니다.")
                    else:
                        print("예상하지 못한 패킷 수신.")

        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            print(f"클라이언트 {client_address}와의 연결을 종료합니다.")
            client_socket.close()

if __name__ == "__main__":
    create_server()
