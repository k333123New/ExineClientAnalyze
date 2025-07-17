using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Linq;

class CustomFileProcessor
{
    const int FileNameLength = 32;

    // .dat 파일을 추출하는 함수
    public static void ExtractFiles(string inputFilePath)
    {
        using var reader = new BinaryReader(File.OpenRead(inputFilePath));
        int fileCount = reader.ReadInt32();

        var fileEntries = new List<(int Offset, string Name)>();

        for (int i = 0; i < fileCount; i++)
        {
            int offset = reader.ReadInt32();
            byte[] nameBytes = reader.ReadBytes(FileNameLength);
            string name = Encoding.UTF8.GetString(nameBytes).Split('\0')[0];
            fileEntries.Add((offset, name));
        }

        string outputFolder = Path.GetFileNameWithoutExtension(inputFilePath);
        Directory.CreateDirectory(outputFolder);

        for (int i = 0; i < fileCount - 1; i++)
        {
            int startOffset = fileEntries[i].Offset;
            int endOffset = fileEntries[i + 1].Offset;
            int size = endOffset - startOffset;

            reader.BaseStream.Seek(startOffset, SeekOrigin.Begin);
            byte[] fileData = reader.ReadBytes(size);

            string outputPath = Path.Combine(outputFolder, fileEntries[i].Name);
            File.WriteAllBytes(outputPath, fileData);
            Console.WriteLine($"Extracted: {outputPath}");
        }

        // dummy.bin 추출 (첫 파일 오프셋 - 36 바이트 위치)
        int dummyOffset = fileEntries[0].Offset - 36;
        if (dummyOffset >= 0)
        {
            reader.BaseStream.Seek(dummyOffset, SeekOrigin.Begin);
            byte[] dummyData = reader.ReadBytes(36);

            string dummyFilePath = Path.Combine(outputFolder, "dummy.bin");
            File.WriteAllBytes(dummyFilePath, dummyData);
            Console.WriteLine($"Created dummy file: {dummyFilePath}");
        }
        else
        {
            Console.WriteLine("Cannot extract dummy: not enough data before first file offset.");
        }
    }

    // 폴더 내 파일들을 .dat 파일로 합치는 함수
    public static void CreateArchiveFromFolder(string folderName)
    {
        string[] allFiles = Directory.GetFiles(folderName);

        // dummy.bin 분리
        string dummyPath = allFiles.FirstOrDefault(f => Path.GetFileName(f).ToLower() == "dummy.bin");
        var files = allFiles.Where(f => Path.GetFileName(f).ToLower() != "dummy.bin").ToArray();

        if (files.Length == 0)
        {
            Console.WriteLine("No files to archive in folder (excluding dummy.bin).");
            return;
        }

        string outputFilePath = $"{folderName}.dat";

        using var stream = new MemoryStream();
        using var writer = new BinaryWriter(stream, Encoding.UTF8, true);

        int fileCount = files.Length + 1; // dummy.bin 포함

        writer.Write(fileCount); // 파일 갯수 + 1

        // 1. 헤더(오프셋 + 파일명) 자리 확보 (dummy.bin 제외한 실제 파일만 헤더에 씀)
        long headerStart = stream.Position;

        // dummy.bin은 헤더에 이름 안 넣음(또는 넣을 수도 있지만, 기존 방식 유지)
        // 여기선 dummy.bin 헤더는 넣지 않고 나머지 파일만 헤더 기록

        for (int i = 0; i < files.Length; i++)
        {
            writer.Write(0); // offset placeholder (4 bytes)
            writer.Write(new byte[FileNameLength]); // 파일명 자리 (32 bytes)
        }

        // 2. 파일 크기 총합 계산 (dummy.bin 제외 파일들)
        long totalDataSize = 0;
        var fileSizes = new long[files.Length];
        for (int i = 0; i < files.Length; i++)
        {
            fileSizes[i] = new FileInfo(files[i]).Length;
            totalDataSize += fileSizes[i];
        }

        byte[] dummyData = null;
        int dummyDataLength = 0;

        if (dummyPath != null && File.Exists(dummyPath))
        {
            dummyData = File.ReadAllBytes(dummyPath);
            dummyDataLength = dummyData.Length;
        }

        // 3. 데이터 영역 크기만큼 공간 확보(dummy.bin 크기 + 실제 파일들 크기)
        long totalDataAreaSize = dummyDataLength + totalDataSize;
        writer.Write(new byte[totalDataAreaSize]);

        // 4. 데이터 시작 위치 계산 (헤더 다음 위치)
        long dataStartPos = headerStart + files.Length * (4 + FileNameLength);

        // 5. 파일별 오프셋 계산 (dummy.bin 크기 만큼 밀림)
        var fileOffsets = new List<int>();
        long currentOffset = dataStartPos + dummyDataLength;
        foreach (var size in fileSizes)
        {
            fileOffsets.Add((int)currentOffset);
            currentOffset += size;
        }

        // 6. 헤더 위치로 돌아가서 오프셋과 파일명 기록
        writer.Seek((int)headerStart, SeekOrigin.Begin);
        for (int i = 0; i < files.Length; i++)
        {
            writer.Write(fileOffsets[i]);

            byte[] nameBytes = new byte[FileNameLength];
            byte[] rawName = Encoding.UTF8.GetBytes(Path.GetFileName(files[i]));
            Array.Copy(rawName, nameBytes, Math.Min(rawName.Length, FileNameLength));
            writer.Write(nameBytes);
        }

        // 7. dummyData 앞 4바이트에 전체 dat파일 크기 기록
        if (dummyData != null)
        {
            int totalDatFileSize = (int)(4 + (files.Length * (4 + FileNameLength)) + totalDataAreaSize); 
            // 4: 파일갯수(int), 헤더크기, 데이터크기 합산

            byte[] sizeBytes = BitConverter.GetBytes(totalDatFileSize);
            Array.Copy(sizeBytes, 0, dummyData, 0, 4);
        }

        // 8. dummyData 기록 (첫 번째 파일 앞에)
        if (dummyData != null)
        {
            writer.Seek((int)dataStartPos, SeekOrigin.Begin);
            writer.Write(dummyData);
        }

        // 9. 파일 데이터 기록
        for (int i = 0; i < files.Length; i++)
        {
            writer.Seek(fileOffsets[i], SeekOrigin.Begin);
            byte[] fileData = File.ReadAllBytes(files[i]);
            writer.Write(fileData);
        }

        // 10. 최종 저장
        File.WriteAllBytes(outputFilePath, stream.ToArray());
        Console.WriteLine($"Created archive: {outputFilePath}");
    }

    // 메인 실행부
    static void Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.WriteLine("Usage:");
            Console.WriteLine("  <.dat file> - to extract files.");
            Console.WriteLine("  <folder>    - to create .dat file.");
            return;
        }

        string inputPath = args[0];

        if (File.Exists(inputPath) && inputPath.EndsWith(".dat"))
        {
            ExtractFiles(inputPath);
        }
        else if (Directory.Exists(inputPath))
        {
            CreateArchiveFromFolder(inputPath);
        }
        else
        {
            Console.WriteLine("Invalid input. Please provide either a .dat file or a folder.");
        }
    }
}
