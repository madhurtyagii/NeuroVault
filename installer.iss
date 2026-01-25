; NeuroVault Installer Script for Inno Setup
; Compile with Inno Setup Compiler: https://jrsoftware.org/isdl.php

[Setup]
AppName=NeuroVault
AppVersion=4.0.0
AppVerName=NeuroVault 4.0
AppPublisher=Madhur Tyagi
AppPublisherURL=https://github.com/madhurtyagii/NeuroVault
AppSupportURL=https://github.com/madhurtyagii/NeuroVault/issues
AppUpdatesURL=https://github.com/madhurtyagii/NeuroVault/releases
DefaultDirName={autopf}\NeuroVault
DefaultGroupName=NeuroVault
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installers
OutputBaseFilename=NeuroVault-v4.0-Setup
Compression=lzma2/ultra64
SolidCompression=yes
SetupIconFile=assets\logo.ico
UninstallDisplayIcon={app}\NeuroVault.exe
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\NeuroVault.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\NeuroVault"; Filename: "{app}\NeuroVault.exe"; Comment: "AI-Powered Second Brain"
Name: "{group}\{cm:ProgramOnTheWeb,NeuroVault}"; Filename: "https://github.com/madhurtyagii/NeuroVault"
Name: "{group}\{cm:UninstallProgram,NeuroVault}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\NeuroVault"; Filename: "{app}\NeuroVault.exe"; Tasks: desktopicon; Comment: "AI-Powered Second Brain"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\NeuroVault"; Filename: "{app}\NeuroVault.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\NeuroVault.exe"; Description: "{cm:LaunchProgram,NeuroVault}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
