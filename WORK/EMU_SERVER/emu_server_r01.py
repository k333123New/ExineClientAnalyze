import socket

#create response packet area
def Create_packet(packet_type: int, data: bytes) -> bytes:
    if not (0 <= packet_type <= 0xFF):
        raise ValueError("packet_type must be a single byte (0-255).")
    header = bytes([0xAA])
    length = len(data) + 1  # +1 for the packet_type byte
    length_bytes = length.to_bytes(2, byteorder='big')  # 2-byte big-endian
    type_byte = bytes([packet_type])
    return header + length_bytes + type_byte + data

def GenResponseData_0x00(ip_address: str) -> bytes:

    if not isinstance(ip_address, str):
        raise TypeError("ip_address must be a string.")
    ip_bytes = ip_address.encode('ascii')
    if len(ip_bytes) > 15:
        raise ValueError("IP address string too long (max 15 characters).")
        
    return bytes([
        0x00, 0x00,0x47, 0x41, 0x4B, 0x01, 0x0C,*ip_bytes
    ])

def GenResponseData_0x03(ip_address: str, port: int) -> bytes:
    # IP 주소 -> little-endian 4바이트
    ip_parts = list(map(int, ip_address.split('.')))
    if len(ip_parts) != 4:
        raise ValueError("IP 주소는 4개의 옥텟이어야 합니다.")
        
    ip_int = (ip_parts[0] << 24) | (ip_parts[1] << 16) | (ip_parts[2] << 8) | ip_parts[3]
    ip_bytes = ip_int.to_bytes(4, byteorder='little')  # IP는 little-endian

    # 포트 번호 -> big-endian 2바이트
    if not (0 <= port <= 65535):
        raise ValueError("포트 번호는 0~65535 사이여야 합니다.")
        
    port_bytes = port.to_bytes(2, byteorder='big')     # 포트는 big-endian
    
    # 마지막 바이트 0x00
    end_byte = bytes([0x00])
    return ip_bytes + port_bytes + end_byte

def GenResponseData_0x18() -> bytes:
    return bytes([
        0x00,       # metadata_type (0: server list, 1: one server info)
        0x00,       # server group type (예: pk, npk, normal, test 등)
        0x00, 0x02, # server count (2 servers, 2바이트 빅엔디안)
        
        0x01,       # 첫 번째 서버 이름 길이 (1바이트)
        0x31,       # 첫 번째 서버 이름 문자열 ('1', ASCII 0x31)
        0x00, 0x00, 0x00, 0x00, # 알 수 없는 4바이트 (0으로 채움)
        
        0x03,       # 두 번째 서버 이름 길이 (3바이트)
        0x32, 0x32, 0x32,       # 두 번째 서버 이름 문자열 ('322', ASCII 0x32 0x32 0x32)
        0x00, 0x00, 0x00, 0x00  # 알 수 없는 4바이트 (0으로 채움)
    ])

def GenResponseData_0x18_meta1() -> bytes:
    return bytes([
        0x01,       # metadata_type (1: one server info)
        0x00,       # sub_type (예: 서버 리스트/하위 구분 등)
        0x01,       # 서버 이름 길이 (1바이트)
        0x51,       # 서버 이름 문자열 ('Q', ASCII 0x51)
        0x00, 0x00, 0x00, 0x00,  # 알 수 없는 4바이트 (서버 ID 추정)
        0x00, 0x04, # data length (4바이트, big-endian)
        0x41, 0x41, 0x41, 0x41  # 복사할 데이터 (예: 'AAAA', ASCII 0x41 0x41 0x41 0x41)
    ])

def GenResponseData_0x18_meta1_2() -> bytes:
    return bytes([
        0x01,       # metadata_type (1: one server info)
        0x00,       # sub_type (0: server list, 1: one server info 등)
        0x01,       # 서버 이름 길이 (1바이트)
        0x52,       # 서버 이름 문자열 ('R', ASCII 0x52)
        0x00, 0x00, 0x00, 0x00,  # 알 수 없는 4바이트 (서버 ID 등 추정)
        0x00, 0x04,             # 데이터 길이 (4바이트, big-endian) — 총 4바이트
        0x42, 0x42, 0x42, 0x42  # 데이터 (예: 'BBBB', ASCII 0x42 0x42 0x42 0x42)
    ])

