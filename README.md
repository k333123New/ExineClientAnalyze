"# ExineClientAnalyze" 

ghidra_11.3.1_PUBLIC


---------fact check not yet!-----
[Thread::AddMessage]
메시지 타입별로 분기 처리:

case 3, 4: 소켓 연결 재설정
case 5: HandleIncomingTCPIPPacket - 들어오는 패킷 처리
case 6: ProcessSendPacketMessage - 패킷 전송 처리
case 7: CPacket 인코딩 후 전송
case 8: 포인터 설정
case 9: 직접 소켓 전송
case 0xc: 메모리 버퍼 관리
case 0xd, 0xe: 기타 처리


링버퍼에서 꺼낸 메시지의 첫 번째 매개변수가 메시지 타입이고, 나머지 매개변수들이 메시지 데이터입니다.
이 함수는 Thread의 가상함수를 오버라이드한 것으로, Thread에서 생성된 스레드가 링버퍼에서 메시지를 꺼내서 이 함수를 호출합니다.

즉, Thread::AddMessage → RingBuffer::AddElem → Socket::DispatchMessageW의 흐름으로 메시지가 처리됩니다!


---------fact check not yet!-----
SMultiServerPacket 구조 (각 서버 정보 0x60c = 1548 바이트):
오프셋크기내용
0x0 1 바이트 서버 타입/ID
0x4 4바이트서버 관련 정보
0x8 2바이트포트 번호
0x9 1바이트서버 상태
0xc 512바이트서버 이름 (유니코드)
0x20c 512바이트서버 IP 주소 (유니코드)
0x40c 512바이트서버 설명 (유니코드)
0x60c ...다음 서버 정보
요약:
ProcessMultiServer 함수는 서버로부터 받은 SMultiServerPacket을 파싱하여:

여러 서버들의 정보(이름, IP, 설명 등)를 추출
각 서버 정보를 클라이언트의 서버 목록에 추가
서버 목록을 로컬 파일로 저장

추정되는 실제 패킷 구조:
SMultiServerPacket:
- 헤더 (패킷타입 0x56 등)
- 서버 개수: 1바이트
- 각 서버마다:
  - 서버타입: 1바이트
  - 서버정보(아이피임): 4바이트  
  - 포트: 2바이트
  - 상태: 1바이트
  - 서버이름길이: 2바이트
  - 서버이름: 가변길이 (유니코드)
  - IP주소길이: 2바이트
  - IP주소: 가변길이 (유니코드)
  - 설명길이: 2바이트  
  - 설명: 가변길이 (유니코드)
  
  --

Server.dat 파일은 암호화나 압축 없이 단순한 바이너리 형태로 저장됩니다.
중요!!! 서버 아이피 쪽은 리틀엔디언임.

------
pk
아인소프
케이네인
디토미아
콰브나토

npk
디아크리노
헤그네이아
프로네마
에이레네

SMultiServerPacket (0x56):
┌─────────────────────────────────────────────────────────────┐
│ [패킷 헤더]                                                 │
│   - 패킷 타입: 0x56                                         │
│   - 패킷 크기: 가변                                         │
├─────────────────────────────────────────────────────────────┤
│ [서버 정보 섹션]                                            │
│   - 총 서버 개수: 1바이트 (최대 8개)                       │
├─────────────────────────────────────────────────────────────┤
│ [PK 모드 서버들] (최대 4개)                                 │
│   └ 서버1:                                                  │
│     - 서버 타입: 1바이트 (0x00 = PK 모드)                  │
│     - 서버 ID: 4바이트                                      │
│     - 포트 번호: 2바이트                                    │
│     - 서버 상태: 1바이트 (온라인/오프라인/점검중)           │
│     - 서버 이름 길이: 1바이트                               │
│     - 서버 이름: 가변길이 (유니코드)                        │
│     - 서버 IP 길이: 1바이트                                 │
│     - 서버 IP: 가변길이 (유니코드)                          │
│     - 서버 설명 길이: 1바이트                               │
│     - 서버 설명: 가변길이 (유니코드)                        │
│     - 추가 정보 길이: 2바이트                               │
│     - 추가 정보: 가변길이 (접속자 수, 채널 정보 등)         │
│   └ 서버2: (동일 구조)                                      │
│   └ 서버3: (동일 구조)                                      │
│   └ 서버4: (동일 구조)                                      │
├─────────────────────────────────────────────────────────────┤
│ [NPK 모드 서버들] (최대 4개)                                │
│   └ 서버1:                                                  │
│     - 서버 타입: 1바이트 (0x01 = NPK 모드)                 │
│     - (나머지 구조는 PK 서버와 동일)                        │
│   └ 서버2: (동일 구조)                                      │
│   └ 서버3: (동일 구조)                                      │
│   └ 서버4: (동일 구조)                                      │
└─────────────────────────────────────────────────────────────┘

