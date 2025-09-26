import pydivert
import sys

if len(sys.argv) != 5:
    print("usage: python packet_redirect_v3.py <original_server_ip> <original_server_port> <new_server_ip> <new_server_port>")
    print("ex: python packet_redirect_v3.py 222.168.111.123 4321 192.168.0.15 1234")
    sys.exit(1)


# 가로챌 원래 목적지 주소 및 포트

original_ip = sys.argv[1]#"222.168.111.123"

original_port = int(sys.argv[2])#1234



# 변경할 목적지 주소 및 포트

redirect_ip = sys.argv[3]#"192.168.0.15"

redirect_port = int(sys.argv[4])#1234



# 필터 설정: TCP 3-way handshake 및 데이터 패킷을 모두 가로채기

filter_str = f"(tcp.DstPort == {original_port} or tcp.SrcPort == {redirect_port}) and (ip.DstAddr == {original_ip} or ip.SrcAddr == {redirect_ip})"



print(f"[*] Filtering packets: {filter_str}")



# NAT 매핑을 저장할 딕셔너리

connection_map = {}



with pydivert.WinDivert(filter_str) as w:

    for packet in w:

        # 클라이언트 -> 서버로 가는 패킷

        if packet.dst_addr == original_ip and packet.dst_port == original_port:

            # NAT 매핑 저장 (클라이언트의 원래 IP, 포트 -> 변경된 IP)

            connection_map[(packet.src_addr, packet.src_port)] = (packet.dst_addr, packet.dst_port)

            

            # 목적지를 변경하여 패킷 전송

            packet.dst_addr = redirect_ip

            packet.dst_port = redirect_port

            print(f"[*] Redirecting {packet.src_addr}:{packet.src_port} -> {redirect_ip}:{redirect_port}")



        # 서버 -> 클라이언트로 가는 패킷 (응답 패킷)

        elif packet.src_addr == redirect_ip and packet.src_port == redirect_port:

            # 기존 매핑 정보가 있는 경우 클라이언트의 원래 주소로 변경

            original_dst = connection_map.get((packet.dst_addr, packet.dst_port))

            if original_dst:

                packet.src_addr, packet.src_port = original_dst

                print(f"[*] Redirecting response {redirect_ip}:{redirect_port} -> {packet.dst_addr}:{packet.dst_port}")



        # 수정된 패킷을 다시 네트워크로 전송

        w.send(packet)

