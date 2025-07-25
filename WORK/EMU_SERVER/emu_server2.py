import socket
#inrealserver
def create_server():
    host = '192.168.0.15'  # 서버 주소
    port = 1511            # 포트 번호

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

                    # CTransferServerPacket
                    if recv_packet == bytes([0xAA,0x00,0x01,0x10]):
                         print("CTransferServerPacket 이 들어옴")
                         #aa 00 09 02 00 03 44 D5 C9 B9 74 C7  응답0이 정상
                         initial_response = bytes([
                         0xAA ,0x00 ,0x09 ,0x02 ,0x00 ,0x03 ,0x44 ,0xD5 ,0xC9 ,0xB9 ,0x74 ,0xC7
                         ])
                         client_socket.sendall(initial_response)
                         print("CheckPacket 데이터를 서버응답으로 보냈습니다.")
                         
                    elif recv_packet == bytes([0xAA, 0x00, 0x02, 0x0B, 0x00]):
                        response = bytes([
                            0xAA, 0x00, 0x13, 0x7E, 0x1B, 0x43, 0x4F, 0x4E, 0x4E, 0x45,
                            0x43, 0x54, 0x45, 0x44, 0x20, 0x53, 0x45, 0x52, 0x56, 0x45,
                            0x52, 0x0A
                        ])
                        client_socket.sendall(response)
                        print("응답을 보냈습니다.")
                        
                    elif recv_packet == bytes([0xaa,0x00,0x12,0x03,0x07,0x6b,0x33,0x33,0x33,0x31,0x32,0x33,0x08,0x31,0x32,0x34,0x38,0x31,0x32,0x34,0x38]):
                        print("CLoginPacket 요청이 들어옴")
                        
                        #0x03 type
                        # AA 00 xx 03 XX XX XX XX(ip) YY YY(port) dat2len dat2
                        response = bytes([
                        0xAA ,0x00 ,0x08 ,0x03, 0x0F, 0x00 ,0xA8 ,0xC0 ,0x05 ,0xE7 ,0x00
                        ])
                        client_socket.sendall(response)
                        print("ProcessTransferServer 데이터를 서버응답으로 보냈습니다.")       
                         
                    elif recv_packet == bytes([0xaa,0x00,0x02,0x06,0x03]):
                        print("CManufactureRequest 이 들어옴")
                        
                        '''
                        #7d3aff99(Reach To MapPane!!! only with 7d3aff99)
                        response = bytes([
                        0xAA, 0x00, 0x07, 0x4A, 0x00, 0x00, 0x7d, 0x3a, 0xff, 0x99
                        ])
                        client_socket.sendall(response)
                        print("SBadGuyPacket 데이터를 서버응답으로 보냈습니다.(mainmenupane test)")
                        '''
                        
                        #----------------MapPane----------------
                         
                         
                         
                        #ProcessPutHumanObject?? 0x33
                        response = bytes([
                        0xAA, 
                        0x00, 0x0X, 
                        0x33, 
                        0x01,
                        #0x03,
                        ])
                        client_socket.sendall(response)
                        print("SPutHumanObject 데이터를 서버응답으로 보냈습니다.")
                         
                         
                         
                        #ProcessUserAppearance? 0x05
                        #OK!!!(UI Apply! pos:555,555)
                        response = bytes([
                        0xAA, 
                        0x00, 0x1D, 
                        0x05,
                        0x00, 0x00, 0x00, 0x00,
                        0x00,
                        0x00,
                        0x00, 0x00, 
                        0x00, 0x00, 
                        0x00, 0x00, 
                        0x00, 0x00, 
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x00,
                        0x11,
                        
                        0x00,
                        0x00,
                        0x00,
                        
                        0x00, 0x00, 
                        
                        0x00
                        ])
                        client_socket.sendall(response)
                        print("SUserAppearance 데이터를 서버응답으로 보냈습니다.")
                        
                        
                        #ProcessMessage? 0x0A
                        #OK!!!
                        response = bytes([
                        0xAA, 
                        0x00, 0x0E, 
                        0x0A,
                        0x01, 
                        0x01,  
                        #0X00, 0x04, 0x4C ,0xD1 ,0xA4 ,0xC2 ,0xB8 ,0xD2 ,0xF5 ,0xB9 #EUC-KR (또는 CP949)!!!
                        0x0A, 0xC7, 0xEC, 0xB1, 0xD7, 0xB3, 0xD7, 0xC0, 0xCC, 0xBE, 0xC6 #EUC-KR!!!, len : real bytes
                        ])
                        client_socket.sendall(response)
                        print("SMessagePacket 데이터를 서버응답으로 보냈습니다.")
                        
                       
                        
                        #ProcessSay? 0x0D
                        #OK!!!(UI Apply! chatdialog! sometext)
                        response = bytes([
                        0xAA, 
                        0x00, 0x12, 
                        0x0D, 
                        0x01, 
                        0x01,0x01,0x01,0x01,
                        0x01,
                        0x0A, 0xC7, 0xEC, 0xB1, 0xD7, 0xB3, 0xD7, 0xC0, 0xCC, 0xBE, 0xC6 #EUC-KR!!!, len : real bytes
                        ])
                        client_socket.sendall(response)
                        print("SMessagePacket 데이터를 서버응답으로 보냈습니다.")
                        
                         
                        #ProcessMapSize? 0x15
                        #OK! minimap -> some name
                        response = bytes([
                        0xAA, 
                        0x00, 0x15, 
                        0x15, 
                        
                        #0x00,0x01, #10000 arke
                        0x27,0x10, #MAP Number! 10000 arke
                        0x00,0x00, #not used
                        0x00,0x00, #not used
                        0x0A,#00001010 → 0x0A (bit flag)
                        0x01,
                        0x01, 
                        #c7 ec b1 d7 b3 d7 c0 cc be c6 (헤그네이아) https://dencode.com/
                        #EUC-KR!!!, len : real bytes Map Name
                        0x0A, 0xC7, 0xEC, 0xB1, 0xD7, 0xB3, 0xD7, 0xC0, 0xCC, 0xBE, 0xC6 
                         
                        ])
                        client_socket.sendall(response)
                        print("SMapSize 데이터를 서버응답으로 보냈습니다.")
                         
                        #ProcessMapCRC? 0x14 
                        #OK! 0x03 => 잘못된 파일 이름입니다. & 종료
                        #순서!!! (ProcessMapSize -> ProcessMapCRC, 0x01 OK)
                        response = bytes([
                        0xAA, 
                        0x00, 0x02, 
                        0x14, 
                        0x01,
                        #0x03,
                        ])
                        client_socket.sendall(response)
                        print("SMapCRC 데이터를 서버응답으로 보냈습니다.")
                        
                         #OK! order!!!!!!
                        #ProcessUserPosition	0x04
                        response = bytes([
                        0xAA, 
                        0x00, 0x09, 
                        0x04,
                        0x00, 0x01, 
                        0x00, 0x01,  
                        0x00, 0x01, 
                        0x00, 0x01
                        ])
                        client_socket.sendall(response)
                        print("SUserPositionPacket 데이터를 서버응답으로 보냈습니다.")
                        
                        
                        #ProcessPlaySound? 0x19 
                        #OK!!! Perfect!
                        #00001_arke~00014 mp3
                        #00000 ~ 00389.wav
                        response = bytes([
                        0xAA, 
                        0x00, 0x04, 
                        0x19,
                        
                        0x01, #type 0x00 => wav(decode2), 0x01 => bgm(decode1, decode1)
                        0x01, #file number(mode:bgm)
                        0x01  #loop?(mode:bgm)
                        ])
                        client_socket.sendall(response)
                        print("SPlaySound 데이터를 서버응답으로 보냈습니다.")
                        
                        
                        #ProcessChangeHour?? 0x20
                        #OK!!! Perfect!!! (minimap time display)
                        response = bytes([
                        0xAA, 
                        0x00, 0x03, 
                        0x20,
                        0x09, #hour
                        0x0B #min
                        ])
                        client_socket.sendall(response)
                        print("SChangeHour 데이터를 서버응답으로 보냈습니다.")
                         
                         
                        
                        
                         
                        
                        
                        #ProcessRemoveObjects? E
                        
                        #ProcessAddInventory? F
                        
                        #ProcessRemoveInventory? 0x10
                        
                        #ProcessChangeDirection? 0x11
                        
                        #ProcessUseActionEnd? 0x12
                        
                        #ProcessDamageEffect? 0x13
                         
                        #ProcessMove? 0x0B
                        
                        #ProcessMoveObject? 0x0C
                        
                        #ProcessMetaData?? 0x18
                        
                        #ProcessMotion?? 0x1a
                        
                        
                        '''
                        #ProcessStatus? 0x08 
                        #ERR! maybe order?
                        response = bytes([
                        0xAA, 
                        0x00, 0x20, 
                        0x08,
                        
                        0x00, 0x40,
                        
                        0x01,
                        0x01,
                        0x01,
                        0x01, 0x00, 0x00, 0x00,
                        0x0A, 0xC7, 0xEC, 0xB1, 0xD7, 0xB3, 0xD7, 0xC0, 0xCC, 0xBE, 0xC6,
                        0x00, 0x00, 0x00, 0x01,
                        0x00, 0x01,
                        0x00, 0x01,
                        0x01,
                        0x01,
                        0x01
                        ])
                        client_socket.sendall(response)
                        print("SStatusPacket 데이터(최소)를 서버응답으로 보냈습니다.")
                        '''
                        
                        
                        
                        #ProcessMoveHumanAck? 0x06
                        
                        #ProcessDrawObjects? 0x07
                        
                        
                        #ProcessEffect?? 0x29
                        
                        #ProcessAddLastingSpell?? 0x2c
                        
                        #ProcessRemoveLastingSpell?? 0x2d
                        
                        #ProcessFieldMap? 0x2e
                         
                       
                        
                        #ProcessObjectInfoReply?? 0x34
                        
                        #ProcessRemoveEquipment? 0x38
                        
                        #ProcessUpdateGroupMembers?? 0x3a
                        
                        #ProcessRequestCRC?? 0x3b
                        
                        #ProcessCancelCastSpell? 0x48
                        
                        #ProcessPortrait?? 0x49
                         
                        #ProcessBlockClient? 0x51
                        
                        #ProcessDieObjects?? 0x5f
                        
                        #ProcessAddAction?? 0x62
                        
                        #ProcessRemoveAction? 0x63
                        
                        #ProcessMovePath? 0x64
                        
                        #ProcessCheckTime?? 0x66
                        
                        #ProcessPassive? 0x6d
                        
                        #ProcessActionRequisite? 0x6f
                        #----------------MapPane----------------
                        
                        
                        
                        
                        
                        
                        #OK
                        '''
                        #SManufactureReply	0x67
                        response = bytes([
                        0xAA ,0x00 ,0x02 ,0x67 ,0x01
                        ])
                        client_socket.sendall(response)
                        print("SManufactureReply 데이터를 서버응답으로 보냈습니다.")
                        '''
                        
                        #SUserAppearancePacket 0x05
                        
                        '''
                        #SStatusPacket 0x08
                        response = bytes([
                        0xAA, 
                        
                        #0x00, 0x61, #0x66, 
                        0x00, 0x66,
                        
                        0x08,
                        0x03, 0xff,
                        0x02, 
                        0x1E, 
                        0x05,
                        0xA4, 0x86, 0x01, 0x00, #char id
                        0x04, 0x4C ,0xD1 ,0xA4 ,0xC2 ,0xB8 ,0xD2 ,0xF5 ,0xB9, #char name
                        0x40, 0x42, 0x0F, 0x00,
                        0x90, 0x01, 
                        0x58, 0x02,
                        0x14, 
                        0x12, 
                        0x0F,
                        
                        0x50, 
                        0x3C, 
                        0x28, 
                        0x1E, 
                        0x96, 
                        0x5A, 
                        0x3C,
                        0x32, 
                        0x1E, 
                        0x14, 
                        0x0A, 
                        0x08, 
                        0x06, 
                        0x04, 
                        
                        
                        0x40, 0x01,
                        0x20, 0x03,
                        0x80, 0x02, 
                        0xC0, 0x04, 
                        
                        0x7D, 
                        0x5E, 
                        0x3F, 
                        0x2A,

                        0xC8, 0x00, 0x00, 0x00, 
                        0x64, 0x00, 0x00, 0x00, 
                        0x10, 0x27, 0x00, 0x00,
                        0xE8, 0x03, 0x00, 0x00, 
                        0x0C, 0x00, 0x00, 0x00, 
                        0x58, 0x02, 0x00, 0x00, 
                        0xF4, 0x01, 0x00, 0x00, 
                        0x2C, 0x01, 0x00, 0x00,
                        0xA0, 0x0F, 0x00, 0x00, 
                        
                        #0x00,
                        0x05, #count
                        0x7B, 0x3E, 0x42, 0x1F, 0xA6,
                        0x00,
                        
                        0xFF, 
                        0xFF,
                        0xFF
                        ])
                        client_socket.sendall(response)
                        print("SStatusPacket 데이터를 서버응답으로 보냈습니다.")  
                        '''
                        
                        '''
                        #map size packet(= map info)
                        #0xAA ,0x00 ,0x13 ,0x15 ,0x00 ,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x04 ,0x4C ,0xD1 ,0xA4 ,0xC2 ,0xB8 ,0xD2 ,0xF5 ,0xB9
                        #aa 00 11 15 00 01 00 00 00 00 00 04 4C D1 A4 C2 B8 D2 F5 B9
                        response = bytes([
                        0xAA ,0x00 ,0x13 ,0x15 ,
                        0x00 ,0x00 ,#map id
                        0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,
                        0x04 ,0x4C ,0xD1 ,0xA4 ,0xC2 ,0xB8 ,0xD2 ,0xF5 ,0xB9 #map name
                        ])
                        client_socket.sendall(response)
                        print("MapSizePacket 데이터를 서버응답으로 보냈습니다.")                        
                        '''
                        
                        
                        '''
                        #test mappane process
                        #0x03 type
                        # AA 00 xx 03 XX XX XX XX(ip) YY YY(port) dat2len dat2
                        response = bytes([
                        0xAA ,0x00 ,0x07 ,0xC0, 0xA8 ,0x00 ,0x0F ,0x05 ,0xE6 ,0x00
                        ])
                        client_socket.sendall(response)
                        print("ProcessTransferServer 데이터를 서버응답으로 보냈습니다.")         
                        '''
                        
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