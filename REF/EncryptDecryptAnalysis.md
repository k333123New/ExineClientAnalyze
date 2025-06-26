기본 XOR 키: "NexonInc." 문자열
4E 65 78 6F 6E 49 6E 63 2E

추가 XOR 키 배열: 256개의 4바이트 값

인덱스 i에 대해 값은 0xIIIIIIII (여기서 II는 인덱스의 16진수 표현)
예: 인덱스 0 = 0x00000000, 인덱스 10 = 0x0A0A0A0A, 인덱스 255 = 0xFFFFFFFF



이러한 키들은 패킷 암호화 과정에서 DoXOR 함수를 통해 사용됩니다. 암호화 순서값(this[0x100aa])은 매 패킷마다 1씩 증가하며, 어떤 추가 XOR 키를 사용할지 결정하는 인덱스로 사용됩니다.

추가 XOR 키 배열 (this + 0x100e0)
추가 XOR 키 배열은 FUN_0051c3f0 함수에 의해 계산됩니다. 이 함수는 파라미터(코드 상 0으로 설정됨)에 따라 다른 알고리즘을 사용하여 키를 생성합니다.
param_1 = 0일 때, 알고리즘은 간단합니다:

각 인덱스(0-255)에 대해 uVar2 = uVar5 (현재 인덱스)
결과 값은 uVar2 | (uVar2 << 8) | (uVar2 << 16) | (uVar2 << 24)

즉, 4바이트 값에서 모든 바이트가 동일하게 설정됩니다. 예를 들어:

인덱스 0: 0x00000000
인덱스 1: 0x01010101
인덱스 2: 0x02020202
...
인덱스 255: 0xFFFFFFFF

이 추가 XOR 키 배열은 블록별 암호화와 최종 암호화에서 사용됩니다.


==============
c#기반 암복호화 코드(검증 필요함)

using System;
using System.Text;

public class PacketCrypto
{
    // 기본 XOR 키 (NexonInc.)
    private readonly byte[] baseKey;
    // 추가 XOR 키 배열 (256개의 4바이트 값)
    private readonly uint[] extraKeys;
    // 암호화 순서값 (0-255 순환)
    private byte encryptionSequence;

    /// <summary>
    /// 패킷 암호화/복호화를 위한 클래스 생성자
    /// </summary>
    public PacketCrypto()
    {
        // 기본 XOR 키 설정 (NexonInc.)
        baseKey = Encoding.ASCII.GetBytes("NexonInc.");
        
        // 추가 XOR 키 배열 초기화 (256개의 4바이트 값)
        extraKeys = new uint[256];
        InitializeExtraKeys();
        
        // 암호화 순서값 초기화
        encryptionSequence = 0;
    }

    /// <summary>
    /// 추가 XOR 키 배열 초기화
    /// </summary>
    private void InitializeExtraKeys()
    {
        // 알고리즘 타입 0: 각 인덱스에 대해 모든 바이트가 해당 인덱스와 동일
        for (int i = 0; i < 256; i++)
        {
            byte value = (byte)i;
            extraKeys[i] = ((uint)value << 24) | ((uint)value << 16) | ((uint)value << 8) | value;
        }
    }

    /// <summary>
    /// 암호화 순서값 증가 (0-255 순환)
    /// </summary>
    /// <returns>현재 암호화 순서값</returns>
    private byte IncrementEncryptionSequence()
    {
        byte current = encryptionSequence;
        encryptionSequence = (byte)((encryptionSequence + 1) % 256);
        return current;
    }

    /// <summary>
    /// XOR 연산 수행
    /// </summary>
    /// <param name="source">원본 데이터</param>
    /// <param name="sourceOffset">원본 데이터 시작 위치</param>
    /// <param name="destination">결과 데이터</param>
    /// <param name="destinationOffset">결과 데이터 시작 위치</param>
    /// <param name="length">처리할 길이</param>
    /// <param name="key">XOR 키</param>
    /// <param name="keySize">키 크기</param>
    private void DoXOR(byte[] source, int sourceOffset, byte[] destination, int destinationOffset, 
                      int length, byte[] key, int keySize)
    {
        for (int i = 0; i < length; i++)
        {
            int keyIndex = i % keySize;
            destination[destinationOffset + i] = (byte)(source[sourceOffset + i] ^ key[keyIndex]);
        }
    }