#read server.dat if exist
def GenResponseData_0x56() -> bytes:
    return bytes([
        0x01,
        0x01,
        0xE8, 0x00, 0xA8, 0xC0,  # main server ip (little endian)
        0x05, 0xE7,              # main server port (big endian)
        0x01,
        0x04, 0x54, 0xCF, 0x74, 0xC7, 0x24, 0xB1, 0x78, 0xC7,  # 1byte len, 2bytes string(케이네인)
        0x06, 0x4C, 0xD1, 0xA4, 0xC2, 0xB8, 0xD2, 0x20, 0x00, 0x1C, 0xC1, 0x84, 0xBC,  # 1byte len, 2bytes string(테사트 서버)
        0x04, 0x54, 0xCF, 0x74, 0xC7, 0x24, 0xB1, 0x78, 0xC7,  # 1byte len, 2bytes string (케이네인)
        0x00, 0x01, 0x0A, 0x0A  # 2byte len, 2bytes string
    ])
    
def GenResponseData_0x7E() -> bytes:
    return bytes([
        0x1B, 0x43, 0x4F, 0x4E, 0x4E, 0x45,
        0x43, 0x54, 0x45, 0x44, 0x20, 0x53,
        0x45, 0x52, 0x56, 0x45, 0x52, 0x0A
    ])

def parse_recv_Loginpacket(recv_packet: bytes):

    # 최소 길이 확인
    if len(recv_packet) < 4:
        print("패킷이 너무 짧습니다.")
        return
        
    # 4번째 바이트가 0x03인지 확인
    if recv_packet[3] != 0x03:
        print("유효하지 않은 패킷 타입입니다.")
        return
        
    try:
        # 첫 문자열 추출
        offset = 4
        str1_len = recv_packet[offset]
        offset += 1
        str1 = recv_packet[offset:offset + str1_len].decode('ascii')
        offset += str1_len
        
        # 두 번째 문자열 추출
        str2_len = recv_packet[offset]
        offset += 1
        str2 = recv_packet[offset:offset + str2_len].decode('ascii')

        print(f"✅ 문자열 1: {str1}")
        print(f"✅ 문자열 2: {str2}")
        
        #check login database
        return True
        
        
    except Exception as e:

        print("패킷 파싱 중 오류 발생:", e)


