=============================================
<기본적인 흐름>
1. 애플리케이션 초기화 단계

WinMainCRTStartup: C 런타임 시작점

Windows 버전 정보 획득
애플리케이션 초기화 함수들 호출
WinMain 함수 호출



2. 메인 애플리케이션 시작 (WinMain)

Application 객체 생성 및 초기화
게임 모듈 초기화 (InitializeGameModules)
MFGS 업데이터 초기화
메인 윈도우 생성 및 표시
메인 루프 진입 (MainLoopMaybe_FUN_004158b0)

3. 메인 루프에서의 이벤트 처리
MainLoopMaybe_FUN_004158b0에서:

Windows 메시지 대기 및 처리
PaneMan_ProcessEvents_Maybe_FUN_004cf5a0 호출로 이벤트 처리

4. 이벤트 처리 시스템
PaneMan_ProcessEvents_Maybe_FUN_004cf5a0에서:

타이머 기반 이벤트 처리
네트워크 상태 확인
ProcessEventHandler_Maybe_FUN_004cd850 호출로 각 이벤트 핸들러 실행

5. 패킷 송신 처리
송신 경로:

SendPacket_Maybe → 메모리 할당 후 Thread::AddMessage로 큐에 추가
SendCPacket → CPacket 전용 송신 함수
ProcessSendPacketMessage → 실제 패킷 송신 처리

암호화 처리 (EncryptPacket)
TCP/IP는 직접 send() 호출
HTTP는 Base64 인코딩 후 전송



6. 패킷 수신 처리
수신 경로:

HandleIncomingTCPIPPacket → TCP/IP 패킷 수신 메인 함수

recv() 함수로 소켓에서 데이터 수신
패킷 헤더 파싱 (0xAA 시작 바이트 확인)
패킷 길이 정보 추출(2바이트)
패킷 완전성 확인



7. 패킷 디코딩 및 처리

DecryptPacket: 패킷 복호화(필요한 경우)
PacketFactory::CreateSPacketFromCode: 패킷 타입별 객체 생성
SPacket::Decode: 패킷 데이터 디코딩(각 패킷 클래스별 DoDecoding이있음 > 패킷을 객체화 시킴)
UNIPostMessage: Windows 메시지로 메인 윈도우에 전달 (메시지 ID: 0x404)

8. 패킷 타입별 처리
메인 윈도우에서 0x404 메시지를 받으면 패킷 타입에 따라:

버전 체크 패킷
사용자 위치 패킷
액션 패킷
스크립트 패킷
메시지 패킷 등
(패킷 명세 부분 참고할것)
=============================================

<로그인 화면까지의 절차>

# 게임 시작부터 로그인 화면까지의 절차 분석

## 1. 애플리케이션 초기화 단계

### _WinMainCRTStartup
- C 런타임 라이브러리 초기화
- Windows 버전 정보 획득 (`GetVersion()`)
- 기본 초기화 함수들 호출
- _WinMain@16 호출

## 2. 메인 애플리케이션 시작 단계

### _WinMain@16
- Application 객체 생성 및 초기화
- 게임 모듈 초기화 (`InitializeGameModules()`)
- MFGS 업데이터 초기화 (`InitializeMFGSUpdater()`)
  - 다운로드 서버: `download.nexon.co.kr/elancia/mfg`
  - 계정: `anonymous`
  - 서버: `esteam.nexon.co.kr`
- 메인 윈도우 생성 및 배치
- 메인 루프 진입 (`MainLoopMaybe_FUN_004158b0`)

## 3. 클라이언트 버전 정보 획득

### GetVersionNo_Maybe
- 실행 파일의 버전 정보 추출
  - `GetModuleFileNameA()`: 현재 실행 파일 경로 획득
  - `GetFileVersionInfo()`: 파일 버전 정보 읽기
  - `VerQueryValue()`: 버전 값 추출
- 기본값: 버전 1 (정보 획득 실패 시)

## 4. 서버 연결 초기화

### ToConnectedStateMaybe___
- 소켓 초기화 및 설정
  - `DoGetRawBytes_Maybe___FUN_0051b650()`: Raw 바이트 모드 비활성화
  - `FUN_0051b550()`: 연결 모드 설정 (HTTP/TCP 선택)
  - `Thread::FlushMessageQueue()`: 메시지 큐 초기화

- 초기 패킷 전송 ("baram")
  - `FormatStringToPacket_FUN_0058c44f()`: "baram" 문자열을 패킷으로 포맷
  - `Socket::SendPacket_Maybe()`: 서버로 초기 신호 전송

