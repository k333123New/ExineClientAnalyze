<최종정리중>
1)서버에서 SVersionCheckPacket(패킷 타입 0) 을 보낼때 서버목록 체크섬 값이 있음.
2)클라이언트에서 CMetaDataPacket 를 보내서 응답으로 SMetaDataPacket에서 서버들의 이름을 보냄
3)SMetaDataPacket에서 처리 시점에 server.dat파일을 열어서 체크섬을 계산해서 받아둔 서버목록 체크섬 값과 비교함.
=>동일 하면 정상적으로 리스트 표현함.
=>동일하지 않으면 temp\서버명.dat파일을 찾아보고 그것도 없으면 CMultiServerPacket 로 추가적인 서버 정보를 요청함.
SMultiServerPacket 응답 - "전체 서버 정보입니다"을 전해줌 -> 해당 정보를 메모리에 올리고 업데이트 하고 화면을 띄우고 server.dat로 저장함


1. CMetaDataPacket 요청 (타입 3) - "서버명 목록 주세요"
2. SMetaDataPacket 응답 - "서버명들입니다"
3. 로컬 캐시 검증 
4. CMultiServerPacket 요청 (타입 1) - "전체 서버 정보 주세요" ← 여기!
5. SMultiServerPacket 응답 - "전체 서버 정보입니다"



-----------------------
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
-----------------------

ProcessMetaDataPacket
=>struct MetaDataPacket {
    // 공통 패킷 헤더 (추정)
    uint8_t  packet_header[...];     // 패킷 헤더
    uint8_t  packet_type;            // +0x24: 패킷 타입 (0 또는 1)
    uint8_t  some_flag;              // +0x25: 플래그값
// 타입에 따른 데이터
    union {
        // Type 0: 다중 서버 목록
        struct {
            uint32_t server_list_start;  // +0x8d*4: 서버 목록 시작 포인터
            uint32_t server_list_end;    // +0x8e*4: 서버 목록 끝 포인터
            // 서버 항목들 (각각 0x204 = 516바이트)
            ServerEntry servers[];
        } multi_server;
        
        // Type 1: 단일 서버 정보
        struct {
            wchar_t server_name[256];    // +0xb*4: 서버명 (최대 512바이트)
        } single_server;
    };
};


// Type 0: 다중 서버 목록
struct MultiServerPacket {
    uint8_t  packet_type;           // 0
    uint8_t  flag_value;            // +0x25
    uint32_t server_data_start;     // +0x8d*4
    uint32_t server_data_end;       // +0x8e*4
    
    // 각 서버 항목 (516바이트씩)
    struct {
        uint8_t  padding[4];        // +0 ~ +3
        wchar_t  server_name[256];  // +4 ~ +515 (512바이트)
    } servers[(server_data_end - server_data_start) / 0x204];
};


// Type 1: 단일 서버 정보
struct SingleServerPacket {
    uint8_t  packet_type;       // 1
    uint8_t  flag_value;        // +0x25  
    wchar_t  server_name[256];  // +0xb*4 위치부터 서버명
};







다중 서버 처리시 패킷 흐름 서버명은 유니코드.
1. 패킷 타입 확인: *(char *)(param_1 + 9) == 0
2. 서버 개수 계산: (param_1[0x8e] - param_1[0x8d]) / 0x204
3. 각 서버별 처리:
   - 서버명 추출: (short *)(puVar2[0x8d] + 4 + offset)
   - DownloadAndProcessServerData()로 상세 정보 다운로드
   - AddServerToContainer()로 서버 목록에 추가
4. SaveServerListToFile()로 로컬 저장



단일 서버 처리시 패킷 흐름 서버명은 유니코드.
1. 패킷 타입 확인: *(char *)(param_1 + 9) == 1
2. 서버명 추출: (short *)(param_1 + 0xb)
3. SaveServerInfoMetaData()로 메타데이터 저장
4. DownloadAndProcessServerData()로 상세 정보 다운로드
5. AddServerToContainer()로 서버 목록에 추가




===============================
서버 정보 실제 다운로드 부분 분석 결과
코드 분석을 통해 서버 정보를 실제로 다운로드하는 부분을 찾았습니다!
1. MFGS (파일 업데이트 시스템)
게임 시작 시 InitializeMFGSUpdater 함수를 통해 파일 업데이트 시스템이 초기화됩니다:
cInitializeMFGSUpdater(1, 
    "download.nexon.co.kr/elancia/mfgs/supdate/", 
    "anonymous", 
    "esteam.nexon.co.kr", 
    3000);
2. FTP 기반 다운로드 시스템
A. 설정 정보

FTP 서버: download.nexon.co.kr/elancia/mfgs/supdate/
사용자명: anonymous (익명 FTP)
이메일: esteam.nexon.co.kr
간격: 3000ms (3초마다 체크)

B. MFGS 함수들
cMFGS_Initialize(&LAB_004ae200);  // 초기화 (콜백 함수)
MFGS_SetInterval(3000);          // 업데이트 간격 설정
MFGS_SetFTP(...);               // FTP 서버 설정
MFGS_SetShowUpdate(0);          // UI 표시 설정
MFGS_Start();                   // 업데이트 시작
3. 실제 다운로드 과정
A. 백그라운드 FTP 다운로드
1. MFGS_Start() 실행
   ↓
2. 3초마다 FTP 서버 체크
   ↓
3. download.nexon.co.kr에서 서버 정보 파일들 다운로드
   ↓
4. temp\ 폴더에 압축된 서버 정보 파일들 저장
   ↓
