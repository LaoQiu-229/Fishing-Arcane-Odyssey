import subprocess
import tempfile
import os
import time

class ImageClicker:
    """
    Module to handle clicking with AutoHotkey using temporary scripts.
    Generates AHK scripts on-the-fly with realistic mouse movements.
    """
    
    def __init__(self, ahk_path=None):
        """
        Initialize ImageClicker
        
        Args:
            ahk_path: Path to AutoHotkey.exe. If None, will try default locations.
        """
        self.ahk_path = ahk_path or self._find_ahk()
        
    def _find_ahk(self):
        """Find AutoHotkey installation path"""
        possible_paths = [
            r"C:\Program Files\AutoHotkey\AutoHotkey.exe",
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey.exe",
            r"C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError("AutoHotkey not found. Please install it from https://www.autohotkey.com/")
    
    def _generate_ahk_script(self, x, y, move_to_center=False):
        """
        Generate AHK script content with realistic mouse movements
        
        Args:
            x: X coordinate to click
            y: Y coordinate to click
            move_to_center: Whether to move mouse back to center after clicking
            
        Returns:
            String containing the AHK script
        """
        # Build the center movement part if needed - uses SysGet like swarm.ahk
        center_movement = ""
        if move_to_center:
            center_movement = """
; Move mouse to center
SysGet, ScreenWidth, 78
SysGet, ScreenHeight, 79
CenterX := ScreenWidth // 2
CenterY := ScreenHeight // 2
MouseMove, %CenterX%, %CenterY%, 10
Sleep, 100

; Small jitter movements to look more human
Random, offset1, -1, 1
Random, offset2, -1, 1
newX := CenterX + offset1
newY := CenterY + offset2
MouseMove, %newX%, %newY%, 2
Sleep, 30

MouseMove, %CenterX%, %CenterY%, 2
Sleep, 30

Random, offset3, -1, 1
Random, offset4, -1, 1
newX2 := CenterX + offset3
newY2 := CenterY + offset4
MouseMove, %newX2%, %newY2%, 2
Sleep, 30

MouseMove, %CenterX%, %CenterY%, 2
Sleep, 100
"""
        
        script = f"""#NoEnv
#Warn
SendMode Input
SetWorkingDir %A_ScriptDir%

; Target coordinates
x := {x}
y := {y}

Sleep, 250

; Move to target with slight variations
MouseMove, %x%, %y%, 10
Sleep, 100

; Small jitter movements to look more human
Random, offset1, -1, 1
Random, offset2, -1, 1
newX := x + offset1
newY := y + offset2
MouseMove, %newX%, %newY%, 2
Sleep, 30

MouseMove, %x%, %y%, 2
Sleep, 30

Random, offset3, -1, 1
Random, offset4, -1, 1
newX2 := x + offset3
newY2 := y + offset4
MouseMove, %newX2%, %newY2%, 2
Sleep, 30

MouseMove, %x%, %y%, 2
Sleep, 100

; Click at the target coordinates
Click, %x%, %y%
Sleep, 250
{center_movement}
ExitApp
"""
        return script
    
    def click(self, x, y, move_to_center=True):
        """
        Click at specified coordinates using temporary AHK script and optionally move back to center
        
        Args:
            x: X coordinate to click
            y: Y coordinate to click
            move_to_center: Whether to move mouse back to center after clicking (default: True)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate AHK script content with center movement
            script_content = self._generate_ahk_script(x, y, move_to_center)
            
            # Create temporary AHK file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ahk', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(script_content)
                temp_path = temp_file.name
            
            # Execute the temporary AHK script
            result = subprocess.run(
                [self.ahk_path, temp_path],
                timeout=5,
                capture_output=True
            )
            
            # Clean up temporary file
            time.sleep(0.1)
            try:
                os.unlink(temp_path)
            except:
                pass
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"AHK script timeout for coordinates ({x}, {y})")
            return False
        except Exception as e:
            print(f"Error executing AHK click: {e}")
            return False