## 5. 버전 체크 패킷 전송

### CVersionPacket 생성 및 전송
- 버전 패킷 생성
  - 클라이언트 버전 번호 설정
  - 언어 코드 설정 ('A': 기본, 'E': 영어, 'J': 일본어, 'K': 한국어)
  - `CPacket::Send()`: 서버로 전송

## 6. 서버 응답 처리

### ProcessVersionCheckPacket
서버로부터 받은 버전 체크 응답을 처리하며, 3가지 경우로 분기:

#### Case 0: 버전 일치 (정상)
- 서버 접속 허용
- 스크립트 패킷 요청 (`CScriptPacket` 전송) > 이후 서버의 응답 패킷이 들어와야 됨
- 메타데이터 패킷 요청 (`CMetaDataPacket` 전송) > 이후 서버의 패킷이 들어와야 됨.

#### Case 1: 버전 불일치 (업데이트 필요)
- SVersionCheckPacket 생성
- 파일 목록 정보 복사
- 업데이트 다이얼로그 표시
- 사용자가 업데이트를 선택할 수 있는 UI 제공

#### Case 2: 기타 오류
- 오류 처리
- 적절한 에러 메시지 표시


## 7. 메타데이터 및 서버 목록 처리
### 서버에서 응답 수신 및 서버 정보 수신
- SScriptPacket응답 : 첫 바이트가 0으로 들어와야 정상적으로 UI초기화 절차가 진행되며 로그인 화면으로 넘어갈 수 있다.
- SMetaDataPacket 응답옴 : Server.dat파일의 내용이 오며 해당 파일이 없으면 저장, 있으면 기존에 있는 정보와 비교하여 업데이트 함.(비교시 체크섬 사용)

참고 : SMetaDataPacket에서 주는 내용은 단순한 화면 표출용 내용이고 실제 사용하는 것은 인덱스 값 뿐이며 뒷 부분은 그냥 글자로 표현해주는 것이 다임.



# SMetaDataPacket 수신 시 Server.dat 파일 생성 과정 상세 분석

## 1. 파일 생성 트리거 지점

### ProcessMetaDataPacket에서 Server.dat 파일 생성


// 개별 서버 메타데이터 수신 시 (타입 1)
else if (*(char *)(param_1 + 9) == '\x01') {
    // 서버 메타데이터를 파일에 저장
    SaveMetaDataFile(psVar1);  // 이 함수가 Server.dat 생성!
    
    // 서버 정보를 메모리 컨테이너에 추가
    FUN_004ab0a0(param_1, psVar1);
    AddServerToMetaData(this_00, (int)param_1);
    
    // 대기 중인 메타데이터 카운터 감소
    *(char *)((int)this + 0x26c) -= 1;
}


각 서버의 SMetaDataPacket(타입 1)을 받을 때마다 Server.dat 파일이 업데이트됩니다.

## 2. SaveMetaDataFile 함수 - 파일 생성 과정

### 파일 경로 결정

// 1. 애플리케이션 실행 경로 획득
FUN_00415d50(DAT_0060d17c);  // GetModuleFileName 등으로 실행 경로 획득

// 2. temp 디렉토리 경로 생성
_swprintf(local_618, u__s_temp_0060179c);  // "%s\temp" 포맷
(*UNICreateDirectory_DAT_00612798)();      // temp 디렉토리 생성

// 3. Server.dat 파일 경로 생성  
_swprintf(auStack_214, u__s__s_005fce24);  // "%s\%s" 포맷으로 전체 경로
// 결과: "[실행경로]\temp\Server.dat"


### 서버 데이터 직렬화

// SerializeServerMetaData 호출
SerializeServerMetaData(DAT_0060d180, param_1, 0);


## 3. SerializeServerMetaData - 데이터 직렬화 과정

### 서버 정보 처리

if (param_2 == 0) {  // 새 서버 추가 모드
    // 1. 서버 이름을 키로 사용
    FUN_00588a28((short *)local_404, param_1, 0xff);
    
    // 2. 서버 컨테이너에서 해당 서버 검색/추가
    FUN_004ad200(piVar6, (int *)&local_410, local_404);
    
    // 3. 임시 파일명 생성 (랜덤)
    _rand();
    _swprintf(puVar4, u_temp_u_00601814);  // "temp%u" 포맷
    
    // 4. 서버 정보를 컨테이너에 삽입
    FUN_004ad030(piVar6, local_40c, local_404);
}


