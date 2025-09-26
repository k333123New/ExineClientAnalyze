start_emu_server.bat -> login server
start_emu_server2.bat -> main server


how to change server ip change
->edit emu_server.py (with CLoginPacket ack, with CVersionPacket args)
->edit emu_server2.py (with CLoginPacket ack)
->edit hex Exine\RData\Server.dat  (0x02~0x05, each 1byte)
->extract local.dat with dattol & edit ServersKR.txt end archive local.dat with dattol
