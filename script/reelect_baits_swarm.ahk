; =====================================================
; FILE: reelect_baits_swarm.ahk
; =====================================================
#NoEnv
#Warn
SendMode Input
SetWorkingDir %A_ScriptDir%

Sleep, 250

MouseMove, 850, 905, 10
Sleep, 100

MouseMove, 851, 906, 2
Sleep, 30
MouseMove, 850, 905, 2
Sleep, 30
MouseMove, 849, 904, 2
Sleep, 30
MouseMove, 850, 905, 2
Sleep, 100

Click, 850, 905
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