### 이진 트리 구조로 서버 관리

// 서버들을 이진 검색 트리로 관리
bVar3 = true;
pcVar1 = (char *)*piVar6;           // 트리 루트
pcVar2 = *(char )((char *)*piVar6 + 4);  // 현재 노드

while (pcVar2 != (char *)0x0) {
    // 서버 이름으로 비교하여 트리 탐색
    bVar3 = FUN_0055a490(local_404, (ushort *)(pcVar2 + 0x10));
    pcVar1 = pcVar2;
    if (bVar3) {
        pcVar2 = *(char )(pcVar2 + 8);   // 왼쪽 자식
    } else {
        pcVar2 = *(char )(pcVar2 + 0xc); // 오른쪽 자식  
    }
}


## 4. 실제 파일 쓰기 과정

### 파일 생성 및 쓰기

// 1. 파일 핸들 생성
hFile = (HANDLE)(*DAT_0061276c)(auStack_214, 0xc0000000, 0);
// auStack_214 = "[실행경로]\temp\Server.dat"
// 0xc0000000 = GENERIC_READ | GENERIC_WRITE

// 2. 직렬화된 데이터 쓰기
if (hFile != (HANDLE)0xffffffff) {
    WriteFile(hFile, pvStack_1c, DStack_18, (LPDWORD)&stack0xfffff7c0, (LPOVERLAPPED)0x0);
}

// 3. 메모리 정리 및 파일 닫기
if (pvStack_1c != (LPCVOID)0x0) {
    MemoryMan::FreePtr((int)pvStack_1c);
}
if (hFile != (HANDLE)0xffffffff) {
    CloseHandle(hFile);
}


## 5. 전체 Server.dat 파일 저장 과정

### SaveServerDataToFile - 압축 및 암호화된 저장


// 1. 인코더 초기화
Encoder::Encoder(local_230);
Encoder::StartEncoding((Encoder *)&stack0xfffffdb4, pbVar2, 0x100000);

// 2. 전체 서버 컨테이너 데이터 인코딩
Encoder::Encode2((Encoder *)&stack0xfffffdb4, *(undefined4 *)(param_1 + 0x14));

// 3. 각 서버별 정보 인코딩
while (iVar5 != iVar4) {  // 모든 서버 순회
    // 서버 이름 인코딩
    Encoder::EncodeStringToDBCS1((Encoder *)&stack0xfffffdb4, (LPCWSTR)(iVar5 + 0x10), 0xff);
    
    // 서버 추가 정보 인코딩  
    Encoder::EncodeStringToDBCS1((Encoder *)&stack0xfffffdb4, *(LPCWSTR *)(iVar5 + 0x210), 0xff);
    
    // 다음 서버로 이동 (트리 순회)
    // ... 이진 트리 순회 로직
}

// 4. 인코딩 완료 및 압축
iVar4 = Encoder::EndEncoding((Encoder *)&stack0xfffffdb4, (undefined4 *)&stack0xfffffda8);

// 5. CRC32 체크섬 계산
uStack_250 = CalculateCRC32(0, pbVar2, uVar6);

// 6. 데이터 압축
FUN_0055f620(lpBuffer, &DStack_264, (int)pbVar2, uVar6);

// 7. 최종 파일 쓰기
WriteFile(pvStack_260, &uStack_250, 4, ...);        // CRC32 먼저 쓰기
WriteFile(hFile, lpBuffer, DStack_264, ...);         // 압축된 데이터 쓰기


## 6. Server.dat 파일 구조

### 파일 포맷

[4바이트: CRC32 체크섬]
[압축된 서버 데이터]


### 압축된 데이터 내용
1. 서버 개수 (인코딩됨)
2. 각 서버별 정보 (DBCS 문자열로 인코딩):
   - 서버 이름
   - 서버 상세 정보 (IP, 포트, 상태 등)
   - 기타 메타데이터

## 7. 파일 생성 시점과 순서

### 타이밍

1. CScriptPacket + CMetaDataPacket 전송
            ↓
2. SScriptPacket 수신 → UI 초기화
            ↓  
3. SMetaDataPacket(타입 0) 수신 → 서버 목록 획득
            ↓
4. 각 서버별 CMetaDataPacket(타입 2) 요청
            ↓
5. 각 SMetaDataPacket(타입 1) 수신 → 각각 SaveMetaDataFile() 호출
   └─ Server.dat 파일이 서버 개수만큼 업데이트됨
            ↓
