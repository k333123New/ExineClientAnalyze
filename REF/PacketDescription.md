1.Packet의 기본 구조는 다음과 같다.
예시 ) aa[스타트] 00 09[길이] [00[타입] 0b 23 41 4b 4c 22 c0 3c]->[암호화되거나 암호화 되지 않은 데이터]
=>클라이언트에서 서버로 보내는(CPacket) 패킷의 타입이 0x00, 0x10인 경우는 암호화를 하지 않고 (나머지는 타입을 포함해서 암호화 한다)
=>서버에서 클라이언트로 보내는(SPacket) 패킷의 타입이 0x00, 0x03인 경우에는 암호화 되어있지 않다.(나머지는 타입을 포함해서 암호화 되어있다)




2.클라이언트 > 서버 패킷 종류 및 타입
CVersionPacket	0x00 (암호화 안함)
CTransferServerPacket	0x10 (암호화 안함)

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
SVersionCheckPacket	0x00 (암호화 안함)
STransferServerPacket	0x03 (암호화 안함)

SCheckPacket	0x02
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

=================
Server.dat파일의 구조 추정중
[4바이트: CRC32 체크섬]
[압축된 데이터:
  [2바이트: 서버 개수]
  각 서버별로:
    [1바이트: 서버이름 길이][가변길이: 서버이름 DBCS 바이트들]
    [1바이트: 추가정보 길이][가변길이: 추가정보 DBCS 바이트들]
]
여기서 추가정보 부분은 실제로 파싱되는 부분이 없는 정보 표시용이라 아무거나 써도된다고함.



<서버 파일 불러오는 코드 추정>
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Text;

/// <summary>
/// Server.dat 파일 파서 클래스
/// </summary>
public class ServerDatParser
{
    /// <summary>
    /// 서버 정보 클래스
    /// </summary>
    public class ServerInfo
    {
        public byte ServerID { get; set; }
        public uint ServerStatus { get; set; }
        public ushort ServerPort { get; set; }
        public byte ServerType { get; set; }
        public string ServerName { get; set; } = "";
        public string AdditionalInfo { get; set; } = "";
        public string Description { get; set; } = "";
        public string ExtraData { get; set; } = "";

        public override string ToString()
        {
            return $"[{ServerID}] {ServerName} - {AdditionalInfo}";
        }
    }

    /// <summary>
    /// 파싱 결과 클래스
    /// </summary>
    public class ParseResult
    {
        public bool Success { get; set; }
        public string ErrorMessage { get; set; } = "";
        public uint CalculatedChecksum { get; set; }
        public uint FileChecksum { get; set; }
        public List<ServerInfo> Servers { get; set; } = new List<ServerInfo>();
        public int DecompressedSize { get; set; }
    }

    /// <summary>
    /// CRC32 계산 클래스
    /// </summary>
    private static class CRC32
    {
        private static readonly uint[] Table = new uint[256];

        static CRC32()
        {
            for (uint i = 0; i < 256; i++)
            {
                uint crc = i;
                for (int j = 0; j < 8; j++)
                {
                    if ((crc & 1) == 1)
                        crc = (crc >> 1) ^ 0xEDB88320;
                    else
                        crc >>= 1;
                }
                Table[i] = crc;
            }
        }

        public static uint Calculate(byte[] data)
        {
            uint crc = 0xFFFFFFFF;
            foreach (byte b in data)
            {
                crc = Table[(crc ^ b) & 0xFF] ^ (crc >> 8);
            }
            return ~crc;
        }
    }

    /// <summary>
    /// 바이너리 디코더 클래스
    /// </summary>
    private class BinaryDecoder
    {
        private readonly byte[] _buffer;
        private int _position;

        public BinaryDecoder(byte[] buffer)
        {
            _buffer = buffer;
            _position = 0;
        }

        public int Position => _position;
        public int Remaining => _buffer.Length - _position;

        public byte ReadByte()
        {
            if (_position >= _buffer.Length)
                throw new EndOfStreamException("디코더 버퍼 끝에 도달했습니다.");
            return _buffer[_position++];
        }

        public ushort ReadUInt16()
        {
            if (_position + 1 >= _buffer.Length)
                throw new EndOfStreamException("디코더 버퍼 끝에 도달했습니다.");
            
            ushort value = (ushort)(_buffer[_position] | (_buffer[_position + 1] << 8));
            _position += 2;
            return value;
        }

        public uint ReadUInt32()
        {
            if (_position + 3 >= _buffer.Length)
                throw new EndOfStreamException("디코더 버퍼 끝에 도달했습니다.");
            
            uint value = (uint)(_buffer[_position] | 
                               (_buffer[_position + 1] << 8) | 
                               (_buffer[_position + 2] << 16) | 
                               (_buffer[_position + 3] << 24));
            _position += 4;
            return value;
        }

