Unicode True
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"

!define PRODUCT_NAME "Doclira PDF Lite"
!define PRODUCT_VERSION "0.1.0"
!define PRODUCT_PUBLISHER "Doclira"
!define PRODUCT_EXE "DocliraPDFLite.exe"
!define UNINSTALL_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\DocliraPDFLite"

Name "${PRODUCT_NAME}"
OutFile "..\release_build\DocliraPDF_Lite_Setup_v${PRODUCT_VERSION}_Windows_x64.exe"
InstallDir "$LocalAppData\Programs\Doclira PDF Lite"
InstallDirRegKey HKCU "Software\Doclira\Doclira PDF Lite" "InstallDir"
RequestExecutionLevel user
SetCompressor /SOLID lzma
BrandingText "Doclira PDF Lite"
Icon "..\assets\doclira_lite.ico"
UninstallIcon "..\assets\doclira_lite.ico"

VIProductVersion "0.1.0.0"
VIAddVersionKey /LANG=1033 "ProductName" "${PRODUCT_NAME}"
VIAddVersionKey /LANG=1033 "ProductVersion" "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=1033 "FileVersion" "${PRODUCT_VERSION}"
VIAddVersionKey /LANG=1033 "CompanyName" "${PRODUCT_PUBLISHER}"
VIAddVersionKey /LANG=1033 "FileDescription" "${PRODUCT_NAME} Installer"
VIAddVersionKey /LANG=1033 "LegalCopyright" "Copyright (c) 2026 Doclira"

!define MUI_ABORTWARNING
!define MUI_FINISHPAGE_RUN "$INSTDIR\${PRODUCT_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Doclira PDF Lite"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Function .onInit
  ${IfNot} ${RunningX64}
    MessageBox MB_ICONSTOP "Doclira PDF Lite requires 64-bit Windows 10 or Windows 11."
    Abort
  ${EndIf}
FunctionEnd

Section "Doclira PDF Lite (required)" SecMain
  SectionIn RO
  SetOutPath "$INSTDIR"
  File "..\dist\${PRODUCT_EXE}"
  File "Readme.txt"

  WriteUninstaller "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Doclira\Doclira PDF Lite" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "DisplayIcon" "$INSTDIR\${PRODUCT_EXE}"
  WriteRegStr HKCU "${UNINSTALL_KEY}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
  WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINSTALL_KEY}" "NoRepair" 1

  CreateDirectory "$SMPROGRAMS\Doclira PDF Lite"
  CreateShortcut "$SMPROGRAMS\Doclira PDF Lite\Doclira PDF Lite.lnk" "$INSTDIR\${PRODUCT_EXE}"
  CreateShortcut "$SMPROGRAMS\Doclira PDF Lite\Uninstall Doclira PDF Lite.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section /o "Desktop shortcut" SecDesktop
  CreateShortcut "$DESKTOP\Doclira PDF Lite.lnk" "$INSTDIR\${PRODUCT_EXE}"
SectionEnd

LangString DESC_SecMain ${LANG_ENGLISH} "Install the free Doclira PDF Lite application and uninstaller."
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create a Doclira PDF Lite shortcut on the desktop."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Section "Uninstall"
  Delete "$DESKTOP\Doclira PDF Lite.lnk"
  Delete "$SMPROGRAMS\Doclira PDF Lite\Doclira PDF Lite.lnk"
  Delete "$SMPROGRAMS\Doclira PDF Lite\Uninstall Doclira PDF Lite.lnk"
  RMDir "$SMPROGRAMS\Doclira PDF Lite"

  Delete "$INSTDIR\${PRODUCT_EXE}"
  Delete "$INSTDIR\Readme.txt"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"

  DeleteRegKey HKCU "${UNINSTALL_KEY}"
  DeleteRegKey HKCU "Software\Doclira\Doclira PDF Lite"
  DeleteRegKey /ifempty HKCU "Software\Doclira"
SectionEnd