6. 모든 서버 정보 수집 완료 → SaveServerDataToFile() 호출  
   └─ 최종 완전한 Server.dat 파일 생성
            ↓
7. ActivateMainMenuPane() → 로그인 화면 표시


## 8. 핵심 특징

### 증분 업데이트
- 각 서버의 메타데이터를 받을 때마다 파일 업데이트
- 이진 트리 구조로 효율적인 서버 관리
- 중복 서버는 자동으로 병합

### 데이터 무결성
- CRC32 체크섬으로 파일 무결성 검증
- 압축을 통한 파일 크기 최적화
- 인코딩을 통한 데이터 보호

### 캐시 시스템
- 다음 실행 시 LoadMetaDataFromFile()로 빠른 로딩
- 체크섬 비교로 최신 여부 확인
- 필요시에만 서버에서 새 데이터 요청

결론: SMetaDataPacket(타입 1)을 받을 때마다 Server.dat 파일이 점진적으로 업데이트되며, 모든 서버 정보 수집 완료 후 최종적으로 완전한 Server.dat 파일이 생성됩니다.


### 서버 목록 수신 후:
- ExtractServerIndices(): 서버 인덱스 추출
- GetServerByIndex(): 개별 서버 정보 획득
- UpdateServerList(): UI의 서버 목록 업데이트
- ActivateMainMenuPane(): 메인 메뉴 활성화

## 8. 메인 메뉴 UI 초기화

### InitializeMainMenuUI
- 네트워크 관련 초기화
  - 타임아웃 설정 (5000ms)
  - 소켓 버퍼 설정
- UI 컴포넌트 생성
  - UserProfile 객체 생성
  - Status 객체 생성
  - 각종 다이얼로그 패널 생성 (30개 이상)
- UI 레이아웃 배치
  - 서버 선택 목록
  - 로그인 입력 필드
  - 각종 버튼들

## 9. 로그인 검증 시스템

### LoginValidation
웹 기반 계정 인증 시스템:

#### HTTP 요청 처리
- InternetOpen(): 인터넷 연결 초기화
- InternetOpenUrl(): 인증 서버로 HTTP 요청
- InternetReadFile(): 서버 응답 읽기

#### 응답 처리
- "1" 응답: 로그인 성공
- "ID_not_exist": 존재하지 않는 계정
- "wrong_password": 잘못된 비밀번호
- 기타: 네트워크 오류 또는 서버 오류

### LoginValidationCallback
- 로그인 결과에 따른 UI 상태 업데이트
- 성공 시 게임 서버 연결 준비
- 실패 시 적절한 오류 메시지 표시

## 10. 최종 상태

### 로그인 화면 완성
- 서버 목록 표시: 사용 가능한 게임 서버들
- 계정 입력 필드: ID/Password 입력란
- 로그인 버튼: 웹 인증 시작
- 기타 UI 요소: 설정, 종료 등의 버튼들

## 핵심 특징

### 보안 측면
- 이중 인증: 웹 서버를 통한 계정 인증 + 게임 서버 접속
- 버전 체크: 클라이언트 무결성 검증
- 패킷 암호화: 네트워크 통신 보안

### 네트워크 구조
- 웹 서버: 계정 인증 및 업데이트 정보
- 게임 서버: 실제 게임 데이터 통신
- 다운로드 서버: 클라이언트 업데이트 파일

### 다국어 지원
- 언어별 버전 코드 구분 (A/E/J/K)












========================
그 이후 처리
# 실제 게임 서버 접속 후 흐름 분석

## 전체 흐름 개요

```
1. 게임 서버 소켓 연결
   ↓
2. 초기 핸드셰이크 (프로토콜 설정)
   ↓  
3. 로그인 인증 (ID/Password)
   ↓
4. 캐릭터 선택/생성
   ↓
5. 게임 월드 입장 (맵 로딩)
   ↓
6. 실시간 게임 플레이
```

## 1. 게임 서버 소켓 연결

### ProcessTransferServerMessage - 소켓 재연결:
```c
// 1. 기존 로그인 서버 연결 종료
closesocket(loginServerSocket);
WSACleanup();

// 2. 실제 게임 서버로 새 소켓 연결  
OpenTCPIPSocket(this, realServerIP, realServerPort);
Sleep(1000); // 연결 안정화 대기
```

## 2. 초기 핸드셰이크

