param([int]$x = 880, [int]$y = 480)
Add-Type @"
using System; using System.Runtime.InteropServices;
public class M {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern bool GetCursorPos(out POINT p);
  [DllImport("user32.dll")] public static extern void keybd_event(byte k, byte s, uint f, IntPtr e);
  public struct POINT { public int X; public int Y; }
}
"@
[M]::SetProcessDPIAware() | Out-Null
[M]::SetCursorPos($x, $y) | Out-Null
Start-Sleep -Milliseconds 150
[M]::mouse_event(0x0008, 0, 0, 0, [IntPtr]::Zero)
Start-Sleep -Milliseconds 100
$pt = New-Object M+POINT
for ($i = 0; $i -lt 10; $i++) { [M]::mouse_event(0x0001, 6, 4, 0, [IntPtr]::Zero); Start-Sleep -Milliseconds 20 }
[M]::GetCursorPos([ref]$pt) | Out-Null
"while right held: cursor=($($pt.X),$($pt.Y)) start=($x,$y)"
[M]::mouse_event(0x0010, 0, 0, 0, [IntPtr]::Zero)
Start-Sleep -Milliseconds 250
[M]::keybd_event(0x1B, 0, 0, [IntPtr]::Zero); [M]::keybd_event(0x1B, 0, 2, [IntPtr]::Zero)
