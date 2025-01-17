# Logjammer

## Challenge Information
- **Challenge Name**: Logjammer
- **Category**: Log Analysis
- **Difficulty Level**: Easy

## Investigation Steps

### 1. Initial Security Log Analysis
I manually looked for the most earliest logon in the Security.evtx file

### 2. Firewall Rule Analysis
Get the most recent firewall rule addition from Windows Firewall-Firewall.evtx

```powershell
Get-WinEvent -Path "Windows Firewall-Firewall.evtx" | 
    Where-Object {
        $_.ID -eq 2004 # Event ID 2004 indicates a rule addition
    } | 
    Select-Object TimeCreated, ID, Message | 
    Sort-Object TimeCreated -Descending | 
    Select-Object -First 1 | 
    Format-List
```

Output:
```
TimeCreated: 3/27/2023 7:44:43 PM
Id: 2004
Message: A rule has been added to the Windows Defender Firewall exception list.

Added Rule:
    Rule ID: {11309293-FB68-4969-93F9-7F75A9032570}
    Rule Name: Metasploit C2 Bypass // this is the answer for this part
    Origin: Local
    Active: Yes
    Direction: Outbound // this is the answer for the next part
    Profiles: Private,Domain, Public
    Action: Allow
    Application Path:
    Service Name:
    Protocol: TCP
    Security Options: None
    Edge Traversal: None
    Modifying User: S-1-5-21-3393683511-3463148672-371912004-1001
    Modifying Application: C:\Windows\System32\mmc.exe
```

### 3. Firewall Rule Direction
The above data includes the answer for this part as well. i.e. the direction of the firewall rule

### 4. Audit Policy Changes
The following command checks the Security.evtx file for audit policy changes:

```powershell
Get-WinEvent -Path "Security.evtx" | 
    Where-Object {
        $_.ID -eq 4719  # System audit policy was changed
    } | 
    Select-Object TimeCreated, ID, Message | 
    Format-List
```

Output:
```
TimeCreated : 3/27/2023 7:50:03 PM
Id : 4719
Message : System audit policy was changed.

Subject:
    Security ID:            S-1-5-18
    Account Name:           DESKTOP-887GK2L$
    Account Domain:         WORKGROUP
    Logon ID:               0x3E7

Audit Policy Change:
    Category:               Object Access
    Subcategory:           Other Object Access Events // this is the answer for this part
    Subcategory GUID:      {0cce9227-69ae-11d9-bed3-505054503030}
    Changes:               Success Added
```

### 5. Scheduled Task Analysis
The following command checks the Security.evtx file for a created scheduled task:

```powershell
Get-WinEvent -Path "Security.evtx" | Where-Object {
    $_.ID -eq 4698  # Scheduled task created
} | Select-Object TimeCreated, ID, Message | Format-List
```

Output:
```
TimeCreated : 3/27/2023 7:51:21 PM
Id          : 4698
Message     : A scheduled task was created.

Subject:
    Security ID   : S-1-5-21-3393683511-3463148672-371912004-1001
    Account Name  : CyberJunkie
    Account Domain: DESKTOP-887GK2L
    Logon ID      : 0x25F28

Task Information:
    Task Name   : \HTB-AUTOMATION // this is the answer for this part
    Task Content: 
    <?xml version="1.0" encoding="UTF-16"?>
    <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
        <RegistrationInfo>
            <Date>2023-03-27T07:51:21.4599985</Date>
            <Author>DESKTOP-887GK2L\CyberJunkie</Author>
            <Description>practice</Description>
            <URI>\HTB-AUTOMATION</URI>
        </RegistrationInfo>
        <Triggers>
            <CalendarTrigger>
                <StartBoundary>2023-03-27T09:00:00</StartBoundary>
                <Enabled>true</Enabled>
                <ScheduleByDay>
                    <DaysInterval>1</DaysInterval>
                </ScheduleByDay>
            </CalendarTrigger>
        </Triggers>
        <Principals>
            <Principal id="Author">
                <RunLevel>LeastPrivilege</RunLevel>
                <UserId>DESKTOP-887GK2L\CyberJunkie</UserId>
                <LogonType>InteractiveToken</LogonType>
            </Principal>
        </Principals>
        <Settings>
            <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
            <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
            <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
            <AllowHardTerminate>true</AllowHardTerminate>
            <StartWhenAvailable>false</StartWhenAvailable>
            <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
            <IdleSettings>
                <Duration>PT10M</Duration>
                <WaitTimeout>PT1H</WaitTimeout>
                <StopOnIdleEnd>true</StopOnIdleEnd>
                <RestartOnIdle>false</RestartOnIdle>
            </IdleSettings>
            <AllowStartOnDemand>true</AllowStartOnDemand>
            <Enabled>true</Enabled>
            <Hidden>false</Hidden>
            <RunOnlyIfIdle>false</RunOnlyIfIdle>
            <WakeToRun>false</WakeToRun>
            <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
            <Priority>7</Priority>
        </Settings>
        <Actions Context="Author">
            <Exec>
                <Command>C:\Users\CyberJunkie\Desktop\Automation-HTB.ps1</Command> // this is the answer for the next part
                <Arguments>-A cyberjunkie@hackthebox.eu</Arguments> // this is the answer for the next to next part
            </Exec>
        </Actions>
    </Task>

Other Information:
    ProcessCreationTime: 4222124650660162
    ClientProcessId    : 9320
    ParentProcessId    : 6112
    FQDN               : 0
```

