1.Packet의 기본 구조는 다음과 같다.
예시 ) aa[스타트] 00 09[길이] 00[타입] 0b 23 41 4b 4c 22 c0 3c[암호화되거나 암호화 되지 않은 데이터]

2.클라이언트 > 서버 패킷 종류 및 타입
CVersionPacket	0x00
CNewUserPacket	0x02
CLoginPacket	0x03
CNewUserInfoPacket	0x04
CGetPacket	0x07
CDropPacket	0x08
CUserInfoPacket	0x0a
CQuitPacket	0x0b
CPutRequestPacket	0x0c
CStashPacket	0x0d
CSayPacket	0x0e
CMetaDataPacket	0x0f
CTransferServerPacket	0x10
CChangeDirPacket	0x11
CAttackPacket	0x13
CPassivePacket	0x14
CCancelNewUserPacket	0x15
CGuidePacket	0x16
CTradePacket	0x17
CUserListPacket	0x18
CActionRequisitePacket	0x1A
CToggleStatusPacket	0x1b
CUsePacket	0x1C
CWearPacket	0x1e
CTakeOffPacket	0x1f
CRepairPacket	0x22
CIdentifyPacket	0x23
CGuildPacket	0x24
CChangePasswordPacket	0x26
CResurrectPacket	0x2b
CSelfLookPacket	0x2d
CGroupPacket	0x2e
CChangeSlotPacket	0x30
CSitPacket	0x32
CMovePacket	0x33
CFriendsInfoPacket	0x34
CMapCRCPacket	0x35
CRefreshPacket	0x38
CMapChangedPacket	0x39
CPursuitPacket	0x3a
CFieldMapPacket	0x3f
CExceptionPacket	0x42
CobjectInfoRequestPacket	0x43
CReplyCRCPacket	0x45
CAddAbilityPacket	0x47
CExchangePacket	0x4A
CStipulationPacket	0x4b
CStartCastSpellPacket	0x4D
CPortraitPacket	0x4f
CMovePathPacket	0x54
CCastSpellPacket	0x56
CMultiServerPacket	0x57
CScriptPacket	0x6C
CUseActionPacket	0x65
CBrowserPacket	0x68
CWebBoardPacket	0x72
CCheckTimePacket	0x75



3.서버 > 클라이언트 패킷 종류 및 타입
SVersionCheckPacket	0x00
SCheckPacket	0x02
STransferServerPacket	0x03
SUserPositionPacket	0x04
SUserAppearancePacket	0x05
SMoveHumanAckPacket	0x06
SDrawObjectsPacket	0x07
SStatusPacket	0x08
SMessagePacket	0x0A
SMovePacket	0x0B
SMoveObjectPacket	0x0C
SSayPacket	0x0D
SRemoveObjectsPacket	0x0E
SAddInventoryPacket	0x0F
SRemoveInventoryPacket	0x10
SChangeDirectionPacket	0x11
SUseActionEndPacket	0x12
SDamageEffectPacket	0x13
SMapCRCPacket	0x14
SMapSizePacket	0x15
SFriendsInfoPacket	0x17
SMetaDataPacket	0x18
SPlaySoundPacket	0x19
SMotionPacket	0x1A
SChangeWeatherPacket	0x1F
SChangeHourPacket	0x20
SAddLastingSpellPacket	0x2C
SRemoveLastingSpellPacket	0x2D
SFieldMapPacket	0x2E
SMerchantPacket	0x2F
SPursuitPacket	0x30
SPutHumanObjectPacket	0x33
SObjectInfoReplyPacket	0x34
SUserListPacket	0x36
SAddEquipmentPacket	0x37
SRemoveEquipmentPacket	0x38
SSelfLookPacket	0x39
SUpdateGroupMembersPacket	0x3A
SRequestCRCPacket	0x3B
SCancelCastSpellPacket	0x48
SPortraitPacket	0x49
SBadGuyPacket	0x4A
SBouncePacket	0x4B
SAddUserPacket	0x44
SScriptPacket	0x44
SCastSpellPacket	0x52
SBlockClientPacket	0x51
SMultiServerPacket	0x56
SStipulationPacket	0x60
SWebBoardPacket	0x61
SAddActionPacket	0x62
SRemoveActionPacket	0x63
SMovePathPacket	0x64
SCheckTimePacket	0x66
SBrowserPacket	0x68
SStashPacket	0x6B
SPassivePacket	0x6D
STradePacket	0x6E
SActionRequisitePacket	0x6F
SGuildPacket	0x70



4. 실제 클라이언트 패킷 예시(0.59 클라이언트)
aa (시작)
0005(데이터 바이트 수)
00(타입 : 버전정보)
00(메이저 버전 0)
3b(마이너 버전 59)
41(아스키 A - 유효)
4b(아스키 K - korea) =>  'E'(0x45), 'J'(0x4A), 또는 'K'(0x4B)


5. 실제 서버 패킷 추정 예시
aa(시작)
0014(데이터 바이트 수)
00(타입 : 버전정보)
00003b414b010c (???)
3139322e3136382e302e3135 (= 192.168.0.15 => server ip)
