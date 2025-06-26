server.dat 
[Header]
- 1 byte: 서버 개수 (Decoder::Decode1으로 읽음)

[Server Entry] × 서버 개수만큼 반복
각 서버 항목당 데이터:

- 1 byte: 알 수 없는 플래그/상태값 
server_status (1바이트):
서버 온라인/오프라인 상태 표시에 사용하는 것을 확인함.
0 = 오프라인, 1 = 온라인, 2 = 점검중 등
enum ServerStatus {
    SERVER_OFFLINE    = 0,  // 오프라인 (회색 표시)
    SERVER_ONLINE     = 1,  // 온라인 (정상 표시)
    SERVER_BUSY       = 2,  // 혼잡 (노란색 표시)
    SERVER_FULL       = 3,  // 만원 (빨간색 표시)
    SERVER_MAINTENANCE = 4, // 점검중 (특별 표시)
    // 기타 상태들...
};


- 4 bytes: 서버 ID 또는 포트 번호
server_port (4바이트):
포트 번호 네트워크 연결에 사용하는것을 확인함.


- 2 bytes: 추가 정보 (아마도 서버 타입이나 상태)
server_type (2바이트):
서버 종류 (PvP, PvE, 테스트 서버 등) 게임 모드 구분 =>현재 분석에서는 사용되는 곳이 없다고함!!!
enum ServerType {
    SERVER_TYPE_NORMAL    = 0,  // 일반 서버
    SERVER_TYPE_PVP       = 1,  // PvP 서버  
    SERVER_TYPE_PVE       = 2,  // PvE 서버
    SERVER_TYPE_HARDCORE  = 3,  // 하드코어 서버
    SERVER_TYPE_EVENT     = 4,  // 이벤트 서버
    SERVER_TYPE_TEST      = 5,  // 테스트 서버
    // 기타...
};


- 1 byte: 또 다른 플래그값
server_flags (1바이트):
추가 서버 설정 플래그들. 신규/추천 서버 표시, 캐릭터 생성 가능 여부 등=> 현재 분석에서는 사용되는 곳이 없다고함!!!
enum ServerFlags {
    SERVER_FLAG_NONE         = 0x00,  // 기본값
    SERVER_FLAG_NEW          = 0x01,  // 신규 서버 (NEW 아이콘)
    SERVER_FLAG_RECOMMENDED  = 0x02,  // 추천 서버 (★ 표시)
    SERVER_FLAG_EVENT        = 0x04,  // 이벤트 서버 (이벤트 아이콘)
    SERVER_FLAG_PVP_ENABLED  = 0x08,  // PvP 허용
    SERVER_FLAG_HARDCORE     = 0x10,  // 하드코어 모드
    SERVER_FLAG_BEGINNER     = 0x20,  // 초보자 서버
    SERVER_FLAG_ADULT_ONLY   = 0x40,  // 성인 전용
    SERVER_FLAG_PREMIUM      = 0x80,  // 프리미엄 서버
};


- 255 bytes: 서버 이름 (문자열)
server_name (255바이트):
서버 이름 (유니코드 문자열)
UI에 표시되는 서버명
->첫바이트에 길이가 있음. 뒷부분에 실제정보가 있음. => 실제로 다양하게 사용되는 것을 확인함!!!
server_name 필드는 가장 활발하게 사용되는 필드로:
서버 식별: 고유한 서버 구분자로 사용
UI 표시: 사용자에게 보여지는 서버 이름
데이터 구조: 서버 컨테이너에서 정렬/검색 키
네트워크: 서버-클라이언트 간 통신에서 서버 식별
파일 시스템: 서버별 설정/캐시 파일 관리



- 255 bytes: 서버 주소/IP (문자열) 
server_address (255바이트):
서버 IP 주소 또는 도메인
실제 연결에 사용되는 주소
->첫바이트에 길이가 있음. 뒷부분에 실제정보가 있음. => 네트워크에서 실제로 사용하는 것을 확인함!!!


- 255 bytes: 서버 설명 (문자열)
server_description (255바이트):
서버 설명
서버 특성, 이벤트 정보 등
->첫바이트에 길이가 있음. 뒷부분에 실제정보가 있음.=> 현재 분석한 코드에서는 server_description 필드가 직접적으로 사용되지 않고 있습니다.



- 65535 bytes: 확장 데이터 (FUN_0044c760으로 처리) => 체크섬 계산에는 포함되지 않음!!! 따라서 비워둬도됨.또한 패킷에서는 없는 영역임.
extended_data (65535바이트):
확장 서버 정보
서버별 상세 설정, 캐릭터 수, 부하 정보 등
// 추정되는 확장 데이터 구조
struct ExtendedServerData {
    uint32_t last_connect_time;     // 마지막 접속 시간
    uint32_t total_playtime;        // 총 플레이 시간
    char     favorite_characters[MAX_CHARS][32]; // 즐겨찾는 캐릭터들
    uint32_t client_preferences;   // 클라이언트 설정
    char     user_notes[512];       // 사용자 메모
    uint8_t  server_bookmarks;      // 북마크 설정
    // 기타 클라이언트 전용 데이터...
};





참고
1. 네트워크에서 서버 정보를 받는 방식
A. 메타데이터 패킷 (ProcessMetaDataPacket)

서버명만 포함된 간단한 패킷
각 서버당 516바이트 크기

B. 상세 정보 다운로드 (DownloadAndProcessServerData)

서버명으로 상세 정보를 별도 다운로드
HTTP나 별도 프로토콜 사용

C. 확장 데이터 패킷 (ProcessSStipulationPacket_Maybe_FUN_0048b630)

extended_data 영역에 데이터 저장
FUN_004b56e0에서 오프셋 0x608에 저장

2. 패킷에서 server.dat로의 변환 순서
기본적으로 네트워크 패킷에는 server.dat의 모든 필드가 포함되지 않습니다. 대신:

서버명만 패킷으로 수신
서버별 상세 정보는 별도 다운로드
클라이언트에서 로컬 정보와 결합하여 server.dat 생성

3. 실제 변환 과정
c// 추정되는 패킷 → server.dat 변환 과정
1. 네트워크 패킷 수신 (서버명만)
2. CreateServerInfoObject() - 서버 객체 생성
3. DownloadAndProcessServerData() - 서버 상세 정보 다운로드
4. 클라이언트에서 기본값이나 캐시된 값으로 나머지 필드 채움:
   - server_status = 계산된 상태값
   - server_id_or_port = 설정값 또는 기본값
   - server_type = 설정값 또는 기본값  
   - server_flags = 설정값 또는 기본값
   - server_address = 다운로드된 정보 또는 설정값
   - server_description = 다운로드된 정보 또는 기본값
   - extended_data = 별도 패킷으로 수신 또는 로컬 생성
5. SaveServerListToFile() - 완성된 정보를 server.dat에 저장
결론: 네트워크 패킷에는 server.dat의 전체 구조가 직접 포함되지 않으며, 대신 단편적인 정보들을 여러 경로로 받아서 클라이언트에서 조합하여 완전한 서버 정보를 만듭니다.