        public string ReadDBCSString()
        {
            if (_position >= _buffer.Length)
                throw new EndOfStreamException("문자열 길이를 읽을 수 없습니다.");

            byte length = ReadByte();
            if (length == 0) return "";

            if (_position + length > _buffer.Length)
                throw new EndOfStreamException($"문자열 데이터가 부족합니다. 필요: {length}, 남은: {Remaining}");

            // DBCS (일반적으로 CP949/EUC-KR) 디코딩
            byte[] stringBytes = new byte[length];
            Array.Copy(_buffer, _position, stringBytes, 0, length);
            _position += length;

            try
            {
                // 한국어 인코딩 시도
                var encoding = Encoding.GetEncoding("ks_c_5601-1987"); // CP949
                return encoding.GetString(stringBytes).TrimEnd('\0');
            }
            catch
            {
                // 폴백: 기본 시스템 인코딩 사용
                return Encoding.Default.GetString(stringBytes).TrimEnd('\0');
            }
        }

        public string ReadUnicodeString()
        {
            if (_position + 1 >= _buffer.Length)
                throw new EndOfStreamException("유니코드 문자열 길이를 읽을 수 없습니다.");

            ushort length = ReadUInt16();
            if (length == 0) return "";

            if (_position + length > _buffer.Length)
                throw new EndOfStreamException($"유니코드 문자열 데이터가 부족합니다. 필요: {length}, 남은: {Remaining}");

            byte[] stringBytes = new byte[length];
            Array.Copy(_buffer, _position, stringBytes, 0, length);
            _position += length;

            return Encoding.Unicode.GetString(stringBytes).TrimEnd('\0');
        }
    }

    /// <summary>
    /// Server.dat 파일 파싱
    /// </summary>
    /// <param name="filePath">파일 경로</param>
    /// <returns>파싱 결과</returns>
    public static ParseResult ParseServerDat(string filePath)
    {
        var result = new ParseResult();

        try
        {
            if (!File.Exists(filePath))
            {
                result.ErrorMessage = $"파일을 찾을 수 없습니다: {filePath}";
                return result;
            }

            // 1. 파일 전체 읽기
            byte[] fileData = File.ReadAllBytes(filePath);
            
            if (fileData.Length < 4)
            {
                result.ErrorMessage = "파일이 너무 작습니다. 최소 4바이트(CRC32) 필요.";
                return result;
            }

            // 2. CRC32 체크섬 읽기
            result.FileChecksum = BitConverter.ToUInt32(fileData, 0);

            // 3. 압축된 데이터 추출
            byte[] compressedData = new byte[fileData.Length - 4];
            Array.Copy(fileData, 4, compressedData, 0, compressedData.Length);

            // 4. 데이터 압축 해제
            byte[] decompressedData = DecompressData(compressedData);
            result.DecompressedSize = decompressedData.Length;

            // 5. CRC32 검증
            result.CalculatedChecksum = CRC32.Calculate(decompressedData);
            if (result.CalculatedChecksum != result.FileChecksum)
            {
                result.ErrorMessage = $"CRC32 체크섬 불일치. 파일: 0x{result.FileChecksum:X8}, 계산: 0x{result.CalculatedChecksum:X8}";
                return result;
            }

            // 6. 서버 데이터 파싱
            result.Servers = ParseServerData(decompressedData);
            result.Success = true;

            return result;
        }
        catch (Exception ex)
        {
            result.ErrorMessage = $"파일 파싱 중 오류 발생: {ex.Message}";
            return result;
        }
    }

    /// <summary>
    /// 압축된 데이터 해제
    /// </summary>
    private static byte[] DecompressData(byte[] compressedData)
    {
        try
        {
            // zlib 압축 해제 시도
            using (var compressedStream = new MemoryStream(compressedData))
            using (var deflateStream = new DeflateStream(compressedStream, CompressionMode.Decompress))
            using (var decompressedStream = new MemoryStream())
            {
                // zlib 헤더 스킵 (첫 2바이트)
                compressedStream.ReadByte();
                compressedStream.ReadByte();
                
                deflateStream.CopyTo(decompressedStream);
                return decompressedStream.ToArray();
            }
        }
        catch
        {
            // zlib 실패 시 다른 압축 방식 시도 또는 비압축 데이터로 처리
            try
            {
                using (var compressedStream = new MemoryStream(compressedData))
                using (var gzipStream = new GZipStream(compressedStream, CompressionMode.Decompress))
                using (var decompressedStream = new MemoryStream())
                {
                    gzipStream.CopyTo(decompressedStream);
                    return decompressedStream.ToArray();
                }
            }
            catch
            {
                // 압축되지 않은 데이터로 처리
                return compressedData;
            }
        }
    }

