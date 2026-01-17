; =====================================================
; FILE: reelect_baits_giant.ahk
; =====================================================
#NoEnv
#Warn
SendMode Input
SetWorkingDir %A_ScriptDir%

Sleep, 250

MouseMove, 850, 935, 10
Sleep, 100

MouseMove, 851, 936, 2
Sleep, 30
MouseMove, 850, 935, 2
Sleep, 30
MouseMove, 849, 934, 2
Sleep, 30
MouseMove, 850, 935, 2
Sleep, 100

Click, 850, 935
Sleep, 250

; Move mouse to center
SysGet, ScreenWidth, 78
SysGet, ScreenHeight, 79
CenterX := ScreenWidth // 2
CenterY := ScreenHeight // 2
MouseMove, %centerX%, %centerY%, 10
Sleep, 100
MouseMove, % centerX + 1, % centerY + 1, 2
Sleep, 30
MouseMove, %centerX%, %centerY%, 2
Sleep, 30
MouseMove, % centerX - 1, % centerY - 1, 2
Sleep, 30
MouseMove, %centerX%, %centerY%, 2
Sleep, 100

ExitApp