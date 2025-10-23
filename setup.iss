[Setup]
AppName=Speed Reader
AppVersion=1.0.0
AppPublisher=Speed Reader Team
AppPublisherURL=https://github.com/yourusername/open-speed-reader
AppSupportURL=https://github.com/yourusername/open-speed-reader/issues
AppUpdatesURL=https://github.com/yourusername/open-speed-reader/releases
DefaultDirName={autopf}\SpeedReader
DefaultGroupName=Speed Reader
AllowNoIcons=yes
LicenseFile=LICENSE.md
OutputDir=installer
OutputBaseFilename=SpeedReader_Setup_v1.0.0
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\SpeedReader.exe
UninstallDisplayName=Speed Reader
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Speed Reader Team
VersionInfoDescription=A PyQt6-based desktop application for speed reading PDF and EPUB documents
VersionInfoCopyright=Copyright (C) 2024 Speed Reader Team

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\SpeedReader.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Speed Reader"; Filename: "{app}\SpeedReader.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\{cm:UninstallProgram,Speed Reader}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Speed Reader"; Filename: "{app}\SpeedReader.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Speed Reader"; Filename: "{app}\SpeedReader.exe"; IconFilename: "{app}\icon.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\SpeedReader.exe"; Description: "{cm:LaunchProgram,Speed Reader}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\progress.json"
Type: filesandordirs; Name: "{app}\*.log"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // Check if the application is already running
  if CheckForMutexes('SpeedReaderMutex') then
  begin
    if MsgBox('Speed Reader is currently running. Please close it before continuing with the installation.', mbConfirmation, MB_YESNO) = IDNO then
      Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create progress.json file if it doesn't exist
    if not FileExists(ExpandConstant('{app}\progress.json')) then
    begin
      SaveStringToFile(ExpandConstant('{app}\progress.json'), '{}', False);
    end;
  end;
end;
