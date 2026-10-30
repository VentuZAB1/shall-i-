# Lists every Windows audio session (all output devices): process, mute, volume, live peak level. Read-only.
$code = @"
using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Diagnostics;
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorCom {}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
  int EnumAudioEndpoints(int dataFlow, int stateMask, out IMMDeviceCollection devices);
  int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice device);
}
[Guid("0BD7A1BE-7A1A-44DB-8397-CC5392387B5E"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceCollection { int GetCount(out uint n); int Item(uint i, out IMMDevice d); }
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
  int Activate(ref Guid iid, int ctx, IntPtr p, [MarshalAs(UnmanagedType.IUnknown)] out object o);
  int OpenPropertyStore(int access, out IPropertyStore store);
  int GetId([MarshalAs(UnmanagedType.LPWStr)] out string id);
  int GetState(out int state);
}
[Guid("886d8eeb-8cf2-4446-8d02-cdba1dbdcf99"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IPropertyStore { int GetCount(out int c); int GetAt(int i, out PROPERTYKEY k); int GetValue(ref PROPERTYKEY k, out PROPVARIANT v); }
[StructLayout(LayoutKind.Sequential)] struct PROPERTYKEY { public Guid fmtid; public int pid; }
[StructLayout(LayoutKind.Explicit)] struct PROPVARIANT { [FieldOffset(0)] public short vt; [FieldOffset(8)] public IntPtr p; [FieldOffset(16)] public IntPtr p2; }
[Guid("77AA99A0-1BD6-484F-8BC7-2C654C9A9B6F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionManager2 {
  int GetAudioSessionControl(IntPtr a, int b, out IntPtr c);
  int GetSimpleAudioVolume(IntPtr a, int b, out IntPtr c);
  int GetSessionEnumerator(out IAudioSessionEnumerator e);
}
[Guid("E2F5BB11-0570-40CA-ACDD-3AA01277DEE8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionEnumerator { int GetCount(out int n); int GetSession(int i, out IAudioSessionControl2 s); }
[Guid("bfb7ff88-7239-4fc9-8fa2-07c950be9c6d"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioSessionControl2 {
  int GetState(out int s); int GetDisplayName([MarshalAs(UnmanagedType.LPWStr)] out string n); int SetDisplayName(string n, ref Guid g);
  int GetIconPath(out IntPtr p); int SetIconPath(string p, ref Guid g); int GetGroupingParam(out Guid g); int SetGroupingParam(ref Guid a, ref Guid b);
  int RegisterAudioSessionNotification(IntPtr n); int UnregisterAudioSessionNotification(IntPtr n);
  int GetSessionIdentifier([MarshalAs(UnmanagedType.LPWStr)] out string id); int GetSessionInstanceIdentifier([MarshalAs(UnmanagedType.LPWStr)] out string id);
  int GetProcessId(out uint pid);
}
[Guid("87CE5498-68D6-44E5-9215-6DA47EF883D8"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface ISimpleAudioVolume { int SetMasterVolume(float v, ref Guid g); int GetMasterVolume(out float v); int SetMute(bool m, ref Guid g); int GetMute(out bool m); }
[Guid("C02216F6-8C67-4B5B-9D00-D008E73E0064"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioMeterInformation { int GetPeakValue(out float p); }
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
  int RegisterControlChangeNotify(IntPtr p); int UnregisterControlChangeNotify(IntPtr p); int GetChannelCount(out int c);
  int SetMasterVolumeLevel(float l, ref Guid g); int SetMasterVolumeLevelScalar(float l, ref Guid g); int GetMasterVolumeLevel(out float l); int GetMasterVolumeLevelScalar(out float l);
  int SetChannelVolumeLevel(uint c, float l, ref Guid g); int SetChannelVolumeLevelScalar(uint c, float l, ref Guid g); int GetChannelVolumeLevel(uint c, out float l); int GetChannelVolumeLevelScalar(uint c, out float l);
  int SetMute(bool m, ref Guid g); int GetMute(out bool m);
}
public static class Sessions {
  static string Name(IMMDevice d) {
    try { IPropertyStore st; d.OpenPropertyStore(0, out st); var k = new PROPERTYKEY { fmtid = new Guid("a45c254e-df1c-4efd-8020-67d146a850e0"), pid = 14 }; PROPVARIANT v; st.GetValue(ref k, out v); return Marshal.PtrToStringUni(v.p); } catch { return "?"; }
  }
  public static string Run() {
    var sb = new StringBuilder();
    var en = (IMMDeviceEnumerator)(new MMDeviceEnumeratorCom());
    IMMDevice def; en.GetDefaultAudioEndpoint(0, 1, out def); string defId; def.GetId(out defId);
    IMMDeviceCollection col; en.EnumAudioEndpoints(0, 1, out col);
    uint n; col.GetCount(out n);
    for (uint i = 0; i < n; i++) {
      IMMDevice d; col.Item(i, out d); string id; d.GetId(out id);
      Guid ev = typeof(IAudioEndpointVolume).GUID; object evo; d.Activate(ref ev, 23, IntPtr.Zero, out evo);
      var epv = (IAudioEndpointVolume)evo; bool dm; float dv; epv.GetMute(out dm); epv.GetMasterVolumeLevelScalar(out dv);
      sb.AppendLine("DEVICE " + Name(d) + (id == defId ? "  [DEFAULT]" : "") + "  mute=" + dm + " vol=" + dv.ToString("0.00"));
      Guid iid = typeof(IAudioSessionManager2).GUID; object o; d.Activate(ref iid, 23, IntPtr.Zero, out o);
      var mgr = (IAudioSessionManager2)o; IAudioSessionEnumerator se; mgr.GetSessionEnumerator(out se);
      int c; se.GetCount(out c);
      for (int j = 0; j < c; j++) {
        IAudioSessionControl2 s; se.GetSession(j, out s); uint pid; s.GetProcessId(out pid);
        string pn = "?"; try { pn = Process.GetProcessById((int)pid).ProcessName; } catch {}
        var vol = (ISimpleAudioVolume)s; bool m; float v; vol.GetMute(out m); vol.GetMasterVolume(out v);
        var met = (IAudioMeterInformation)s; float pk; met.GetPeakValue(out pk);
        int state; s.GetState(out state);
        sb.AppendLine("   " + pn + " (pid " + pid + ") mute=" + m + " vol=" + v.ToString("0.00") + " peak=" + pk.ToString("0.000") + " state=" + state);
      }
    }
    return sb.ToString();
  }
}
"@
Add-Type -TypeDefinition $code -Language CSharp
[Sessions]::Run()
