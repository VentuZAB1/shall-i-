Add-Type @"
using System; using System.Runtime.InteropServices;
public class M {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern bool GetCursorPos(out POINT p);
  [DllImport("user32.dll")] public static extern bool GetClipCursor(out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
  public struct POINT { public int X; public int Y; }
  public struct RECT { public int L; public int T; public int R; public int B; }
}
"@
[M]::SetProcessDPIAware() | Out-Null
$r = New-Object M+RECT; [M]::GetClipCursor([ref]$r) | Out-Null
"clip rect: $($r.L),$($r.T) - $($r.R),$($r.B)"
$sb = New-Object System.Text.StringBuilder 256; [M]::GetWindowText([M]::GetForegroundWindow(), $sb, 256) | Out-Null
"foreground: " + $sb.ToString()
[M]::SetCursorPos(880, 480) | Out-Null
Start-Sleep -Milliseconds 100
for ($i = 0; $i -lt 10; $i++) { [M]::mouse_event(0x0001, 10, 0, 0, [IntPtr]::Zero); Start-Sleep -Milliseconds 20 }
$pt = New-Object M+POINT; [M]::GetCursorPos([ref]$pt) | Out-Null
"after 10x(+10px) relative moves, no button: cursor=($($pt.X),$($pt.Y))  (expect ~980 with accel off)"
[M]::SetCursorPos(1000, 400) | Out-Null
Start-Sleep -Milliseconds 50
[M]::GetCursorPos([ref]$pt) | Out-Null
"after SetCursorPos(1000,400): cursor=($($pt.X),$($pt.Y))"