    /// <summary>
    /// 서버 데이터 파싱
    /// </summary>
    private static List<ServerInfo> ParseServerData(byte[] data)
    {
        var servers = new List<ServerInfo>();
        var decoder = new BinaryDecoder(data);

        try
        {
            // 서버 개수 읽기 (2바이트)
            ushort serverCount = decoder.ReadUInt16();
            
            Console.WriteLine($"서버 개수: {serverCount}");

            // 각 서버 정보 파싱
            for (int i = 0; i < serverCount; i++)
            {
                var server = new ServerInfo();

                try
                {
                    // 기본 서버 정보 읽기
                    server.ServerID = decoder.ReadByte();
                    server.ServerStatus = decoder.ReadUInt32();
                    server.ServerPort = decoder.ReadUInt16();
                    server.ServerType = decoder.ReadByte();

                    // 문자열 정보 읽기
                    server.ServerName = decoder.ReadDBCSString();
                    server.AdditionalInfo = decoder.ReadDBCSString();
                    server.Description = decoder.ReadDBCSString();
                    
                    // 추가 메타데이터 (선택사항)
                    if (decoder.Remaining > 2)
                    {
                        server.ExtraData = decoder.ReadUnicodeString();
                    }

                    servers.Add(server);
                    
                    Console.WriteLine($"서버 {i + 1}: {server}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"서버 {i + 1} 파싱 중 오류: {ex.Message}");
                    // 일부 서버 파싱 실패해도 계속 진행
                    break;
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"서버 데이터 파싱 오류: {ex.Message}");
        }

        return servers;
    }

    /// <summary>
    /// 간단한 파싱 (서버 이름과 추가정보만)
    /// </summary>
    public static ParseResult ParseServerDatSimple(string filePath)
    {
        var result = new ParseResult();

        try
        {
            byte[] fileData = File.ReadAllBytes(filePath);
            
            // CRC32 스킵하고 압축 데이터 처리
            byte[] compressedData = new byte[fileData.Length - 4];
            Array.Copy(fileData, 4, compressedData, 0, compressedData.Length);

            byte[] decompressedData = DecompressData(compressedData);
            var decoder = new BinaryDecoder(decompressedData);

            // 서버 개수 읽기
            ushort serverCount = decoder.ReadUInt16();

            // 각 서버의 이름과 추가정보만 읽기
            for (int i = 0; i < serverCount; i++)
            {
                var server = new ServerInfo();
                
                // 기본 정보 스킵하고 문자열만 읽기
                server.ServerName = decoder.ReadDBCSString();
                server.AdditionalInfo = decoder.ReadDBCSString();
                
                result.Servers.Add(server);
            }

            result.Success = true;
            return result;
        }
        catch (Exception ex)
        {
            result.ErrorMessage = $"간단 파싱 오류: {ex.Message}";
            return result;
        }
    }
}

/// <summary>
/// 사용 예제 및 테스트
/// </summary>
public class Program
{
    public static void Main(string[] args)
    {
        string serverDatPath = @"C:\Game\Server.dat"; // 실제 파일 경로로 변경

        Console.WriteLine("=== Server.dat 파일 파서 ===\n");

        // 전체 파싱
        var result = ServerDatParser.ParseServerDat(serverDatPath);
        
        if (result.Success)
        {
            Console.WriteLine($"✅ 파싱 성공!");
            Console.WriteLine($"📁 압축 해제 크기: {result.DecompressedSize:N0} 바이트");
            Console.WriteLine($"🔐 CRC32 체크섬: 0x{result.FileChecksum:X8}");
            Console.WriteLine($"🌐 서버 개수: {result.Servers.Count}\n");

            Console.WriteLine("📋 서버 목록:");
            Console.WriteLine(new string('-', 80));
            
            for (int i = 0; i < result.Servers.Count; i++)
            {
                var server = result.Servers[i];
                Console.WriteLine($"{i + 1,2}. {server.ServerName}");
                
                if (!string.IsNullOrEmpty(server.AdditionalInfo))
                {
                    Console.WriteLine($"    ℹ️  {server.AdditionalInfo}");
                }
                
                if (!string.IsNullOrEmpty(server.Description))
                {
                    Console.WriteLine($"    📝 {server.Description}");
                }
                
                Console.WriteLine($"    🏷️  ID: {server.ServerID}, 상태: {server.ServerStatus}, 포트: {server.ServerPort}");
                Console.WriteLine();
            }
        }
        else
        {
            Console.WriteLine($"❌ 파싱 실패: {result.ErrorMessage}");
        }

        Console.WriteLine("\n=== 간단 파싱 테스트 ===");
        
        // 간단 파싱 (이름과 추가정보만)
        var simpleResult = ServerDatParser.ParseServerDatSimple(serverDatPath);
        
        if (simpleResult.Success)
        {
            Console.WriteLine("✅ 간단 파싱 성공!\n");
            foreach (var server in simpleResult.Servers)
            {
                Console.WriteLine($"🖥️  {server.ServerName}");
                if (!string.IsNullOrEmpty(server.AdditionalInfo))
                {
                    Console.WriteLine($"    ↳ {server.AdditionalInfo}");
                }
            }
        }
        else
        {
            Console.WriteLine($"❌ 간단 파싱 실패: {simpleResult.ErrorMessage}");
        }

        Console.WriteLine("\n아무 키나 누르세요...");
        Console.ReadKey();
    }
}

/// <summary>
/// Server.dat 파일 수정 유틸리티
/// </summary>
public static class ServerDatModifier
{
    /// <summary>
    /// 서버 추가정보 수정
    /// </summary>
    public static bool ModifyServerInfo(string filePath, int serverIndex, string newAdditionalInfo)
    {
        try
        {
            var result = ServerDatParser.ParseServerDat(filePath);
            if (!result.Success || serverIndex >= result.Servers.Count)
                return false;

            // 서버 정보 수정
            result.Servers[serverIndex].AdditionalInfo = newAdditionalInfo;

            // TODO: 파일 다시 저장하는 기능 구현
            // (인코딩 → 압축 → CRC32 계산 → 파일 쓰기)
            
            Console.WriteLine($"서버 {serverIndex} 추가정보 수정됨: {newAdditionalInfo}");
            return true;
        }
        catch
        {
            return false;
        }
    }
}


// 기본 사용
var result = ServerDatParser.ParseServerDat(@"C:\Game\Server.dat");

if (result.Success)
{
    Console.WriteLine($"서버 개수: {result.Servers.Count}");
    foreach (var server in result.Servers)
    {
        Console.WriteLine($"{server.ServerName}: {server.AdditionalInfo}");
    }
}


<서버파일 만드는 코드 추정>

using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Text;

/// <summary>
/// Server.dat 파일 생성기 클래스
/// </summary>
public class ServerDatGenerator
{
    /// <summary>
    /// 서버 정보 클래스
    /// </summary>
    public class ServerInfo
    {
        public byte ServerID { get; set; }
        public uint ServerStatus { get; set; } = 1; // 기본: 정상 상태
        public ushort ServerPort { get; set; } = 7001;
        public byte ServerType { get; set; } = 0; // 기본: 일반 서버
        public string ServerName { get; set; } = "";
        public string AdditionalInfo { get; set; } = "";
        public string Description { get; set; } = "";
        public string ExtraData { get; set; } = "";

        public ServerInfo() { }

        public ServerInfo(string name, string additionalInfo, byte id = 0)
        {
            ServerName = name;
            AdditionalInfo = additionalInfo;
            ServerID = id;
        }

        public override string ToString()
        {
            return $"[{ServerID}] {ServerName} - {AdditionalInfo}";
        }
    }

    /// <summary>
    /// 생성 결과 클래스
    /// </summary>
    public class GenerateResult
    {
        public bool Success { get; set; }
        public string ErrorMessage { get; set; } = "";
        public uint CRC32Checksum { get; set; }
        public int UncompressedSize { get; set; }
        public int CompressedSize { get; set; }
        public int FileSize { get; set; }
        public string FilePath { get; set; } = "";
    }

    /// <summary>
    /// CRC32 계산 클래스
    /// </summary>
    private static class CRC32
    {
        private static readonly uint[] Table = new uint[256];

        static CRC32()
        {
            for (uint i = 0; i < 256; i++)
            {
                uint crc = i;
                for (int j = 0; j < 8; j++)
                {
                    if ((crc & 1) == 1)
                        crc = (crc >> 1) ^ 0xEDB88320;
                    else
                        crc >>= 1;
                }
                Table[i] = crc;
            }
        }

        public static uint Calculate(byte[] data)
        {
            uint crc = 0xFFFFFFFF;
            foreach (byte b in data)
            {
                crc = Table[(crc ^ b) & 0xFF] ^ (crc >> 8);
            }
            return ~crc;
        }
    }

    /// <summary>
    /// 바이너리 인코더 클래스
    /// </summary>
    private class BinaryEncoder
    {
        private readonly MemoryStream _stream;
        private readonly BinaryWriter _writer;

        public BinaryEncoder()
        {
            _stream = new MemoryStream();
            _writer = new BinaryWriter(_stream);
        }

        public byte[] GetBytes()
        {
            return _stream.ToArray();
        }

        public int Position => (int)_stream.Position;

        public void WriteByte(byte value)
        {
            _writer.Write(value);
        }

        public void WriteUInt16(ushort value)
        {
            _writer.Write(value);
        }

        public void WriteUInt32(uint value)
        {
            _writer.Write(value);
        }

        public void WriteDBCSString(string text)
        {
            if (string.IsNullOrEmpty(text))
            {
                WriteByte(0);
                return;
            }

            try
            {
                // 한국어 인코딩 사용 (CP949)
                var encoding = Encoding.GetEncoding("ks_c_5601-1987");
                byte[] bytes = encoding.GetBytes(text);
                
                // 길이 제한 (최대 255바이트)
                if (bytes.Length > 255)
                {
                    Array.Resize(ref bytes, 255);
                }

                WriteByte((byte)bytes.Length);
                _writer.Write(bytes);
            }
            catch
            {
                // 폴백: 기본 인코딩 사용
                byte[] bytes = Encoding.Default.GetBytes(text);
                if (bytes.Length > 255)
                {
                    Array.Resize(ref bytes, 255);
                }

                WriteByte((byte)bytes.Length);
                _writer.Write(bytes);
            }
        }

        public void WriteUnicodeString(string text)
        {
            if (string.IsNullOrEmpty(text))
            {
                WriteUInt16(0);
                return;
            }

            byte[] bytes = Encoding.Unicode.GetBytes(text);
            
            // 길이 제한 (최대 65535바이트)
            if (bytes.Length > 65535)
            {
                Array.Resize(ref bytes, 65535);
            }

            WriteUInt16((ushort)bytes.Length);
            _writer.Write(bytes);
        }

        public void Dispose()
        {
            _writer?.Dispose();
            _stream?.Dispose();
        }
    }

    /// <summary>
    /// Server.dat 파일 생성
    /// </summary>
    /// <param name="servers">서버 목록</param>
    /// <param name="outputPath">출력 파일 경로</param>
    /// <returns>생성 결과</returns>
    public static GenerateResult GenerateServerDat(List<ServerInfo> servers, string outputPath)
    {
        var result = new GenerateResult { FilePath = outputPath };

        try
        {
            // 1. 서버 데이터 인코딩
            byte[] uncompressedData = EncodeServerData(servers);
            result.UncompressedSize = uncompressedData.Length;

            // 2. 데이터 압축
            byte[] compressedData = CompressData(uncompressedData);
            result.CompressedSize = compressedData.Length;

            // 3. CRC32 체크섬 계산
            result.CRC32Checksum = CRC32.Calculate(uncompressedData);

            // 4. 최종 파일 생성
            using (var fileStream = new FileStream(outputPath, FileMode.Create, FileAccess.Write))
            using (var writer = new BinaryWriter(fileStream))
            {
                // CRC32 체크섬 쓰기 (4바이트)
                writer.Write(result.CRC32Checksum);
                
                // 압축된 데이터 쓰기
                writer.Write(compressedData);
            }

            result.FileSize = (int)new FileInfo(outputPath).Length;
            result.Success = true;

            return result;
        }
        catch (Exception ex)
        {
            result.ErrorMessage = $"파일 생성 중 오류 발생: {ex.Message}";
            return result;
        }
    }

    /// <summary>
    /// 서버 데이터 인코딩
    /// </summary>
    private static byte[] EncodeServerData(List<ServerInfo> servers)
    {
        using (var encoder = new BinaryEncoder())
        {
            // 서버 개수 쓰기 (2바이트)
            encoder.WriteUInt16((ushort)servers.Count);

            // 각 서버 정보 인코딩
            foreach (var server in servers)
            {
                // 기본 서버 정보 (8바이트)
                encoder.WriteByte(server.ServerID);
                encoder.WriteUInt32(server.ServerStatus);
                encoder.WriteUInt16(server.ServerPort);
                encoder.WriteByte(server.ServerType);

                // 문자열 정보 (가변 길이)
                encoder.WriteDBCSString(server.ServerName);
                encoder.WriteDBCSString(server.AdditionalInfo);
                encoder.WriteDBCSString(server.Description);

                // 추가 메타데이터 (선택사항)
                if (!string.IsNullOrEmpty(server.ExtraData))
                {
                    encoder.WriteUnicodeString(server.ExtraData);
                }
                else
                {
                    encoder.WriteUInt16(0); // 빈 유니코드 문자열
                }
            }

            return encoder.GetBytes();
        }
    }

    /// <summary>
    /// 간단한 서버 데이터 인코딩 (이름과 추가정보만)
    /// </summary>
    private static byte[] EncodeServerDataSimple(List<ServerInfo> servers)
    {
        using (var encoder = new BinaryEncoder())
        {
            // 서버 개수 쓰기
            encoder.WriteUInt16((ushort)servers.Count);

            // 각 서버의 이름과 추가정보만 인코딩
            foreach (var server in servers)
            {
                encoder.WriteDBCSString(server.ServerName);
                encoder.WriteDBCSString(server.AdditionalInfo);
            }

            return encoder.GetBytes();
        }
    }

    /// <summary>
    /// 데이터 압축
    /// </summary>
    private static byte[] CompressData(byte[] data)
    {
        using (var output = new MemoryStream())
        {
            // zlib 헤더 추가 (RFC 1950)
            output.WriteByte(0x78); // CMF
            output.WriteByte(0x9C); // FLG

            using (var deflateStream = new DeflateStream(output, CompressionLevel.Optimal, true))
            {
                deflateStream.Write(data, 0, data.Length);
            }

            // Adler-32 체크섬 추가 (zlib 요구사항)
            uint adler32 = CalculateAdler32(data);
            output.WriteByte((byte)(adler32 >> 24));
            output.WriteByte((byte)(adler32 >> 16));
            output.WriteByte((byte)(adler32 >> 8));
            output.WriteByte((byte)adler32);

            return output.ToArray();
        }
    }

    /// <summary>
    /// Adler-32 체크섬 계산
    /// </summary>
    private static uint CalculateAdler32(byte[] data)
    {
        const uint MOD_ADLER = 65521;
        uint a = 1, b = 0;

        foreach (byte c in data)
        {
            a = (a + c) % MOD_ADLER;
            b = (b + a) % MOD_ADLER;
        }

        return (b << 16) | a;
    }

    /// <summary>
    /// 간단한 Server.dat 생성 (이름과 추가정보만)
    /// </summary>
    public static GenerateResult GenerateServerDatSimple(List<ServerInfo> servers, string outputPath)
    {
        var result = new GenerateResult { FilePath = outputPath };

        try
        {
            byte[] uncompressedData = EncodeServerDataSimple(servers);
            result.UncompressedSize = uncompressedData.Length;

            byte[] compressedData = CompressData(uncompressedData);
            result.CompressedSize = compressedData.Length;

            result.CRC32Checksum = CRC32.Calculate(uncompressedData);

            using (var fileStream = new FileStream(outputPath, FileMode.Create, FileAccess.Write))
            using (var writer = new BinaryWriter(fileStream))
            {
                writer.Write(result.CRC32Checksum);
                writer.Write(compressedData);
            }

            result.FileSize = (int)new FileInfo(outputPath).Length;
            result.Success = true;

            return result;
        }
        catch (Exception ex)
        {
            result.ErrorMessage = $"간단 파일 생성 중 오류: {ex.Message}";
            return result;
        }
    }

    /// <summary>
    /// 샘플 서버 목록 생성
    /// </summary>
    public static List<ServerInfo> CreateSampleServers()
    {
        return new List<ServerInfo>
        {
            new ServerInfo
            {
                ServerID = 1,
                ServerName = "한국서버1",
                AdditionalInfo = "210.123.45.67:7001\n현재 1,234명 접속중\n신규유저 권장",
                Description = "한국 메인 서버",
                ServerStatus = 1,
                ServerPort = 7001,
                ServerType = 0,
                ExtraData = "MainServer=true;Region=KR;MaxUsers=5000"
            },
            new ServerInfo
            {
                ServerID = 2,
                ServerName = "한국서버2",
                AdditionalInfo = "210.123.45.68:7002\n현재 2,567명 접속중\n고수유저 권장",
                Description = "한국 보조 서버",
                ServerStatus = 1,
                ServerPort = 7002,
                ServerType = 1,
                ExtraData = "MainServer=false;Region=KR;MaxUsers=3000"
            },
            new ServerInfo
            {
                ServerID = 3,
                ServerName = "일본서버",
                AdditionalInfo = "jp.game-server.com:7003\n現在567名接続中\n日本語サポート",
                Description = "일본 전용 서버",
                ServerStatus = 1,
                ServerPort = 7003,
                ServerType = 0,
                ExtraData = "MainServer=true;Region=JP;Language=ja"
            },
            new ServerInfo
            {
                ServerID = 4,
                ServerName = "테스트서버",
                AdditionalInfo = "🧪 베타 테스트 진행중\n⚠️ 데이터 초기화 가능\n💡 새로운 기능 체험",
                Description = "개발 및 테스트용",
                ServerStatus = 2, // 테스트 상태
                ServerPort = 7999,
                ServerType = 99, // 테스트 서버
                ExtraData = "TestServer=true;WipeData=true;Features=experimental"
            },
            new ServerInfo
            {
                ServerID = 99,
                ServerName = "점검중서버",
                AdditionalInfo = "🔧 정기 점검중\n⏰ 오후 6시 재오픈 예정\n📞 문의: support@game.com",
                Description = "정기점검중",
                ServerStatus = 0, // 점검 상태
                ServerPort = 7000,
                ServerType = 0,
                ExtraData = "Maintenance=true;ExpectedUp=18:00"
            }
        };
    }
}

/// <summary>
/// 사용 예제 및 테스트
/// </summary>
public class ServerDatGeneratorExample
{
    public static void Main(string[] args)
    {
        Console.WriteLine("=== Server.dat 파일 생성기 ===\n");

        // 1. 샘플 서버 데이터 생성
        var servers = ServerDatGenerator.CreateSampleServers();
        
        Console.WriteLine($"📋 생성할 서버 목록 ({servers.Count}개):");
        Console.WriteLine(new string('-', 80));
        for (int i = 0; i < servers.Count; i++)
        {
            var server = servers[i];
            Console.WriteLine($"{i + 1}. {server.ServerName} (ID: {server.ServerID})");
            Console.WriteLine($"   📍 {server.AdditionalInfo.Split('\n')[0]}");
            Console.WriteLine($"   💬 {server.Description}");
            Console.WriteLine();
        }

        // 2. Server.dat 파일 생성
        string outputPath = "Server.dat";
        var result = ServerDatGenerator.GenerateServerDat(servers, outputPath);

        if (result.Success)
        {
            Console.WriteLine("✅ Server.dat 파일 생성 성공!");
            Console.WriteLine($"📁 파일 경로: {Path.GetFullPath(result.FilePath)}");
            Console.WriteLine($"📊 통계:");
            Console.WriteLine($"   - 원본 크기: {result.UncompressedSize:N0} 바이트");
            Console.WriteLine($"   - 압축 크기: {result.CompressedSize:N0} 바이트");
            Console.WriteLine($"   - 최종 파일: {result.FileSize:N0} 바이트");
            Console.WriteLine($"   - 압축률: {(1.0 - (double)result.CompressedSize / result.UncompressedSize) * 100:F1}%");
            Console.WriteLine($"   - CRC32: 0x{result.CRC32Checksum:X8}");
        }
        else
        {
            Console.WriteLine($"❌ 파일 생성 실패: {result.ErrorMessage}");
        }

        // 3. 간단한 버전도 생성
        Console.WriteLine("\n=== 간단한 버전 생성 ===");
        string simpleOutputPath = "Server_Simple.dat";
        var simpleResult = ServerDatGenerator.GenerateServerDatSimple(servers, simpleOutputPath);

        if (simpleResult.Success)
        {
            Console.WriteLine("✅ 간단한 Server.dat 생성 성공!");
            Console.WriteLine($"📁 파일: {Path.GetFullPath(simpleResult.FilePath)}");
            Console.WriteLine($"📊 크기: {simpleResult.FileSize:N0} 바이트");
        }

        // 4. 커스텀 서버 추가 예제
        Console.WriteLine("\n=== 커스텀 서버 추가 ===");
        
        var customServers = new List<ServerDatGenerator.ServerInfo>
        {
            new ServerDatGenerator.ServerInfo
            {
                ServerID = 100,
                ServerName = "나만의 서버",
                AdditionalInfo = "🎮 개인 서버\n🚀 무제한 레벨업\n💎 모든 아이템 제공",
                Description = "치트 서버",
                ServerStatus = 1,
                ServerPort = 8000,
                ExtraData = "CheatMode=true;GodMode=enabled"
            },
            new ServerDatGenerator.ServerInfo("이벤트서버", "🎉 더블 경험치\n🎁 매일 선물\n⭐ 레어 아이템 확률 UP", 101),
            new ServerDatGenerator.ServerInfo("PvP서버", "⚔️ 무제한 PK\n🏆 랭킹 시스템\n💀 하드코어 모드", 102)
        };

        string customOutputPath = "Server_Custom.dat";
        var customResult = ServerDatGenerator.GenerateServerDat(customServers, customOutputPath);

        if (customResult.Success)
        {
            Console.WriteLine($"✅ 커스텀 서버 파일 생성 완료: {customOutputPath}");
            foreach (var server in customServers)
            {
                Console.WriteLine($"   🖥️  {server.ServerName}");
            }
        }

        Console.WriteLine("\n=== 생성된 파일 검증 ===");
        
        // 5. 생성된 파일을 다시 읽어서 검증
        if (File.Exists(outputPath))
        {
            var parseResult = ServerDatParser.ParseServerDat(outputPath);
            if (parseResult.Success)
            {
                Console.WriteLine("✅ 파일 검증 성공!");
                Console.WriteLine($"🔍 읽어온 서버 개수: {parseResult.Servers.Count}");
                Console.WriteLine($"🔐 체크섬 일치: {parseResult.CalculatedChecksum == parseResult.FileChecksum}");
            }
            else
            {
                Console.WriteLine($"❌ 파일 검증 실패: {parseResult.ErrorMessage}");
            }
        }

        Console.WriteLine("\n아무 키나 누르세요...");
        Console.ReadKey();
    }
}

/// <summary>
/// Server.dat 파일 수정 유틸리티
/// </summary>
public static class ServerDatModifier
{
    /// <summary>
    /// 기존 Server.dat 파일에 서버 추가
    /// </summary>
    public static bool AddServerToFile(string filePath, ServerDatGenerator.ServerInfo newServer)
    {
        try
        {
            // 기존 파일 읽기
            var parseResult = ServerDatParser.ParseServerDat(filePath);
            if (!parseResult.Success) return false;

            // 새 서버 추가
            var servers = new List<ServerDatGenerator.ServerInfo>();
            foreach (var server in parseResult.Servers)
            {
                servers.Add(new ServerDatGenerator.ServerInfo
                {
                    ServerID = server.ServerID,
                    ServerName = server.ServerName,
                    AdditionalInfo = server.AdditionalInfo,
                    Description = server.Description,
                    ServerStatus = server.ServerStatus,
                    ServerPort = server.ServerPort,
                    ServerType = server.ServerType,
                    ExtraData = server.ExtraData
                });
            }
            servers.Add(newServer);

            // 파일 다시 생성
            var result = ServerDatGenerator.GenerateServerDat(servers, filePath);
            return result.Success;
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// 서버 정보 수정
    /// </summary>
    public static bool ModifyServer(string filePath, byte serverID, string newName, string newAdditionalInfo)
    {
        try
        {
            var parseResult = ServerDatParser.ParseServerDat(filePath);
            if (!parseResult.Success) return false;

            var servers = new List<ServerDatGenerator.ServerInfo>();
            foreach (var server in parseResult.Servers)
            {
                var newServer = new ServerDatGenerator.ServerInfo
                {
                    ServerID = server.ServerID,
                    ServerName = server.ServerID == serverID ? newName : server.ServerName,
                    AdditionalInfo = server.ServerID == serverID ? newAdditionalInfo : server.AdditionalInfo,
                    Description = server.Description,
                    ServerStatus = server.ServerStatus,
                    ServerPort = server.ServerPort,
                    ServerType = server.ServerType,
                    ExtraData = server.ExtraData
                };
                servers.Add(newServer);
            }

            var result = ServerDatGenerator.GenerateServerDat(servers, filePath);
            return result.Success;
        }
        catch
        {
            return false;
        }
    }
}

// 기본 사용
var servers = new List<ServerDatGenerator.ServerInfo>
{
    new ServerDatGenerator.ServerInfo
    {
        ServerName = "한국서버1",
        AdditionalInfo = "210.123.45.67:7001\n현재 1,234명 접속중",
        ServerID = 1
    }
};

var result = ServerDatGenerator.GenerateServerDat(servers, "Server.dat");
if (result.Success)
{
    Console.WriteLine($"생성 완료! 파일 크기: {result.FileSize} 바이트");
}


// 샘플로 생성
var servers = ServerDatGenerator.CreateSampleServers();
// 한국서버1, 한국서버2, 일본서버, 테스트서버, 점검중서버

---------------
Server.dat의 추가정보로는 직접 접속할 수 없습니다! 실제로는 다음과 같은 과정을 거칩니다:
실제 서버 접속 과정:
1. 서버 선택 시
c// 사용자가 서버 선택 → 서버 인덱스만 전송
CMultiServerPacket packet;
packet.serverIndex = 선택된서버인덱스; // Server.dat의 추가정보는 사용 안 함!
Send(packet);
2. 로그인 서버 응답
c// 서버가 실제 게임 서버 정보를 응답
STransferServerPacket response;
response.realServerIP = "game1.server.com";
response.realServerPort = 7001;
// ↑ 이것이 실제 접속 주소!
3. 게임 서버로 재접속
c// 기존 연결 종료 후 실제 게임 서버로 재연결
closesocket(loginServerSocket);
OpenTCPIPSocket(realServerIP, realServerPort);

==========
<코드부분>
3. 서버 응답 처리
MainMenuPane_HandleServerPackets - Case 3:
ccase 3:
    // STransferServerPacket 처리
    uVar4 = MapPane::ProcessTransferServer2__((MapPane *)((int)this + -0xc), (int)puVar2);
    return uVar4;
ProcessTransferServer2__ - 실제 서버 정보 수신:
c// 1. 서버로부터 실제 접속 정보 수신
FUN_0051b4c0(DAT_0060d1bc, 
             *(undefined4 *)(param_1 + 0x24),    // 실제 서버 IP
             *(undefined2 *)(param_1 + 0x28));   // 실제 서버 포트

// 2. 새로운 서버로 재접속 준비
Thread::WaitForResult(...);

// 3. CTransferServerPacket 생성 및 전송
puVar3 = CTransferServerPacket::__CreateInstance(puVar3);
*(undefined1 *)(puVar3 + 9) = *(undefined1 *)(param_1 + 0x2a);
CPacket::Send(puVar3);
4. 실제 게임 서버 연결
ProcessTransferServerMessage - 소켓 재연결:
c// 1. 기존 로그인 서버 연결 종료
closesocket(기존소켓);
WSACleanup();

// 2. 실제 게임 서버로 새 소켓 연결
OpenTCPIPSocket(this, 실제서버IP, 실제서버포트);
Sleep(1000);
==========