    /// <summary>
    /// XOR 연산 수행 (uint 키 사용)
    /// </summary>
    /// <param name="source">원본 데이터</param>
    /// <param name="sourceOffset">원본 데이터 시작 위치</param>
    /// <param name="destination">결과 데이터</param>
    /// <param name="destinationOffset">결과 데이터 시작 위치</param>
    /// <param name="length">처리할 길이</param>
    /// <param name="key">XOR 키 (uint)</param>
    private void DoXOR(byte[] source, int sourceOffset, byte[] destination, int destinationOffset, 
                      int length, uint key)
    {
        byte[] keyBytes = BitConverter.GetBytes(key);
        
        for (int i = 0; i < length; i++)
        {
            int keyIndex = i % 4;
            destination[destinationOffset + i] = (byte)(source[sourceOffset + i] ^ keyBytes[keyIndex]);
        }
    }

    /// <summary>
    /// 패킷 암호화
    /// </summary>
    /// <param name="packetData">원본 패킷 데이터</param>
    /// <returns>암호화된 패킷 데이터</returns>
    public byte[] EncryptPacket(byte[] packetData)
    {
        if (packetData == null || packetData.Length == 0)
            throw new ArgumentException("패킷 데이터가 비어 있습니다.");

        // 암호화된 패킷 크기 = 원본 + 암호화 순서값 + 종료 바이트
        byte[] encryptedData = new byte[packetData.Length + 2];
        
        // 첫 바이트(패킷 타입)는 그대로 복사
        encryptedData[0] = packetData[0];
        
        // 암호화 순서값 설정 및 증가
        byte sequence = IncrementEncryptionSequence();
        encryptedData[1] = sequence;
        
        // 패킷 데이터가 헤더(1바이트)만 있는 경우 추가 암호화 없음
        if (packetData.Length <= 1)
            return encryptedData;
        
        // 임시 버퍼 (암호화 작업용)
        byte[] tempBuffer = new byte[packetData.Length - 1];
        
        // 단계 1: 기본 XOR 키로 패킷 본문 암호화
        DoXOR(packetData, 1, tempBuffer, 0, packetData.Length - 1, baseKey, baseKey.Length);
        
        // 단계 2: 데이터 블록별로 추가 암호화
        int blockSize = baseKey.Length;
        int blockCount = (packetData.Length - 2) / blockSize + 1;
        
        for (int i = 0; i < blockCount; i++)
        {
            // 현재 블록의 인덱스가 암호화 순서값과 다른 경우에만 처리
            if (i != sequence)
            {
                int blockOffset = i * blockSize;
                int blockLength = Math.Min(blockSize, tempBuffer.Length - blockOffset);
                
                if (blockLength > 0)
                {
                    // 추가 XOR 암호화 적용
                    DoXOR(tempBuffer, blockOffset, tempBuffer, blockOffset, blockLength, extraKeys[i % 256]);
                }
            }
        }
        
        // 단계 3: 암호화 순서값에 따른 최종 XOR
        DoXOR(tempBuffer, 0, tempBuffer, 0, tempBuffer.Length, extraKeys[sequence]);
        
        // 암호화된 데이터를 결과 버퍼에 복사
        Array.Copy(tempBuffer, 0, encryptedData, 2, tempBuffer.Length);
        
        return encryptedData;
    }

