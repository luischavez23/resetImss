#define MyAppName "ResetIMSS"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Luis Pablo Chávez"

#define SourcePath "..\Release"

[Setup]
AppId={{D0B3D6C7-7E8B-45E3-BB2D-9F0E12A5D111}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\ResetIMSS
DefaultGroupName=ResetIMSS

PrivilegesRequired=admin

OutputDir=Output
OutputBaseFilename=ResetIMSSSetup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\ResetIMSSConfig.exe

SetupIconFile=..\assets\reiniciar.ico



[Files]

Source: "{#SourcePath}\ResetIMSSConfig.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\ResetIMSSCore.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\ResetIMSSService.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourcePath}\ResetIMSSService.xml"; DestDir: "{app}"; Flags: ignoreversion

Source: "{#SourcePath}\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs createallsubdirs ignoreversion



[Icons]

Name: "{group}\ResetIMSS"; Filename: "{app}\ResetIMSSConfig.exe"

Name: "{autodesktop}\ResetIMSS"; Filename: "{app}\ResetIMSSConfig.exe"; Tasks: desktopicon



[Tasks]

Name: desktopicon; Description: "Crear acceso directo en el escritorio"; Flags: unchecked



[Run]

Filename: "{app}\ResetIMSSService.exe"; Parameters: "install"; Flags: runhidden waituntilterminated

Filename: "{app}\ResetIMSSService.exe"; Parameters: "start"; Flags: runhidden waituntilterminated



[UninstallRun]

Filename: "{app}\ResetIMSSService.exe"; Parameters: "stop"; Flags: runhidden waituntilterminated skipifdoesntexist

Filename: "{app}\ResetIMSSService.exe"; Parameters: "uninstall"; Flags: runhidden waituntilterminated skipifdoesntexist