def handle_recv_packet(recv_packet: bytes, client_socket):
    # 1. 최소 길이 체크: 헤더(1) + 길이(2) + 데이터(최소 1)
    if len(recv_packet) < 4:
        print("패킷 길이가 너무 짧습니다.")
        return
        
    # 2. 헤더 확인
    if recv_packet[0] != 0xAA:
        print(f"잘못된 헤더: {recv_packet[0]:02X}")
        return

    # 3. 길이 읽기 (빅엔디언)
    data_length = int.from_bytes(recv_packet[1:3], byteorder='big')
    
    # 4. 전체 길이 검증
    expected_len = 1 + 2 + data_length  # 헤더 + 길이 필드 + 데이터
    if len(recv_packet) != expected_len:
        print(f"길이 불일치: 실제 {len(recv_packet)}, 기대 {expected_len}")
        return
        
    # 5. 데이터 영역 분리
    data = recv_packet[3:]  # data_length 길이만큼
    
    # 6. 데이터 영역 첫 바이트가 패킷 타입
    packet_type = data[0]
    
    # 패킷 타입별 처리 함수 정의
    
    #aa 0005 00 0047 41 4b (ver 0.71 A K)
    def handle_type_0x00():
        print("패킷 타입 0x00 처리")
        print("CVersionPacket 요청이 들어옴")
        response = Create_packet(0x00,GenResponseData_0x00('192.168.0.232'))
        client_socket.sendall(response)
        print("CVersionPacket 요청에 대한 IP 응답을 보냈습니다.")
        
    #bytes([0xAA, 0x00, 0x02, 0x0B, 0x00]):
    def handle_type_0x0B():
        print("패킷 타입 0x0B 처리")
        response = Create_packet(0x7E, GenResponseData_0x7E())
        client_socket.sendall(response)
        print("응답을 보냈습니다.")
    
    #aa0003570001(send server.dat bytes - maybe check file validate(CRC), no use this data.)
    def handle_type_0x57():
        print("패킷 타입 handle_type_0x57 처리")
        print("CMultiServerPacket 2 요청이 들어옴")
        response = Create_packet(0x56,GenResponseData_0x56())
        client_socket.sendall(response)
        print("CMultiServerPacket2 데이터를 서버응답으로 보냈습니다.")
        
    #bytes([0xAA, 0x00, 0x03, 0x6C, 0x02, 0x33]):
    def handle_type_0x6C():
        print("패킷 타입 handle_type_0x6C 처리") 
        print("CScriptPacket 요청이 들어옴")
        response = bytes([0xAA, 0x00, 0x03, 0x02, 0x00, 0x4E])
        client_socket.sendall(response)
        print("CScriptPacket 요청에 대한  응답을 보냈습니다.")
        
    def handle_type_0x0F():
        print("패킷 타입 handle_type_0x0F 처리") 
        
    # 패킷 타입 - 처리 함수 매핑
    packet_handlers = {
        0x00: handle_type_0x00,
        0x0B: handle_type_0x0B,
        0x57: handle_type_0x57,
        0x6C: handle_type_0x6C,
        0x0F: handle_type_0x0F,
    }
    
    # 7. 핸들러 호출
    handler = packet_handlers.get(packet_type)
    if handler:
        handler()
    else:
        print(f"알 수 없는 패킷 타입: 0x{packet_type:02X}")

#################################################
    
def create_server():
    host = '192.168.0.232'  # 서버 주소
    port = 1510            # 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"서버가 {host}:{port}에서 클라이언트를 기다립니다...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"클라이언트 {client_address}가 연결되었습니다.")

        try:
            initial_response = Create_packet(0x7E,GenResponseData_0x7E())
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
                    
                    # 최소한 헤더 + 길이까지는 있어야 함
                    if len(recv_buffer) < 3:
                        break
                        
                    # 잘못된 시작 바이트 제거
                    if recv_buffer[0] != 0xAA:
                        recv_buffer.pop(0)
                        continue
                        
                    # 패킷 길이 추출 (2바이트)
                    packet_length = (recv_buffer[1] << 8) | recv_buffer[2]
                    
                    # 아직 전체 패킷이 도착하지 않음
                    if len(recv_buffer) < 3 + packet_length: 
                        break

                    # 패킷 추출
                    recv_packet = recv_buffer[:3 + packet_length]
                    del recv_buffer[:3 + packet_length]

                    print(f"완전한 패킷 수신: {recv_packet.hex()}")
                    handle_recv_packet(recv_packet,client_socket)
                    
                    
                    # 네번째 요청
                    # 1단계: CMetaDataPacket Type 0 응답 (필수!)
                    #bytes([0xAA, 0x00, 0x03, 0x0F, 0x03, 0xCC]):
                    if recv_packet == bytes([0xAA, 0x00, 0x02, 0x0F, 0x03]):
                        print("CMetaDataPacket 요청이 들어옴")
                        response = Create_packet(0x18,GenResponseData_0x18())
                        client_socket.sendall(response)
                        print("CMetaDataPacket Type 0 응답을 보냈습니다.")
                        
                        # 2단계: 잠시 후 Type 1 패킷 전송
                        import time
                        time.sleep(1.0)  # 100ms 대기
                        
                       
                    # 2단계: CMetaDataPacket Type 1 응답 (필수!)
                    elif recv_packet == bytes([0xaa,0x00,0x05,0x0f,0x02,0x00,0x01,0x31]):
                        print("CMetaDataPacket detail 1 0x31 서버 상세 요청이 들어옴")
                        response = Create_packet(0x18,GenResponseData_0x18_meta1())
                        client_socket.sendall(response)
                        print("CMetaDataPacket Type 1 0x31 서버 응답을 보냈습니다.")
                        
                    # 2단계: CMetaDataPacket Type 1 응답 (필수!)
                    elif recv_packet == bytes([0xaa,0x00,0x07,0x0f,0x02,0x00,0x03,0x32,0x32,0x32]):
                        print("CMetaDataPacket detail 1 0x32,0x32,0x32 서버 상세 요청이 들어옴")
                        response = Create_packet(0x18,GenResponseData_0x18_meta1_2())
                        client_socket.sendall(response)
                        print("CMetaDataPacket Type 1 0x32,0x32,0x32 서버응답을 보냈습니다.")
                        
                    
                    #aa001203076b313233313233083131313831313138
                    elif recv_packet[3] == 0x03:
                        print("CLoginPacket 요청이 들어옴")
                        if parse_recv_Loginpacket(recv_packet) == True:
                            response = Create_packet(0x03,GenResponseData_0x03('192.168.0.232',1511))
                            client_socket.sendall(response)
                            print("ProcessTransferServer 데이터를 서버응답으로 보냈습니다.")  
                        else:
                            print("패킷 파싱 중 오류 발생");
                           
                    #aa00010b quit
                    elif recv_packet == bytes([0xaa,0x00,0x01,0x0b]):
                        print("CQuitPacket 이 들어옴")    
                        
                        
                    else:
                        print("예상하지 못한 패킷 수신.")

        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            print(f"클라이언트 {client_address}와의 연결을 종료합니다.")
            client_socket.close()

