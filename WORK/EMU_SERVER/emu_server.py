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
                        
                        '''
                        response = bytes([
                            0xAA, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x0C,
                            *b'192.168.0.15'
                        ])
                        '''
                        '''
                        response = bytes([
                        0xAA, 0x12, 0x00, 0x00, 0x00,           # STX + Length(18) + Type(0) + PacketType(0)
                        0x00, 0x00, 0x00, 0x00,                 # 체크섬 (4바이트)
                        0x01,                                   # 클라이언트 상태
                        0x0C,                                   # 메시지 길이 (12)
                        0x31, 0x39, 0x32, 0x2E, 0x31, 0x36,    # "192.16"
                        0x38, 0x2E, 0x30, 0x2E, 0x31, 0x35     # "8.0.15"
                        ])
                        '''
                        '''
                        response = bytes([
                             #0xAA, 0x22, 0x01, 0x00, 0x01, 0x08, 0xC1, 0xFA, 0xBC, 0xAD, 0xBC, 0xAD, 0xB9, 0xF6,
                             #0xAA, 0x98, 0x00, 0x00, 0x01, 0x08, 0xC1, 0xFA, 0xBC, 0xAD, 
                             0xAA, 0x00, 0x98, 0x00, 0x01, 0x08, 0xC1, 0xFA, 0xBC, 0xAD, 
                             0xBC, 0xAD, 0xB9, 0xF6, 0x04, 0x01, 0x7F, 0x00, 0x00, 0x01, 
                             0xA0, 0x0F, 0x01, 0x0A, 0xB5, 0xF0, 0xBE, 0xC6, 0xC5, 0xA9, 
                             0xB8, 0xAE, 0xB3, 0xEB, 0x01, 0x31, 0x09, 0x31, 0x32, 0x37, 
                             0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x31, 0x31, 
                             0x31, 0x02, 0x7F, 0x00, 0x00, 0x01, 0xA1, 0x0F, 0x01, 0x0A, 
                             0xC7, 0xEC, 0xB1, 0xD7, 0xB3, 0xD7, 0xC0, 0xCC, 0xBE, 0xC6, 
                             0x01, 0x32, 0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 
                             0x2E, 0x31, 0x03, 0x00, 0x32, 0x32, 0x32, 0x03, 0x7F, 0x00, 
                             0x00, 0x01, 0xA2, 0x0F, 0x01, 0x08, 0xBF, 0xA1, 0xC0, 0xCC, 
                             0xB7, 0xB9, 0xB3, 0xD7, 0x01, 0x33, 0x09, 0x31, 0x32, 0x37, 
                             0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x33, 0x33, 
                             0x33, 0x04, 0x7F, 0x00, 0x00, 0x01, 0xA3, 0x0F, 0x01, 0x08, 
                             0xC7, 0xC1, 0xB7, 0xCE, 0xB3, 0xD7, 0xB8, 0xB6, 0x01, 0x34, 
                             0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 
                             0x03, 0x00, 0x34, 0x34, 0x34
                        ])
                        '''
                        '''
                        response = bytes([
                             0xAA, 0x00, 0x35, 0x01, 0x0B, 0xBC, 0xAD, 0xB9, 0xF6, 0x20, 
                             0xB8, 0xAE, 0xBD, 0xBA, 0xC6, 0xAE, 0x03, 0x05, 0xBC, 0xAD, 
                             0xB9, 0xF6, 0x31, 0x05, 0xBC, 0xAD, 0xB9, 0xF6, 0x32, 0x05, 
                             0xBC, 0xAD, 0xB9, 0xF6, 0x33, 0x02, 0x09, 0xBA, 0xCE, 0xB0, 
                             0xA1, 0xC1, 0xA4, 0xBA, 0xB8, 0x31, 0x09, 0xBA, 0xCE, 0xB0, 
                             0xA1, 0xC1, 0xA4, 0xBA, 0xB8, 0x32])
                        '''  
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
                        
                        # Type 1 패킷 (서버 리스트) - 기존 패킷 그대로 사용
                       
                        '''
                        response = bytes([
                             0xAA,0x00 ,0x70 ,0x18 ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F
                             ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42
                             ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49
                             ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65
                             ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63
                             ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F
                             ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42 ,0x4E ,0x65 ,0x78 ,0x6F ,0x6E ,0x49 ,0x6E ,0x63 ,0x2E ,0x42
                        ])
                        '''
                        #현재: 0xAA, 0x22 (8874 bytes - 잘못됨) 올바름: 0x25, 0x01 (293 bytes)
                        
                        
                        '''bytes([
                             #0xAA, 0x22, 0x01, 0x00, 0x01, 0x08, 0xC1, 0xFA, 0xBC, 0xAD, 0xBC, 0xAD, 0xB9, 0xF6,
                             0xAA, 0x22, 0x01, 0x00, 0x01, 0x08, 0xC1, 0xEF, 0xBC, 0xAD, 0xBC, 0xAD, 0xB9, 0xF6,
                             0x04, 0x01, 0x7F, 0x00, 0x00, 0x01, 0xA0, 0x0F, 0x01, 0x0A, 0xB5, 0xF0, 0xBE, 0xC6,
                             0xC5, 0xA9, 0xB8, 0xAE, 0xB3, 0xEB, 0x01, 0x31, 0x09, 0x31, 0x32, 0x37, 0x2E, 0x30,
                             0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x31, 0x31, 0x31, 0x02, 0x7F, 0x00, 0x00, 0x01, 
                             0xA1, 0x0F, 0x01, 0x0A, 0xC7, 0xEC, 0xB1, 0xD7, 0xB3, 0xD7, 0xC0, 0xCC, 0xBE, 0xC6, 
                             0x01, 0x32, 0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 
                             0x32, 0x32, 0x32, 0x03, 0x7F, 0x00, 0x00, 0x01, 0xA2, 0x0F, 0x01, 0x08, 0xBF, 0xA1, 
                             0xC0, 0xCC, 0xB7, 0xB9, 0xB3, 0xD7, 0x01, 0x33, 0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 
                             0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x33, 0x33, 0x33, 0x04, 0x7F, 0x00, 0x00, 0x01, 
                             0xA3, 0x0F, 0x01, 0x08, 0xC7, 0xC1, 0xB7, 0xCE, 0xB3, 0xD7, 0xB8, 0xB6, 0x01, 0x34, 
                             0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x34, 0x34, 
                             0x34, 0x08, 0xC0, 0xDA, 0xC0, 0xAF, 0xBC, 0xAD, 0xB9, 0xF6, 0x04, 0x01, 0x7F, 0x00, 
                             0x00, 0x01, 0xA4, 0x0F, 0x03, 0x00, 0x01, 0x35, 0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 
                             0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x35, 0x35, 0x35, 0x02, 0x7F, 0x00, 0x00, 0x01, 
                             0xA5, 0x0F, 0x03, 0x08, 0xC4, 0xC9, 0xC0, 0xCC, 0xB3, 0xD7, 0xC0, 0xCE, 0x01, 0x36, 
                             0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x36, 0x36, 
                             0x36, 0x03, 0x7F, 0x00, 0x00, 0x01, 0xA6, 0x0F, 0x03, 0x08, 0xB5, 0xF0, 0xC5, 0xE4,
                             0xB9, 0xCC, 0xBE, 0xC6, 0x01, 0x37, 0x09, 0x31, 0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 
                             0x2E, 0x31, 0x03, 0x00, 0x37, 0x37, 0x37, 0x04, 0x7F, 0x00, 0x00, 0x01, 0xA7, 0x0F, 
                             0x03, 0x08, 0xC4, 0xE2, 0xBA, 0xEA, 0xB3, 0xAA, 0xC5, 0xE4, 0x01, 0x38, 0x09, 0x31, 
                             0x32, 0x37, 0x2E, 0x30, 0x2E, 0x30, 0x2E, 0x31, 0x03, 0x00, 0x38, 0x38, 0x38
                        ])'''
                        #client_socket.sendall(response)
                        #print("Type 1 패킷 (서버 리스트)을 보냈습니다.")
                        
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
                        print("CMultiServerPacket 요청이 들어옴")
                        
                        response = bytes([
                        0xAA, #STX
                        0x00, 0xE1, #packet data len
                        
                        0x56, #packet type
                        
                        #Compressed Data
                        0x78, 0x9C, 0x63, 0x65, 0x64, 0x64, 0x60, 0x60, 0x98, 0x20, 0xCF, 0xC0, 0xC5, 0xB0, 0xE3, 0xDE,
                        0x81, 0x73, 0x0A, 0x7B, 0xD6, 0xEE, 0xFC, 0x06, 0x64, 0x1B, 0x1A, 0x99, 0xEB, 0x19, 0x00, 0xA1,
                        0x21, 0x83, 0x28, 0x44, 0x7C, 0xC3, 0x95, 0x03, 0x97, 0xC1, 0x92, 0x07, 0xAE, 0x6C, 0x39, 0xBF,
                        0xE5, 0x26, 0x03, 0x13, 0x13, 0x50, 0xDB, 0x44, 0x79, 0x46, 0x1E, 0x86, 0xA3, 0xD7, 0xF7, 0xEE,
                        0x3A, 0xB6, 0x0E, 0xA2, 0x91, 0x8F, 0xC1, 0xD0, 0xD2, 0x48, 0xCF, 0xD0, 0xCC, 0x42, 0xCF, 0x50,
                        0xCF, 0xD0, 0xC0, 0x00, 0xC8, 0x87, 0xC8, 0xEE, 0x7F, 0x0D, 0x91, 0x67, 0x06, 0x59, 0x36, 0x49,
                        0x9E, 0x81, 0x87, 0xE1, 0xC0, 0x99, 0x5D, 0x4B, 0x61, 0xBA, 0x80, 0xD6, 0x19, 0x80, 0x6D, 0x33,
                        0x35, 0x60, 0x10, 0x63, 0x38, 0xB6, 0x7E, 0xD7, 0x06, 0x05, 0xA8, 0xF4, 0x81, 0x3F, 0x30, 0x9D,
                        0x2C, 0xCC, 0x40, 0x9D, 0x93, 0xE5, 0x99, 0x38, 0x19, 0x02, 0xCA, 0x02, 0x20, 0x42, 0xFC, 0x0C,
                        0x46, 0x06, 0xC6, 0x7A, 0x46, 0xC6, 0x26, 0x7A, 0xA6, 0x40, 0xFB, 0x8C, 0x8C, 0x19, 0xE4, 0xC0,
                        0x72, 0x70, 0x3D, 0x0A, 0xBA, 0x0A, 0x1B, 0xDE, 0xEE, 0xF9, 0xB6, 0xF5, 0xE5, 0x81, 0xE3, 0x40,
                        0xC1, 0x03, 0x4F, 0x19, 0x58, 0x41, 0xB6, 0x4F, 0x01, 0x79, 0x75, 0xEF, 0xD1, 0x8D, 0x57, 0xE0,
                        0x2E, 0x36, 0xB4, 0xD0, 0x33, 0x33, 0x07, 0x19, 0xA0, 0x67, 0x62, 0xCA, 0x20, 0x02, 0x91, 0x3B,
                        0xB0, 0xFE, 0xC0, 0x2F, 0x85, 0x13, 0xEB, 0xF7, 0x6F, 0x85, 0xA8, 0x02, 0x00, 0x03, 0xA7, 0x74,
                        0x6F
                        ])
                        print("CMultiServerPacket 압축된 서버정보 데이터를 서버응답으로 보냈습니다.")
                        
                        
                    else:
                        print("예상하지 못한 패킷 수신.")

        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            print(f"클라이언트 {client_address}와의 연결을 종료합니다.")
            client_socket.close()

if __name__ == "__main__":
    create_server()