### HandleIncomingTCPIPPacket - 프로토콜 협상:
```c
// 패킷 헤더 파싱
if ((char)local_4 == -0x56) { // 0xAA (패킷 시작 바이트)
    *(undefined4 *)((int)param_1 + 0xc098) = 1; // 패킷 수신 모드
    *(undefined4 *)((int)param_1 + 0xc09c) = 0;  // 위치 초기화
    *(undefined4 *)((int)param_1 + 0xc0a0) = 0;  // 길이 초기화
}

// 패킷 길이 읽기 (2바이트)
*(uint *)((int)param_1 + 0xc0a0) = 
    *(uint *)((int)param_1 + 0xc0a0) | (local_4 & 0xff) << 8; // 상위 바이트
*(uint *)((int)param_1 + 0xc0a0) = 
    *(uint *)((int)param_1 + 0xc0a0) | local_4 & 0xff;        // 하위 바이트

// 패킷 데이터 수신 완료 시 처리
if (iVar1 + -1 == *(int *)((int)param_1 + 0xc0a0)) {
    // 패킷 복호화
    iVar1 = DecryptPacket((Socket *)param_1, pbVar5, iVar1, 
                          (byte *)((int)param_1 + 0xc0a8));
    
    // 패킷 객체 생성
    pSVar3 = (SPacket *)PacketFactory::CreateSPacketFromCode(DAT_0060d190, (uint)*pbVar5);
    
    // 패킷 디코딩
    iVar1 = SPacket::Decode(pSVar3, pbVar5, iVar1);
    
    // 메인 윈도우로 패킷 전달 (메시지 0x404)
    (*UNIPostMessage)(mainWindow, 0x404, pSVar3, 0);
}
```

## 3. 패킷 처리 시스템

### Message_0x404_FUN_004508c0 - 패킷 이벤트 처리:
```c
void Message_0x404_FUN_004508c0(SPacket* sPacket) {
    // 이벤트 시스템으로 패킷 전달
    EventMan::ProcessNotifySPacketFromSocketMessage(sPacket);
}
```

### ProcessNotifySPacketFromSocketMessage - 이벤트 생성:
```c
// 패킷을 이벤트로 변환
Event event;
event.field4_0x4 = 0x19;      // 패킷 이벤트 타입
event.spacket = sPacket;       // 패킷 데이터

// 패널 매니저로 이벤트 전달
PaneMan::PostEvent(DAT_0060d0ac, &event);
```

## 4. 로그인 인증 과정

### 4-1. CBrowserPacket 전송:
```c
// InitializeGameChannelPane에서 채널 정보 요청
puVar4 = CBrowserPacket::__CreateInstance_(puVar4);
*(undefined1 *)(puVar4 + 9) = 1; // 브라우저 패킷 타입
CPacket::Send(puVar4);
```

### 4-2. CLoginPacket 전송:
```c
// 사용자가 ID/Password 입력 후
puVar9 = CLoginPacket::__CreateInstance(puVar7);
GetTextFromField(idField, userID);      // ID 추출
GetTextFromField(pwField, password);    // Password 추출
CPacket::Send(puVar9);                  // 로그인 패킷 전송
```

## 5. 주요 수신 패킷 타입들

### 게임 서버에서 받는 주요 SPacket들:

#### 5-1. 맵 관련 패킷:
- **SMapCRCPacket**: 맵 무결성 검증
- **SMapSizePacket**: 맵 크기 정보
- **SMapStatusPacket**: 맵 상태 정보
- **SFieldMapPacket**: 필드 맵 데이터

#### 5-2. 오브젝트 관련 패킷:
- **SDrawObjectsPacket**: 화면에 그려질 오브젝트들
- **SRemoveObjectsPacket**: 제거될 오브젝트들
- **SDieObjectsPacket**: 죽은 오브젝트들
- **SPutHumanObjectPacket**: 플레이어 캐릭터 배치

#### 5-3. 플레이어 관련 패킷:
- **SUserPositionPacket**: 플레이어 위치 정보
- **SUserAppearancePacket**: 플레이어 외형 정보
- **SUserListPacket**: 접속 중인 사용자 목록
- **SStatusPacket**: 플레이어 상태 (HP, MP 등)

#### 5-4. 게임 시스템 패킷:
- **SUpdateGroupMembersPacket**: 파티원 정보 업데이트
- **SPlaySoundPacket**: 효과음 재생
- **SEffectPacket**: 이펙트 표시
- **SMotionPacket**: 모션/애니메이션 재생

## 6. 게임 인터페이스 초기화