ProcessMultiServer에서의 처리 흐름:
// 1. 서버 개수 읽기
서버개수 = 패킷에서_읽기();  // 최대 8개

// 2. 각 서버 정보 파싱
for (int i = 0; i < 서버개수; i++) {
    서버타입 = 패킷에서_읽기();           // 0x00=PK, 0x01=NPK
    서버ID = 패킷에서_읽기();
    포트 = 패킷에서_읽기();
    상태 = 패킷에서_읽기();
    
    서버이름 = 길이와함께_문자열읽기();    // 1바이트 길이 + 유니코드
    서버IP = 길이와함께_문자열읽기();
    서버설명 = 길이와함께_문자열읽기();
    추가정보 = 길이와함께_데이터읽기();   // 2바이트 길이 + 데이터
    
    // 3. 메모리 구조체에 저장 (0x60c 바이트 고정 크기로)
    AddServerToList(서버정보);
}


UI에서의 분류 처리:

// UpdateServerListUI에서:
for (각_서버) {
    if (서버타입 == 0x00) {
        // PK 모드 서버 -> this + 0x274 컨테이너에 추가
        PK컨테이너에_추가(서버정보);
    } else if (서버타입 == 0x01) {
        // NPK 모드 서버 -> this + 0x284 컨테이너에 추가  
        NPK컨테이너에_추가(서버정보);
    }
}

// 각 모드별 최대 4개까지만 UI에 표시
PK모드_UI표시(최대4개);
NPK모드_UI표시(최대4개);


---
로그인 인증은 다음과 같은 흐름입니다:

서버 선택 → CMultiServerPacket(0x57) 전송
로그인 인증 → CLoginPacket(0x03) 전송
서버 응답 → STransferServerPacket(0x03) 수신
게임 서버 연결 → 새로운 IP/포트로 연결 후 CTransferServerPacket 전송

이제 로그인 서버에서 인증 후 실제 게임 서버로 연결이 전환되는 구조가 명확해졌습니다!
--로그인 인증은 다음과 같은 흐름입니다:

서버 선택 → CMultiServerPacket(0x57) 전송
로그인 인증 → CLoginPacket(0x03) 전송
서버 응답 → STransferServerPacket(0x03) 수신
게임 서버 연결 → 새로운 IP/포트로 연결 후 CTransferServerPacket 전송

이제 로그인 서버에서 인증 후 실제 게임 서버로 연결이 전환되는 구조가 명확해졌습니다!

-----
STransferServerPacket:
┌─────────────────────────────────────┐
│ [패킷 헤더]                         │
│   - 패킷 타입: 0x03                 │
├─────────────────────────────────────┤
│ [로그인 결과 분기]                  │
│   case 1: 로그인 성공               │
│     - 게임 서버 IP: 오프셋 0x24     │
│     - 게임 서버 포트: 오프셋 0x28   │
│     - 인증 토큰 길이: 오프셋 0x2a   │
│     - 인증 토큰 데이터: 오프셋 0x2b │
│                                     │
│   case 2: 로그인 실패               │
│     - NULL 패킷 또는 빈 데이터      │
│     - 에러 코드 (선택적)            │
└─────────────────────────────────────┘

-------
클라이언트 → 게임서버: CTransferServerPacket(인증토큰)
게임서버 → 클라이언트: SCheckPacket(인증결과)

if (인증성공) {
    게임서버 → 클라이언트: 각종 게임 데이터 패킷들
    - 캐릭터 정보
    - 맵 데이터  
    - 다른 플레이어 정보
    - 인벤토리 정보
    등등...
} else {
    에러 메시지 표시
}

-----------------
게임 화면 표시 후 서버에서 보내야 하는 필수 패킷들:

맵 정보 패킷들:

SMapSizePacket - 맵 크기 정보
SMapCRCPacket - 맵 데이터 무결성 체크
SMapStatusPacket - 맵 상태 정보


플레이어 캐릭터 정보:

SPutHumanObjectPacket - 플레이어 캐릭터 배치


인벤토리 및 장비 정보:

SAddInventoryPacket - 인벤토리 아이템들
SAddEquipmentPacket - 장착한 장비들


스킬 및 마법 정보:

SAddActionPacket - 보유 스킬/액션들
SAddLastingSpellPacket - 지속 효과 마법들


다른 플레이어 및 오브젝트:

SAddUserPacket - 주변 다른 플레이어들
기타 게임 오브젝트들



전송 순서:
1. 맵 정보 패킷들 (게임 월드 준비)
2. 플레이어 캐릭터 정보 (자신의 상태)
3. 인벤토리/장비 정보 (소유 아이템들)
4. 스킬/마법 정보 (능력치)
5. 주변 환경 정보 (다른 플레이어, 오브젝트)
이 패킷들이 모두 전송되어야 클라이언트에서 완전한 게임 화면을 표시하고 플레이할 수 있습니다.

1. CTransferServerPacket(인증토큰) 수신
2. 토큰 검증 성공
3. SCheckPacket(0) 전송 → InitializeGameWorld() 호출
4. 즉시 연속으로 필수 패킷들 전송:
   - SMapSizePacket
   - SMapCRCPacket  
   - SPutHumanObjectPacket
   - SAddInventoryPacket (여러 개)
   - SAddEquipmentPacket (여러 개)
   - SAddActionPacket (여러 개)
   - SAddUserPacket (주변 플레이어들)
   - 기타 게임 상태 패킷들

   ------------------------

   게임 초기화 완료 후 서버에서 자동 전송:

1. SMapCRCPacket (0x14)
   └─ 맵 파일 무결성 확인

2. SMapSizePacket (0x15) 
   └─ 맵 크기 및 기본 정보

3. SFieldMapPacket (0x2e)
   └─ 필드 맵 상세 정보 (지형, 오브젝트 등)

4. SPutHumanObjectPacket (0x33)
   └─ 플레이어 초기 위치 및 상태
   └─ X, Y 좌표, 방향, HP/MP 등

5. 기타 초기화 패킷들
   └─ SAddInventoryPacket (인벤토리)
   └─ SAddEquipmentPacket (장비)
   └─ SAddActionPacket (스킬)
   └─ SAddUserPacket (주변 플레이어)

   
  접속 후
**패킷 전송 시점:**
- ✅ **사용자 입력 시**: 이동, 공격, 아이템 사용 등
- ✅ **게임 이벤트 시**: 다른 플레이어 행동, 서버 이벤트 등
- ❌ **자동/주기적 전송**: 찾을 수 없음

따라서 **완전히 idle 상태에서는 패킷 전송이 없고**, 사용자가 행동을 취할 때만 해당 패킷이 전송됩니다.