    /// <summary>
    /// 패킷 복호화
    /// </summary>
    /// <param name="encryptedData">암호화된 패킷 데이터</param>
    /// <returns>복호화된 패킷 데이터</returns>
    public byte[] DecryptPacket(byte[] encryptedData)
    {
        if (encryptedData == null || encryptedData.Length < 2)
            throw new ArgumentException("암호화된 패킷 데이터가 너무 짧습니다.");

        // 복호화된 패킷 크기 = 암호화된 크기 - 암호화 순서값
        byte[] decryptedData = new byte[encryptedData.Length - 1];
        
        // 첫 바이트(패킷 타입)는 그대로 복사
        decryptedData[0] = encryptedData[0];
        
        // 암호화 순서값 가져오기
        byte sequence = encryptedData[1];
        
        // 패킷 데이터가 헤더와 순서값만 있는 경우 추가 복호화 없음
        if (encryptedData.Length <= 2)
            return decryptedData;
        
        // 임시 버퍼 (복호화 작업용)
        byte[] tempBuffer = new byte[encryptedData.Length - 2];
        Array.Copy(encryptedData, 2, tempBuffer, 0, tempBuffer.Length);
        
        // 단계 1: 암호화 순서값에 따른 XOR 복호화 (EncryptPacket의 단계 3 역연산)
        DoXOR(tempBuffer, 0, tempBuffer, 0, tempBuffer.Length, extraKeys[sequence]);
        
        // 단계 2: 데이터 블록별로 추가 복호화 (EncryptPacket의 단계 2 역연산)
        int blockSize = baseKey.Length;
        int blockCount = (encryptedData.Length - 3) / blockSize + 1;
        
        for (int i = 0; i < blockCount; i++)
        {
            // 현재 블록의 인덱스가 암호화 순서값과 다른 경우에만 처리
            if (i != sequence)
            {
                int blockOffset = i * blockSize;
                int blockLength = Math.Min(blockSize, tempBuffer.Length - blockOffset);
                
                if (blockLength > 0)
                {
                    // 추가 XOR 복호화 적용
                    DoXOR(tempBuffer, blockOffset, tempBuffer, blockOffset, blockLength, extraKeys[i % 256]);
                }
            }
        }
        
        // 단계 3: 기본 XOR 키로 패킷 본문 복호화 (EncryptPacket의 단계 1 역연산)
        DoXOR(tempBuffer, 0, decryptedData, 1, tempBuffer.Length, baseKey, baseKey.Length);
        
        return decryptedData;
    }

    /// <summary>
    /// CVersionPacket 생성
    /// </summary>
    /// <param name="versionNumber">버전 번호</param>
    /// <param name="productCode">제품 코드 (기본값 'A')</param>
    /// <param name="countryCode">국가 코드 (기본값 'K')</param>
    /// <returns>생성된 CVersionPacket</returns>
    public byte[] CreateVersionPacket(ushort versionNumber, char productCode = 'A', char countryCode = 'K')
    {
        // CVersionPacket 구조 (4바이트):
        // [0] - 패킷 타입 (고정값)
        // [1-2] - 버전 번호 (2바이트)
        // [3] - 제품 코드
        // [4] - 국가 코드
        byte[] packet = new byte[5];
        
        // 패킷 타입 설정 (가정: 패킷 타입 = 1)
        packet[0] = 1;
        
        // 버전 번호 설정 (리틀 엔디안)
        packet[1] = (byte)(versionNumber & 0xFF);
        packet[2] = (byte)((versionNumber >> 8) & 0xFF);
        
        // 제품 코드 설정
        packet[3] = (byte)productCode;
        
        // 국가 코드 설정
        packet[4] = (byte)countryCode;
        
        return packet;
    }

    /// <summary>
    /// 암호화된 패킷을 서버에 전송할 형식으로 변환
    /// </summary>
    /// <param name="encryptedPacket">암호화된 패킷</param>
    /// <returns>전송용 패킷 데이터</returns>
    public byte[] PreparePacketForSending(byte[] encryptedPacket)
    {
        // 전송용 패킷 구조:
        // [0] - 패킷 시작 마커 (0xAA)
        // [1-2] - 패킷 데이터 크기 (2바이트)
        // [3...] - 패킷 데이터
        byte[] sendPacket = new byte[encryptedPacket.Length + 3];
        
        // 패킷 시작 마커 설정
        sendPacket[0] = 0xAA;
        
        // 패킷 크기 설정 (리틀 엔디안)
        sendPacket[1] = (byte)(encryptedPacket.Length & 0xFF);
        sendPacket[2] = (byte)((encryptedPacket.Length >> 8) & 0xFF);
        
        // 패킷 데이터 복사
        Array.Copy(encryptedPacket, 0, sendPacket, 3, encryptedPacket.Length);
        
        return sendPacket;
    }