### 6. Scheduled Task File Path
The above data includes the answer for this part as well. i.e. the full path of the file which was scheduled for the task

### 7. Scheduled Task Arguments
The above data includes the answer for this part as well. i.e. the arguments that were passed to the scheduled task

### 8. Windows Defender Analysis
Get the most recent malware detection from Windows Defender:

```powershell
Get-WinEvent -Path "Windows Defender-Operational.evtx" | Where-Object {
    $_.ID -eq 1116 -or  # Malware detected
    $_.ID -eq 1117      # Malware action taken
} | Select-Object TimeCreated, ID, Message | Sort-Object TimeCreated -Descending | Select-Object -First 1 | Format-List
```

Output:
```
TimeCreated : 3/27/2023 7:42:48 PM
Id          : 1117
Message     : Microsoft Defender Antivirus has taken action to protect this machine from malware or other potentially unwanted software.
              For more information please see the following:
              https://go.microsoft.com/fwlink/?linkid=37020&name=HackTool:MSIL/SharpHound!MSR&threatid=2147814944&enterprise=0
Name        : HackTool:MSIL/SharpHound!MSR // this is the answer for this part (Sharphound)
ID          : 2147814944
Severity    : High
Category    : Tool
Path        : containerfile:\_C:\Users\CyberJunkie\Downloads\SharpHound-v1.1.0.zip; // this is the answer for the next part
              file:\_C:\Users\CyberJunkie\Downloads\SharpHound-v1.1.0.zip->SharpHound.exe;
              webfile:\_C:\Users\CyberJunkie\Downloads\SharpHound-v1.1.0.zip|https://objects.githubusercontent.com/github-production-release-asset-2e65be/385323486/70d776cc-8f83-44d5-b226-2dccc4f7c1e3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A4.18.2302.7F202303274.18.2302.7Fus-east-14.18.2302.7Fs34.18.2302.7Faws4_request&X-Amz-Date=20230327T144228Z&X-Amz-Expires=300&X-Amz-Signature=f969ef5ca3eec150dc1e23623434adc1e4a444ba026423c32edf5e85d881a771&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=385323486&response-content-disposition=attachment{0EBC4BEA-5532-4EFB-8A34-64F91CC8702E}BDESKTOP-887GK2L\CyberJunkiefilename{0EBC4BEA-5532-4EFB-8A34-64F91CC8702E}DSharpHound-v1.1.0.zip&response-content-type=application4.18.2302.7Foctet-stream|pid:3532,ProcessStart:133244017530289775
Detection Origin : Internet
Detection Type   : Concrete
Detection Source : Downloads and attachments
User             : NT AUTHORITY\SYSTEM
Process Name     : Unknown
Action           : Quarantine // this is the answer for the next to next part
Action Status    : No additional actions required
Error Code       : 0x80508023
Error description: The program could not find the malware and other potentially unwanted software on this device.
Security intelligence Version: AV: 1.385.1261.0, AS: 1.385.1261.0, NIS: 1.385.1261.0
Engine Version   : AM: 1.1.20100.6, NIS: 1.1.20100.6
```

### 9. Malware Path
The above data includes the answer for this part as well. i.e. the path of the malware that was detected

### 10. Antivirus Action
The above data includes the answer for this part as well. i.e. the action that was taken by the antivirus

### 11. PowerShell Command Analysis
Retrieve PowerShell commands with ID 4104 to identify the command executed by the user:

```powershell
Get-WinEvent -Path "Powershell-Operational.evtx" -MaxEvents 20 | Where-Object {
    $_.ID -eq 4104  # Script block logging only
} | Select-Object TimeCreated, ID, Message | Format-List
```

Output:
```
TimeCreated : 3/27/2023 7:58:33 PM
Id          : 4104
Message     : Creating Scriptblock text (1 of 1):
              prompt
              ScriptBlock ID: 040e087a-07e5-40ca-a7c9-f3e760d6f6c6
              Path:

TimeCreated : 3/27/2023 7:58:33 PM
Id          : 4104
Message     : Creating Scriptblock text (1 of 1):
              Get-FileHash -Algorithm md5 .\Desktop\Automation-HTB.ps1 // this is the answer for this part
              ScriptBlock ID: b4fcf72f-abdc-4a84-923f-8e06a758000b
              Path:

TimeCreated : 3/27/2023 7:58:07 PM
Id          : 4104
Message     : Creating Scriptblock text (1 of 1):
              prompt
              ScriptBlock ID: daafd82b-8566-444f-b5e8-7d29072f96dc
              Path:
```

### 12. System Event Log Analysis
In the System.evtx file, find the event with ID 104.
This is for Source: EventLog, Task Category: Log Clear.
We can see two files here: Microsoft-Windows-Sysmon/Operational, and Microsoft-Windows-Windows Firewall With Advanced Security/Firewall.
The first one is frequently there for many events, and the second one is only for firewall events.