---
패킷 구조 검증 위치: HandleIncomingTCPIPPacket (0x0052b640)
1. 패킷 헤더 검증
c// 패킷 시작 바이트 검증 (0xAA = -0x56)
if ((char)local_4 == -0x56) {
    *(undefined4 *)((int)param_1 + 0xc098) = 1;  // 패킷 상태 플래그 설정
    *(undefined4 *)((int)param_1 + 0xc09c) = 0;  // 읽기 카운터 초기화
    *(undefined4 *)((int)param_1 + 0xc0a0) = 0;  // 패킷 길이 초기화
}
2. 패킷 길이 검증
celse if (iVar1 == 0) {
    // 패킷 길이의 상위 바이트
    *(uint *)((int)param_1 + 0xc0a0) = 
         *(uint *)((int)param_1 + 0xc0a0) | (local_4 & 0xff) << 8;
}
else if (iVar1 == 1) {
    // 패킷 길이의 하위 바이트
    *(uint *)((int)param_1 + 0xc0a0) = 
         *(uint *)((int)param_1 + 0xc0a0) | local_4 & 0xff;
}
3. 패킷 완성도 검증
cif (iVar1 + -1 == *(int *)((int)param_1 + 0xc0a0)) {
    // 패킷 데이터가 모두 수신되었는지 확인
    *(undefined1 *)(*(int *)((int)param_1 + 0xc0a0) + 0x8098 + (int)param_1) = 0;
4. 패킷 타입 검증 및 생성
cif (((0 < iVar1) && (pbVar5 = (byte *)((int)param_1 + 0x8098), pbVar5 != (byte *)0x0)) &&
   (pSVar3 = (SPacket *)PacketFactory::CreateSPacketFromCode(DAT_00626db4,(uint)*pbVar5),
    pSVar3 != (SPacket *)0x0)) {
5. 패킷 디코딩 및 검증
cpbVar5[iVar1] = 0;  // NULL 종료 문자 추가
iVar1 = SPacket::Decode(pSVar3,pbVar5,iVar1);  // 패킷 구조 디코딩
if (iVar1 != 0) {
    // 디코딩 성공 시 메시지 큐로 전달
    (*UNIPostMessage)(uVar2,uVar6,pSVar3,uVar7);
}
핵심 검증 순서:

헤더 바이트 검증 (0xAA)
패킷 길이 검증 (2바이트)
패킷 완성도 확인
패킷 타입 검증 (첫 번째 데이터 바이트)
구조 디코딩 검증 (SPacket::Decode)

이 함수가 모든 패킷이 개별 처리 함수로 분산되기 전에 공통적으로 거치는 구조 검증 지점입니다!


우선 어디에서 CMultiServerPacket::CMultiServerPacket를 날린지 확인해볼것
ProcessMetaData 
어느 시점에 패널이 바뀌면서 해당 패킷이 처리가 안되는 것으로 보임.
이에 따라 서버파일을 직접 작성하는것으로 방향을 바꿈.
서버파일은 설치경로\RData\Server.dat임
(설치경로\Server.dat로 해도되지만 한번 실행하고나면 저 위지로 옮겨짐)
1 byte(server count)
1 byte(server type 0x00 ->pk 0x01 ->npk)
4 byte(Server id)
2 byte(server port)
1 byte(server status 0x00->online, 0x01->offline, 0x02 ->maintenance)
len 1 bytes + string n*2 bytes(max 255*2) (server name)
len 1 bytes + string n*2 bytes(max 255*2) (server ip)
len 1 bytes + string n*2 bytes(max 255*2) (server desc)
len 2 bytes + string n*2 bytes(max 65535) (server additional info[connected user?, chnnel info?])

[서버 정보 섹션]                                            │
│   - 총 서버 개수: 1바이트 (최대 8개)                       │
├─────────────────────────────────────────────────────────────┤
│ [PK 모드 서버들] (최대 4개)                                 │
│   └ 서버1:                                                  │
│     - 서버 타입: 1바이트 (0x00 = PK 모드)                  │
│     - 서버 ID: 4바이트                                      │
│     - 포트 번호: 2바이트                                    │
│     - 서버 상태: 1바이트 (온라인/오프라인/점검중)           │
│     - 서버 이름 길이: 1바이트                               │
│     - 서버 이름: 가변길이 (유니코드, 즉 길이*2)                        │
│     - 서버 IP 길이: 1바이트                                 │
│     - 서버 IP: 가변길이 (유니코드, 즉 길이*2)                          │
│     - 서버 설명 길이: 1바이트                               │
│     - 서버 설명: 가변길이 (유니코드, 즉 길이*2)                        │
│     - 추가 정보 길이: 2바이트                               │
│     - 추가 정보: 가변길이 , 즉 길이*2(접속자 수, 채널 정보 등)         │
│   └ 서버2: (동일 구조)                                      │
│   └ 서버3: (동일 구조)                                      │
│   └ 서버4: (동일 구조)                           

==============================
실제 데이터 수정해서 확인해본 결과 정리중
서버타입에서 0x00은 NPK 서버, 0x01은 PK서버 그룹에 할당됨.

서버 상태: 이걸 0x00으로 하니 디아크리노가, 0x01로 하니 아인소프가 나왔다.
즉, PK 서버중 몇번째 껄로 표시하려면 0x01, NPK중 몇번째껄로 하려면 0x00임.



1. 파일 헤더:

1바이트: 서버 개수 (firstByte = Decoder::Decode1())

2. 각 서버 엔트리 (서버 개수만큼 반복):

1바이트: 서버 타입/ID (Decoder::Decode1())
0x01 : pk서버 그룹

4바이트: 서버 IP 주소 (Decoder::Decode4())
?InitializeNetworkScanner와 SendPing에서 확인가능하다고함.

2바이트: 서버 포트 번호 (Decoder::Decode2())
?InitializeNetworkScanner와 SendPing에서 확인가능하다고함.

1바이트: 추가 플래그/상태 (Decoder::Decode1())
UI그룹(0x01 => pk서버 UI에서 선택됨)

문자열 1: 서버 이름 (DecodeString1, 최대 255자)
04 C4 CE 74 C7 24 B1 78 C7
("케이네인")=> 이거는 아직 확인이 안됨

문자열 2: 서버 주소/IP (DecodeString1, 최대 255자)
=>유니코드가 맞으며 우측상단 서버 설명 부분에 한글로 표시되는 영역(=UTF-16LE로 인코딩)
=>원래는 PK 서버 입니다 등의 설명이 나옴
06 4C D1 A4 C2 B8 D2 20 00 1C C1 84 BC
("테스트 서버")

문자열 3: 서버 설명 (DecodeString1, 최대 255자)
04 C4 CE 74 C7 24 B1 78 C7
("케이네인")=> 우측상단 서버 설명 부분 위쪽에 출력됨을 확인함(원래는 오픈일자)

문자열 4: 확장 정보 (DecodeString2, 최대 65535자)
???


----
MainMenuPane::HandleButtonEvent?에서 서버 선택 버튼이나 오케이 버튼등의 이벤트핸들링을 하는듯


포맷 문자열: "%s%s_%02d.dat"
매개변수들:

첫 번째 %s: 게임 실행 경로 (GetApplicationPath_ 결과)
두 번째 %s: 서버 관련 접두사 (아마도 "Server" 또는 "Character")
%02d: 서버 ID 번호 (2자리 숫자, 예: 01, 02, 03...)


Config::Config 설정 정보 읽기 과정
1. 기본 설정 초기화 (Config::InitConfig_)
cpp// 기본값 설정
param_1[0x85] = 0;         // 폰트 설정
param_1[0x86] = 1;         // 전체화면 모드 (기본값: 1=전체화면)
param_1[2] = languageType; // 언어 설정




게임 진입 후 필요한 주요 데이터들
InitializeGameWorld_ 분석 결과, 다음과 같은 데이터들이 필요합니다:
1. 캐릭터 정보 관련

캐릭터 기본 정보: 이름, 레벨, 클래스, HP/MP
캐릭터 위치: 맵 ID, X/Y 좌표
캐릭터 외형: 모델, 장비 외형

2. 인벤토리 및 장비

인벤토리 아이템들
착용 장비 정보
퀵슬롯 설정

3. 스킬 및 마법

보유 스킬 목록 (SkillDialog 관련)
보유 마법 목록 (SpellDialog 관련)
링 스킬 (RingSkillDialog 관련)

4. UI 상태 데이터
코드에서 DAT_00626de0을 참조하여 다음 UI 상태들을 복원:

LeftSelectDialog 상태 (0xa4 오프셋)
RightSelectDialog 상태 (0xa8 오프셋)
SpellDialog 상태 (0xac 오프셋)
SkillDialog 상태 (0xb0 오프셋)
MakeDialog 상태 (0xb4 오프셋)

5. 맵 및 월드 정보

현재 맵 데이터
미니맵 정보
주변 오브젝트들

누락된 데이터 확인 방법

로그 확인: 게임 실행 중 어떤 패킷을 요청하는지 확인
네트워크 모니터링: 서버로 어떤 요청을 보내는지 확인
UI 상태 확인: 어떤 다이얼로그가 제대로 로드되지 않는지 확인

임시 해결 방법
필요한 데이터를 서버에서 받을 때까지, 기본값들로 초기화:
c// DAT_00626de0 포인터에 기본 데이터 설정
if (DAT_00626de0 != 0) {
    *(int*)(DAT_00626de0 + 0xa4) = 기본값;  // LeftSelect
    *(int*)(DAT_00626de0 + 0xa8) = 기본값;  // RightSelect  
    *(int*)(DAT_00626de0 + 0xac) = 기본값;  // Spell
    *(int*)(DAT_00626de0 + 0xb0) = 기본값;  // Skill
    *(int*)(DAT_00626de0 + 0xb4) = 기본값;  // Make
} 

패킷 전송 순서 (추천)
서버에서 이 순서대로 패킷을 전송하는 것이 좋습니다:
1. SStatusPacket (캐릭터 상태)
2. SMapStatusPacket (맵 정보)  
3. SDrawObjectsPacket (오브젝트들)
4. 인벤토리 관련 패킷들
5. UI 상태 패킷들
최소 필수 패킷들
화면이 나오지 않는 문제를 해결하기 위한 최소 필수 패킷들:

SStatusPacket - 캐릭터 HP/MP 바 표시
SMapStatusPacket - 맵 로딩
SDrawObjectsPacket - 캐릭터 자신 그리기

이 3개 패킷만 제대로 보내줘도 기본적인 게임 화면이 나타날 것입니다.
서버 코드에서 로그인 성공 응답 후 이 패킷들을 순차적으로 전송하도록 구현하면 됩니다.



#서버에서 02 준다음 03 줘야하고 패킷 가장 뒷부분에는 해당 아이디 정보를 보내줘야함(케릭명일듯) 
=> 클라에서 12주고 서버 전환후 클라이서 10을 주면 

---------------------------
실제 추정 중
ProcessMapSize에서 맵 정보를 주소 ProcessMapcrc에서 패킷 검증할 것으로 보임.



추정 패킷 스트림 구조
순서크기디코딩 함수저장 위치추정 의미
1short (2바이트)Decode2+0x18맵 ID
2short (2바이트)Decode2사용안함예약/패딩
3short (2바이트)Decode2사용안함예약/패딩
4byte (1바이트)Decode1비트플래그 처리맵 설정 플래그
5byte (1바이트)Decode1+0x28맵 모드/타입
6byte (1바이트)Decode1+0x1a추가 설정
7가변길이 문자열DecodeStringFromDBCS1+0x4맵 이름/설명
비트 플래그 분석 (4번째 바이트)
4번째 바이트는 다음과 같이 비트별로 처리됩니다:

비트 1 (>> 1 & 1): field12_0x1c - 맵 특성 플래그 1
비트 2 (~uVar1 & 4) >> 2): field13_0x20 - 맵 특성 플래그 2 (반전)
비트 3 (>> 3 & 1): field14_0x24 - 맵 특성 플래그 3

ProcessMapSize에서의 사용
ProcessMapSize 함수에서 확인했던 오프셋들과 매핑:
cpp// ProcessMapSize에서 읽던 값들
*(short *)(param_1 + 0x24) = field9_0x18;     // 맵 ID
*(byte *)(param_1 + 0x26) = field_0x1a;       // 추가 설정
*(dword *)(param_1 + 0x2c) = ???;             // 계산된 값?
*(byte *)(param_1 + 0x34) = field_0x28;       // 맵 모드/타입
최종 추정 패킷 스트림
오프셋 0x00-0x07: 패킷 헤더 (타입, 크기 등)
오프셋 0x08-0x09: 맵 ID (short)
오프셋 0x0A-0x0B: 예약 필드 1 (short)  
오프셋 0x0C-0x0D: 예약 필드 2 (short)
오프셋 0x0E:      맵 설정 플래그 (byte)
                  - 비트 1: 특성 플래그 1
                  - 비트 2: 특성 플래그 2
                  - 비트 3: 특성 플래그 3
오프셋 0x0F:      맵 모드/타입 (byte)
오프셋 0x10:      추가 설정 (byte)
오프셋 0x11-??:   맵 이름/설명 문자열 (가변길이, 최대 255자)
의미 추정

맵 ID: 로드할 맵 파일 번호 ("%03d.map")
맵 설정 플래그: PvP 여부, 특수 규칙, 날씨 등의 비트 플래그
맵 모드/타입: 던전, 필드, 길드전 등의 맵 타입
추가 설정: 시간대, 난이도 등의 추가 설정
맵 이름/설명: 클라이언트에 표시할 맵 이름이나 설명
(sample : 4C D1 A4 C2 B8 D2 F5 B9)


이 구조는 ProcessMapSize에서 +0x2c 위치에 저장되던 dword 값이 실제로는 이런 여러 설정들을 조합한 계산된 값일 가능성이 높다는 것을 보여줍니다.
aa 00 11
15 
00 01
00 00
00
00
00
04 4C D1 A4 C2 B8 D2 F5 B9

aa 00 11 15 00 01 00 00 00 00 00 04 4C D1 A4 C2 B8 D2 F5 B9