### InitializeGameChannelPane - 게임 UI 설정:
```c
// 게임 채널 패널 초기화
FUN_00439c50(param_1); // 기본 패널 초기화

// UI 요소들 설정
GetUIElement(param_1, 5);  // 채널 정보
GetUIElement(param_1, 6);  // 서버 상태
GetUIElement(param_1, 7);  // 접속자 수
GetUIElement(param_1, 8);  // 채널 선택
GetUIElement(param_1, 9);  // 캐릭터 정보

// 게임 화면 전환 준비
FUN_00515810(DAT_0060d0d0, 1, param_1, callback, NULL, 0, 0);
```

## 7. 실시간 게임 루프

### 7-1. 패킷 수신 → 처리 사이클:
```
recv() → HandleIncomingTCPIPPacket() → PacketFactory::CreateSPacketFromCode()
   ↓
SPacket::Decode() → UNIPostMessage(0x404) → EventMan::ProcessNotifySPacketFromSocketMessage()
   ↓
PaneMan::PostEvent() → 해당 패널의 이벤트 핸들러 → 게임 상태 업데이트
```

### 7-2. 주요 게임 루프 컴포넌트:
- **패킷 수신**: 지속적인 네트워크 데이터 수신
- **이벤트 처리**: 패킷을 게임 이벤트로 변환
- **게임 로직**: 캐릭터 이동, 전투, 아이템 등
- **렌더링**: 3D 그래픽 및 UI 업데이트
- **사용자 입력**: 키보드/마우스 처리

## 8. 데이터 동기화

### 8-1. 클라이언트 → 서버:
- **CMovePacket**: 캐릭터 이동
- **CAttackPacket**: 공격 액션
- **CUseActionPacket**: 스킬/아이템 사용
- **CSayPacket**: 채팅 메시지

### 8-2. 서버 → 클라이언트:
- **SMoveObjectPacket**: 다른 플레이어 이동
- **SDamageEffectPacket**: 데미지 이펙트
- **SChangeDirPacket**: 방향 변경
- **SSayPacket**: 채팅 메시지 수신

## 9. 세션 관리

### 9-1. 연결 유지:
```c
// 주기적인 하트비트 패킷 전송
CCheckTimePacket heartbeat;
CPacket::Send(&heartbeat);

// 서버 응답 확인
SCheckTimePacket response; // 서버에서 응답
```

### 9-2. 연결 끊김 처리:
```c
// 네트워크 오류 감지
if (recv() == -1) {
    WSAGetLastError(); // 오류 코드 확인
    // 재연결 시도 또는 로그인 화면으로 복귀
}
```

## 10. 게임 종료 및 정리

### 10-1. 정상 종료:
```c
// CQuitPacket 전송
CQuitPacket quitPacket;
CPacket::Send(&quitPacket);

// 소켓 정리
closesocket(gameServerSocket);
WSACleanup();
```

### 10-2. 비정상 종료:
```c
// 연결 끊김 감지 시 자동 정리
// 임시 데이터 저장
// 로그인 화면으로 복귀
```

## 요약

게임 서버 접속 후의 흐름은 **지속적인 패킷 송수신을 통한 실시간 상태 동기화**가 핵심입니다:

1. **연결 설정** → 소켓 연결 및 프로토콜 협상
2. **인증** → 로그인 패킷으로 사용자 인증
3. **초기화** → 게임 UI 및 캐릭터 정보 로딩
4. **게임 루프** → 실시간 패킷 처리 및 게임 상태 업데이트
5. **세션 관리** → 연결 유지 및 오류 처리

이 모든 과정이 **이벤트 기반 아키텍처**로 구현되어 있어 안정적이고 확장 가능한 온라인 게임 시스템을 제공합니다.

--------
분석 결과, CBrowserPacket을 전송한 이후에 로그인 화면으로 진입하는 것이 맞습니다.
구체적인 흐름:

InitializeGameChannelPane 함수에서 CBrowserPacket을 생성하고 전송
패킷 전송 후 UI 초기화 및 로그인 관련 인터페이스 설정
LoginValidation 함수에서 실제 로그인 검증 수행
**MainMenuPane_HandleServerPackets**에서 서버 응답 처리

CBrowserPacket은 브라우저 관련 정보(아마도 클라이언트 정보, 세션 데이터 등)을 서버에 먼저 전송하여 클라이언트를 식별하고, 그 후에 로그인 절차가 시작되는 구조로 되어 있습니다.