5. DownloadAndProcessServerData()에서 이 파일들 읽기
B. 파일 구조
FTP 서버: download.nexon.co.kr/elancia/mfgs/supdate/
├── 서울서버.dat       (압축된 서버 정보)
├── 부산서버.dat       (압축된 서버 정보)
├── TestServer.dat    (압축된 서버 정보)
└── ...

로컬: [게임폴더]\temp\
├── 서울서버          (다운로드된 압축 파일)
├── 부산서버          (다운로드된 압축 파일)
└── ...
4. 전체 시스템 흐름
[게임 시작]
    ↓
[InitializeMFGSUpdater] → FTP 업데이트 시스템 시작
    ↓
[MFGS 백그라운드 작업] → 3초마다 FTP 서버에서 파일 다운로드
    ↓                    → temp\ 폴더에 압축 파일들 저장
[ProcessMetaDataPacket] → 서버명 목록 수신
    ↓
[DownloadAndProcessServerData] → temp\[서버명] 파일 읽기
    ↓                           → DecompressData로 압축 해제
[AddServerToContainer] → 메모리에 서버 정보 저장
    ↓
[SaveServerListToFile] → server.dat 파일 생성
5. MFGS의 특징
A. 자동 업데이트

게임 실행 중 백그라운드에서 지속적으로 서버 정보 업데이트
새로운 서버 추가나 서버 정보 변경 시 자동 반영

B. FTP 기반

안정적인 파일 전송을 위해 FTP 프로토콜 사용
익명 FTP로 로그인 없이 접근 가능

C. 압축 파일

네트워크 효율성을 위해 압축된 형태로 전송
로컬에서 DecompressData()로 해제

6. 결론
서버 정보의 실제 다운로드는 MFGS(Nexon File Update System)를 통해 수행됩니다:

방식: FTP 기반 자동 업데이트 시스템
서버: download.nexon.co.kr/elancia/mfgs/supdate/
주기: 3초마다 체크하여 변경된 파일 다운로드
저장: temp\[서버명] 형태의 압축 파일로 저장 (이 파일만 있으면 동작에 지장이 없다고 함)
처리: DownloadAndProcessServerData()에서 읽어서 압축 해제 후 사용

이는 많은 넥슨 게임에서 사용하는 표준적인 파일 업데이트 시스템으로, 게임 콘텐츠뿐만 아니라 서버 정보도 함께 관리하는 통합 시스템입니다.
======================


temp\[서버명] 파일이 없이 server.dat파일만 있으면 진행이 가능해?
결론: temp[서버명] 파일을 못 읽어도 server.dat 파일이 존재하면 프로그램 진행에 문제가 없습니다. 시스템은 temp 파일이 실패할 경우 자동으로 server.dat 파일을 대안으로 사용하는 구조로 설계되어 있습니다.



체크섬이 포함된 패킷: SVersionCheckPacket

체크섬 설정 과정:
cProcessVersionCheckPacket() 함수에서:
*(undefined4 *)((int)this + 0x270) = *(undefined4 *)((int)param_1 + 0x28);

SVersionCheckPacket 구조:

param_1 + 0x28: 서버 목록의 체크섬 값
패킷 타입: 0 (케이스 0에서 처리)


패킷 처리 순서:
1. 서버 연결 후 SVersionCheckPacket 수신 (패킷 타입 0)
   └─ ProcessVersionCheckPacket 호출
      └─ 체크섬을 this + 0x270에 저장

2. 이후 SMetaDataPacket 수신 (패킷 타입 0x18)  
   └─ ProcessMetaDataPacket 호출
      └─ 저장된 체크섬과 로컬 server.dat 체크섬 비교

체크섬 사용 로직:

SVersionCheckPacket에서 서버가 클라이언트에게 "현재 서버 목록의 올바른 체크섬"을 전송
ProcessMetaDataPacket에서 이 체크섬과 로컬 server.dat 파일의 체크섬을 비교
일치하면 로컬 캐시 사용, 불일치하면 새 서버 목록 요청



결론: SVersionCheckPacket이 서버 목록의 체크섬 정보를 담고 있는 패킷입니다. 이 패킷은 버전 확인과 동시에 서버 목록의 유효성을 검증할 수 있는 체크섬을 제공합니다.

정확한 순서 정리
실제 흐름은 이렇습니다:
1단계: SVersionCheckPacket 수신

서버에서 SVersionCheckPacket(패킷 타입 0) 전송
클라이언트가 ProcessVersionCheckPacket 호출
체크섬을 this + 0x270에 저장 (param_1 + 0x28에서 가져옴)
클라이언트가 서버에게 CMetaDataPacket 요청 전송

2단계: SMetaDataPacket 수신

서버에서 SMetaDataPacket(패킷 타입 0x18) 응답
클라이언트가 ProcessMetaDataPacket 호출
로컬 server.dat 파일 로드 시도
로컬 체크섬 vs 미리 받은 체크섬 비교

3단계: 결과 처리

체크섬 일치: ActivateMainMenuPane() → 서버 목록 화면 출력
체크섬 불일치: CMultiServerPacket 요청 → 새 서버 목록 다운로드

요약:

SVersionCheckPacket에서 체크섬 받아서 저장
클라이언트가 CMetaDataPacket 요청
SMetaDataPacket 수신 (하지만 여기엔 서버명이 아니라 서버 목록 요청 트리거)
server.dat 체크섬 비교
일치하면 서버 목록 화면 출력, 불일치하면 새 목록 다운로드

SMetaDataPacket에는 서버명이 직접 들어있지 않고, 서버 목록 처리 로직을 트리거하는 역할을 합니다.