if __name__ == "__main__":
    create_server()
    
    
    '''
    1. ProcessTransferServer (case 3) - 서버 연결/전환
    ↓
    2. Status::ProcessStatus_ (case 8) - 플레이어 상태 설정  
    ↓
    3. ProcessMapCRC (case 0x14) - 맵 파일 검증
    ↓
    4. ProcessMapSize (case 0x15) - 맵 크기/설정 ← 여기!
    ↓
    5. ProcessDrawObjects_ (case 7) - 맵 오브젝트들 로드
    '''


'''
(ProcessStatus_ 추정)
Offset 0x00: byte - 플래그 하위바이트
Offset 0x01: byte - 플래그 상위바이트
|15|14|13|12|11|10  | 9 | 8 | 7| 6 | 5  | 4 | 3  | 2 | 1  | 0  |
|  |  |  |  |  |색상|배열|특수|  |기본|상세|영역|위치|통계|상태2|상태1|


조건부 데이터 블록들 (플래그 검사 순서대로)
1. 기본 캐릭터 정보 블록 (플래그 & 0x40 ≠ 0)
Offset +0x02: byte     - 캐릭터 타입 (1=기본, 2=특수, 3=고급, 4=최고급)
Offset +0x03: byte     - 캐릭터 레벨 (1-255)
Offset +0x04: byte     - 추가 속성/상태 플래그
Offset +0x05: uint32   - 캐릭터 고유 ID (Little Endian)
             [0x05] [0x06] [0x07] [0x08]
Offset +0x09: string   - 캐릭터명 (DBCS 인코딩, null-terminated, 최대 255자)
             [길이가 가변적 - N바이트 + null]
Offset +0x09+N+1: uint32 - 경험치값 (Little Endian)
             [+0] [+1] [+2] [+3]
Offset +0x0D+N+1: uint16 - 현재 HP (Little Endian)
             [+0] [+1]
Offset +0x0F+N+1: uint16 - 현재 MP (Little Endian)  
             [+0] [+1]
Offset +0x11+N+1: byte   - STR 능력치
Offset +0x12+N+1: byte   - DEX 능력치
Offset +0x13+N+1: byte   - INT 능력치



2. 상세 캐릭터 정보 블록 (플래그 & 0x20 ≠ 0)
다음 오프셋: byte - 상세 스탯 1 (VIT - 체력)
다음 오프셋: byte - 상세 스탯 2 (LUK - 행운)
다음 오프셋: byte - 상세 스탯 3 (ATK - 공격력)
다음 오프셋: byte - 상세 스탯 4 (DEF - 방어력)
다음 오프셋: byte - 상세 스탯 5 (MATK - 마법공격력)
다음 오프셋: byte - 상세 스탯 6 (MDEF - 마법방어력)
다음 오프셋: byte - 상세 스탯 7 (HIT - 명중률)
다음 오프셋: byte - 상세 스탯 8 (FLEE - 회피율)
다음 오프셋: byte - 상세 스탯 9 (CRIT - 크리티컬)
다음 오프셋: byte - 상세 스탯 10 (ASPD - 공격속도)
다음 오프셋: byte - 상세 스탯 11 (무게 관련)
다음 오프셋: byte - 상세 스탯 12 (상태저항)
다음 오프셋: byte - 상세 스탯 13 (기타1)
다음 오프셋: byte - 상세 스탯 14 (기타2)


3. 영역/좌표 정보 블록 (플래그 & 0x10 ≠ 0)
다음 오프셋: uint16 - 시작 X좌표 (Little Endian)
다음 오프셋: uint16 - 시작 Y좌표 (Little Endian)
다음 오프셋: uint16 - 끝 X좌표 또는 너비 (Little Endian)
다음 오프셋: uint16 - 끝 Y좌표 또는 높이 (Little Endian)
             
             
4. 위치 정보 블록 (플래그 & 0x08 ≠ 0)
다음 오프셋: byte - 정밀 X좌표 (픽셀단위)
다음 오프셋: byte - 정밀 Y좌표 (픽셀단위)
다음 오프셋: byte - Z좌표 또는 레이어
다음 오프셋: byte - 방향값 (0-7, 8방향)



5. 통계 정보 블록 (플래그 & 0x04 ≠ 0)
다음 오프셋: uint32 - 통계값 1 (총 킬수)
다음 오프셋: uint32 - 통계값 2 (총 데스수)
다음 오프셋: uint32 - 통계값 3 (보유 골드)
다음 오프셋: uint32 - 통계값 4 (플레이 시간)
다음 오프셋: uint32 - 통계값 5 (퀘스트 완료수)
다음 오프셋: uint32 - 통계값 6 (PK 점수)
다음 오프셋: uint32 - 통계값 7 (길드 기여도)
다음 오프셋: uint32 - 통계값 8 (명성도)
다음 오프셋: uint32 - 통계값 9 (기타 점수)



6. 동적 배열 블록 (플래그 & 0x100 ≠ 0)
다음 오프셋: byte     - 배열 크기 N (0-255)
다음 오프셋: byte     - 데이터[0] (아이템 ID, 스킬 ID 등)
다음 오프셋: byte     - 데이터[1]
...
다음 오프셋: byte     - 데이터[N-1]
다음 오프셋: byte     - 배열 종료 마커 또는 추가 플래그



7. 색상/외형 정보 블록 (플래그 & 0x200 ≠ 0)
다음 오프셋: byte - Red 값 (0-255)
다음 오프셋: byte - Green 값 (0-255)
다음 오프셋: byte - Blue 값 (0-255)  
다음 오프셋: byte - Alpha 값 (항상 0xFF)


<실제 패킷 예시>
Hex: 01 00
Offset 0x00: 0x01  // 플래그 = 0x0001 (기본 상태만)
Offset 0x01: 0x00  // 플래그 상위바이트

Hex: 40 00 01 0A 00 78 56 34 12 50 6C 61 79 65 72 00 E8 03 00 00 64 00 32 00 0F 0A 08
Offset 0x00: 0x40  // 플래그 = 0x0040 (기본 캐릭터 정보)
Offset 0x01: 0x00  // 플래그 상위바이트
Offset 0x02: 0x01  // 캐릭터 타입 = 1 (기본)
Offset 0x03: 0x0A  // 레벨 = 10
Offset 0x04: 0x00  // 추가 속성 없음
Offset 0x05: 0x78  // 캐릭터 ID = 0x12345678 (Little Endian)
Offset 0x06: 0x56
Offset 0x07: 0x34  
Offset 0x08: 0x12
Offset 0x09: 0x50  // "Player" 문자열 시작
Offset 0x0A: 0x6C  // 'l'
Offset 0x0B: 0x61  // 'a'
Offset 0x0C: 0x79  // 'y'
Offset 0x0D: 0x65  // 'e'
Offset 0x0E: 0x72  // 'r'
Offset 0x0F: 0x00  // null terminator
Offset 0x10: 0xE8  // 경험치 = 1000 (Little Endian)
Offset 0x11: 0x03
Offset 0x12: 0x00
Offset 0x13: 0x00
Offset 0x14: 0x64  // HP = 100 (Little Endian)
Offset 0x15: 0x00
Offset 0x16: 0x32  // MP = 50 (Little Endian)
Offset 0x17: 0x00
Offset 0x18: 0x0F  // STR = 15
Offset 0x19: 0x0A  // DEX = 10
Offset 0x1A: 0x08  // INT = 8

완전한 패킷 (모든 정보 포함)
Hex: FF 03 [기본정보블록] [상세스탯14바이트] [영역정보8바이트] [위치정보4바이트] [통계정보36바이트] [동적배열] [색상정보4바이트]

플래그 = 0x03FF = 모든 블록 포함
총 크기: 약 80-150바이트 (캐릭터명 길이와 동적 배열 크기에 따라 가변)


packet_bytes = bytes([
    0xFF, 0x03, 0x02, 0x1E, 0x05, 0xA4, 0x86, 0x01, 0x00, 0x44,
    0x72, 0x61, 0x67, 0x6F, 0x6E, 0x4B, 0x6E, 0x69, 0x67, 0x68,
    0x74, 0x00, 0x40, 0x42, 0x0F, 0x00, 0x90, 0x01, 0x58, 0x02,
    0x14, 0x12, 0x0F, 0x50, 0x3C, 0x28, 0x1E, 0x96, 0x5A, 0x3C,
    0x32, 0x1E, 0x14, 0x0A, 0x08, 0x06, 0x40, 0x01, 0x20, 0x03,
    0x80, 0x02, 0xC0, 0x04, 0x7D, 0x5E, 0x3F, 0x2A, 0xC8, 0x00,
    0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00,
    0xE8, 0x03, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x58, 0x02,
    0x00, 0x00, 0xF4, 0x01, 0x00, 0x00, 0x2C, 0x01, 0x00, 0x00,
    0xA0, 0x0F, 0x00, 0x00, 0x05, 0x7B, 0x3E, 0x42, 0x1F, 0xA6,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF
])

print(f"패킷 크기: {len(packet_bytes)} 바이트")
print(f"헥스 출력: {packet_bytes.hex().upper()}")


=>
packet_bytes = bytes([0xAA, 0x00, 0x6A, 0x08,
    0xFF, 0x03, 0x02, 0x1E, 0x05, 0xA4, 0x86, 0x01, 0x00, 0x44,
    0x72, 0x61, 0x67, 0x6F, 0x6E, 0x4B, 0x6E, 0x69, 0x67, 0x68,
    0x74, 0x00, 0x40, 0x42, 0x0F, 0x00, 0x90, 0x01, 0x58, 0x02,
    0x14, 0x12, 0x0F, 0x50, 0x3C, 0x28, 0x1E, 0x96, 0x5A, 0x3C,
    0x32, 0x1E, 0x14, 0x0A, 0x08, 0x06, 0x40, 0x01, 0x20, 0x03,
    0x80, 0x02, 0xC0, 0x04, 0x7D, 0x5E, 0x3F, 0x2A, 0xC8, 0x00,
    0x00, 0x00, 0x64, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00,
    0xE8, 0x03, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x58, 0x02,
    0x00, 0x00, 0xF4, 0x01, 0x00, 0x00, 0x2C, 0x01, 0x00, 0x00,
    0xA0, 0x0F, 0x00, 0x00, 0x05, 0x7B, 0x3E, 0x42, 0x1F, 0xA6,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF
])


'''