    /// <summary>
    /// 패킷 헤더 파싱 및 유효성 검사
    /// </summary>
    /// <param name="receivedData">수신한 데이터</param>
    /// <param name="packetData">추출된 패킷 데이터</param>
    /// <returns>패킷이 유효하면 true, 그렇지 않으면 false</returns>
    public bool ParsePacketHeader(byte[] receivedData, out byte[] packetData)
    {
        packetData = null;
        
        // 기본 검사
        if (receivedData == null || receivedData.Length < 3)
            return false;
        
        // 패킷 시작 마커 확인
        if (receivedData[0] != 0xAA)
            return false;
        
        // 패킷 크기 추출 (리틀 엔디안)
        int packetSize = receivedData[1] | (receivedData[2] << 8);
        
        // 패킷 크기 유효성 검사
        if (packetSize <= 0 || receivedData.Length < packetSize + 3)
            return false;
        
        // 패킷 데이터 추출
        packetData = new byte[packetSize];
        Array.Copy(receivedData, 3, packetData, 0, packetSize);
        
        return true;
    }
}

// 사용 예제
public class Program
{
    public static void Main()
    {
        // 패킷 암호화/복호화 클래스 생성
        PacketCrypto crypto = new PacketCrypto();
        
        // 버전 패킷 생성 (버전: 1234, 제품 코드: 'A', 국가 코드: 'K')
        byte[] versionPacket = crypto.CreateVersionPacket(1234, 'A', 'K');
        Console.WriteLine("원본 버전 패킷:");
        PrintBytes(versionPacket);
        
        // 패킷 암호화
        byte[] encryptedPacket = crypto.EncryptPacket(versionPacket);
        Console.WriteLine("\n암호화된 패킷:");
        PrintBytes(encryptedPacket);
        
        // 전송을 위한 패킷 준비
        byte[] sendPacket = crypto.PreparePacketForSending(encryptedPacket);
        Console.WriteLine("\n전송용 패킷:");
        PrintBytes(sendPacket);
        
        // 패킷 헤더 파싱 (서버 측 작업 시뮬레이션)
        if (crypto.ParsePacketHeader(sendPacket, out byte[] receivedEncryptedPacket))
        {
            Console.WriteLine("\n수신된 암호화 패킷:");
            PrintBytes(receivedEncryptedPacket);
            
            // 패킷 복호화
            byte[] decryptedPacket = crypto.DecryptPacket(receivedEncryptedPacket);
            Console.WriteLine("\n복호화된 패킷:");
            PrintBytes(decryptedPacket);
            
            // 복호화 성공 여부 확인
            bool success = versionPacket.Length == decryptedPacket.Length;
            if (success)
            {
                for (int i = 0; i < versionPacket.Length; i++)
                {
                    if (versionPacket[i] != decryptedPacket[i])
                    {
                        success = false;
                        break;
                    }
                }
            }
            
            Console.WriteLine($"\n복호화 성공 여부: {success}");
        }
        else
        {
            Console.WriteLine("패킷 헤더 파싱 실패");
        }
    }
    
    // 바이트 배열 출력 헬퍼 함수
    private static void PrintBytes(byte[] data)
    {
        for (int i = 0; i < data.Length; i++)
        {
            Console.Write($"{data[i]:X2} ");
            if ((i + 1) % 16 == 0 && i < data.Length - 1)
                Console.WriteLine();
        }
        Console.WriteLine();
    }
}
