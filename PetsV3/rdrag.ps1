Add-Type @"
using System; using System.Runtime.InteropServices;
public class M {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetCursorPos(out POINT p);
  public struct POINT { public int X; public int Y; }
}
"@
[M]::SetProcessDPIAware() | Out-Null
$p = Get-Process | Where-Object { $_.MainWindowTitle -like "*Roblox Studio*" } | Select-Object -First 1
if ($p) { [M]::SetForegroundWindow($p.MainWindowHandle) | Out-Null; "studio window: " + $p.MainWindowTitle }
Start-Sleep -Milliseconds 400
[M]::SetCursorPos(880, 480) | Out-Null
Start-Sleep -Milliseconds 150
$RDOWN=0x0008; $RUP=0x0010; $MOVE=0x0001
[M]::mouse_event($RDOWN, 0, 0, 0, [IntPtr]::Zero)
Start-Sleep -Milliseconds 120
$log = @()
for ($i = 0; $i -lt 40; $i++) {
  [M]::mouse_event($MOVE, 8, 0, 0, [IntPtr]::Zero)
  Start-Sleep -Milliseconds 15
  $pt = New-Object M+POINT; [M]::GetCursorPos([ref]$pt) | Out-Null
  if ($i % 8 -eq 0) { $log += "move $i cursor=($($pt.X),$($pt.Y))" }
}
Start-Sleep -Milliseconds 100
[M]::mouse_event($RUP, 0, 0, 0, [IntPtr]::Zero)
$log
"done"
