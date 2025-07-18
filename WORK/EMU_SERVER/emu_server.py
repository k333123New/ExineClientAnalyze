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
                    recv_packet = recv_buffer[:3 + packet_length]
                    del recv_buffer[:3 + packet_length]

                    print(f"완전한 패킷 수신: {recv_packet.hex()}")

                    # 특정 명령에 대한 응답 처리
                    if recv_packet == bytes([0xAA, 0x00, 0x02, 0x0B, 0x00]):
                        response = bytes([
                            0xAA, 0x00, 0x13, 0x7E, 0x1B, 0x43, 0x4F, 0x4E, 0x4E, 0x45,
                            0x43, 0x54, 0x45, 0x44, 0x20, 0x53, 0x45, 0x52, 0x56, 0x45,
                            0x52, 0x0A
                        ])
                        client_socket.sendall(response)
                        print("응답을 보냈습니다.")
                        
                        #aa 0005 00 0047 41 4b (ver 0.71 A K)
                    # 두 번째 요청: aa000500003b414b
                    elif recv_packet == bytes([0xAA, 0x00, 0x05, 0x00, 0x00, 0x47, 0x41, 0x4B]):
                        print("CVersionPacket 요청이 들어옴")
                        
                        
                        response = bytes([
                            #0xAA, 0x00, 0x14, 0x00, 0x00, 0x00, 0x3B, 0x41, 0x4B,0x01, 0x0C,
                            0xAA, 0x00, 0x14, 0x00, 0x00, 0x00, 0x47, 0x41, 0x4B,0x01, 0x0C,
                            *b'192.168.0.15'
                        ])
                        
                        client_socket.sendall(response)
                        print("CVersionPacket 요청에 대한 IP 응답을 보냈습니다.")
                        
                    # 세번째 요청
                        
                    elif recv_packet == bytes([0xAA, 0x00, 0x02, 0x6C, 0x03]):#bytes([0xAA, 0x00, 0x03, 0x6C, 0x02, 0x33]):
                        print("CScriptPacket 요청이 들어옴")
                        response = bytes([
                             0xAA, 0x00, 0x03, 0x02, 0x00, 0x4E
                        ])
                        client_socket.sendall(response)
                        print("CScriptPacket 요청에 대한  응답을 보냈습니다.")
                        
                     # 네번째 요청
                        
                    elif recv_packet == bytes([0xAA, 0x00, 0x02, 0x0F, 0x03]):#bytes([0xAA, 0x00, 0x03, 0x0F, 0x03, 0xCC]):
                        print("CMetaDataPacket 요청이 들어옴")
                        
                        # 1단계: CMetaDataPacket Type 0 응답 (필수!)
                        response = bytes([
                        0xAA, #STX
                        0x00, 0x13, #packet data len
                        
                        0x18, #packet type
                        0x00, #metadata_type(server list(0) or one server info(1))
                        0x00, #server group type(pk? npk? or normal? test?)
                        0x00, 0x02, #server count
                        
                        0x01, 0x31, #server name len +server name str
                        0x00, 0x00, 0x00, 0x00, #unknown 4 bytes 
                        
                        0x03, 0x32, 0x32, 0x32, #server name len +server name str
                        0x00, 0x00, 0x00, 0x00 #unknown 4 bytes 
                        ])
                        
                        client_socket.sendall(response)
                        print("CMetaDataPacket Type 0 응답을 보냈습니다.")
                        
                        # 2단계: 잠시 후 Type 1 패킷 전송
                        import time
                        time.sleep(1.0)  # 100ms 대기
                        
                       
                        
                    elif recv_packet == bytes([0xaa,0x00,0x05,0x0f,0x02,0x00,0x01,0x31]):
                        print("CMetaDataPacket detail 1 0x31 서버 상세 요청이 들어옴")
                        # 2단계: CMetaDataPacket Type 1 응답 (필수!)
                        response = bytes([
                        0xAA, #STX
                        0x00, 0x0f, #packet data len
                        
                        0x18, #packet type
                        0x01, #metadata_type(server list(0) or one server info(1))
                        0x00, #sub_type(server list(0) or one server info(1))
                        
                        0x01, 0x51, #server name len +server name str
                        0x00, 0x00, 0x00, 0x00, #unknown 4 bytes server id?
                        
                        0x00,0x04, #data len
                        0x41, 0x41,0x41,0x41#this data copy to 1mb buffer!)
                        
                        ])
                        client_socket.sendall(response)
                        print("CMetaDataPacket Type 1 0x31 서버 응답을 보냈습니다.")
                        
                    elif recv_packet == bytes([0xaa,0x00,0x07,0x0f,0x02,0x00,0x03,0x32,0x32,0x32]):
                        print("CMetaDataPacket detail 1 0x32,0x32,0x32 서버 상세 요청이 들어옴")
                        # 2단계: CMetaDataPacket Type 1 응답 (필수!)
                        response = bytes([
                        0xAA, #STX
                        0x00, 0x0f, #packet data len
                        
                        0x18, #packet type
                        0x01, #metadata_type(server list(0) or one server info(1))
                        0x00, #sub_type(server list(0) or one server info(1))
                        
                        0x01, 0x52, #server name len +server name str
                        0x00, 0x00, 0x00, 0x00, #unknown 4 bytes server id?
                         
                        0x00,0x04, #data len
                        0x42, 0x42,0x42,0x42#this data copy to 1mb buffer!)
                        ])
                        client_socket.sendall(response)
                        print("CMetaDataPacket Type 1 0x32,0x32,0x32 서버응답을 보냈습니다.")
                        
                        
                        
                    #aa 00 02 57 01 CMultiServerPacket
                    elif recv_packet == bytes([0xaa,0x00,0x02,0x57,0x01]):
                        print("CMultiServerPacket 1 요청이 들어옴")
                        
                        ##14 + 16*27
                        ##0x01, 0x25 or 0x01, 0xBE?
                        
                        response = bytes([
                        0xAA, 0x00, 0x02, 0x56, 0x00
                        ])
                        client_socket.sendall(response)
                        print("CMultiServerPacket 서버정보 데이터를 서버응답으로 보냈습니다.")
                        
                    #aa0003570001
                    elif recv_packet == bytes([0xaa,0x00,0x03,0x57,0x00,0x01]):
                        print("CMultiServerPacket 2 요청이 들어옴")
                        
                        #server.dat data to packet
                        response = bytes([
                        0xAA, 0x00, 0x2D, 0x56 , 
                        0x01, 0x01 ,0x0F ,0x00 ,
                        0xA8 ,0xC0 ,0x05 ,0xE6 ,
                        0x01 ,0x04 ,0xC4 ,0xCE ,
                        0x74 ,0xC7 ,0x24 ,0xB1 ,
                        0x78 ,0xC7 ,0x06 ,0x4C ,
                        0xD1 ,0xA4 ,0xC2 ,0xB8 ,
                        0xD2 ,0x20 ,0x00 ,0x1C ,
                        0xC1 ,0x84 ,0xBC ,0x04 ,
                        0xC4 ,0xCE ,0x74 ,0xC7 ,
                        0x24 ,0xB1 ,0x78 ,0xC7 ,
                        0x00 ,0x01 ,0x0A ,0x0A ,
                        ])
                        client_socket.sendall(response)
                        print("CMultiServerPacket2 데이터를 서버응답으로 보냈습니다.")
                        
                        
                        #aa001203076b333333313233083132343831323438
                    elif recv_packet == bytes([0xaa,0x00,0x12,0x03,0x07,0x6b,0x33,0x33,0x33,0x31,0x32,0x33,0x08,0x31,0x32,0x34,0x38,0x31,0x32,0x34,0x38]):
                        print("CLoginPacket 요청이 들어옴")
                        
                        # 2단계: 잠시 후 Type 1 패킷 전송
                        import time
                        time.sleep(10.0)  # 100ms 대기
                        
                        #aa 00 09 02 00 03 44 D5 C9 B9 74 C7  응답0이 정상
                        response = bytes([
                        0xaa ,0x00 ,0x09 ,0x02 ,0x00 ,0x03 ,0x44 ,0xD5 ,0xC9 ,0xB9 ,0x74 ,0xC7
                        ])
                        client_socket.sendall(response)
                        print("CheckPacket 데이터를 서버응답으로 보냈습니다.")
                        
                        
                    else:
                        print("예상하지 못한 패킷 수신.")

        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            print(f"클라이언트 {client_address}와의 연결을 종료합니다.")
            client_socket.close()

if __name__ == "__main__":
    create_server()
