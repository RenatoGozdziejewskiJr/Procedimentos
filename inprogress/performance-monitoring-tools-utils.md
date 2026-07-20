Perfomance Monitoring tools:

pktmon - rawcap

Hi Renato - I just saw Rafael's email with Mauricio confirming that the high CPU was when Millikan software was connected. I couldn't remember if I had given you all the info about how I had captured comms logs before, but there were 2 ways. One for the internal localhost comms (UI <-> System Controller) and one for "external" comms (everything else).
 
The internal comms used the RawCap utility.
 
The external comms capture used PktMon, which is built in to Windows 10. This is what I used to capture for 240 seconds...
 
pktmon start --capture --pkt-size 0
timeout /t 240
pktmon stop

That creates an PktMon.etl file which can then be converted to the pcapng format that Wireshark can read with the command
 
pktmon etl2pcap PktMon.etl --out test.pcapng

Unfortunately I did not find a way to capture internal and external comms all together.

--------------------------------------------------

To monitor memory, disk, etc...

WPR (windows 10 installed tool)
https://learn.microsoft.com/en-us/windows-hardware/test/wpt/wpr-command-line-options
 
Typeperf:
https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/typeperf

There was also procdump, which can create a crash dump when high CPU is detected 
https://learn.microsoft.com/en-us/sysinternals/downloads/procdump