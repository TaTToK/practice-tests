using System.Diagnostics;
using AndroidTests.Config;
using AndroidTests.Models.Emulator;
using Microsoft.Extensions.Configuration;
using Serilog;

namespace AndroidTests.Utils;

public class EmulatorManager
{
    private static readonly EmulatorSettings Settings = ConfigManager.Configuration
                                                            .GetSection(nameof(EmulatorSettings))
                                                            .Get<EmulatorSettings>()
                                                        ?? throw new InvalidOperationException("EmulatorSettings not found in config");
    
    public static void Start()
    {
        if (IsEmulatorRunning())
        {
            Log.Information("Emulator is already running.");
            return;
        }
        
        Log.Information("Starting Emulator {AvdName}", Settings.Name);
        
        Process.Start(new ProcessStartInfo
        {
            FileName = Settings.Path,
            Arguments = $"-avd {Settings.Name}",
            UseShellExecute = true
        });

        WaitForBoot();
    }

    private static bool IsEmulatorRunning()
    {
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = Settings.AdbPath,
                Arguments = "devices",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };
        process.Start();
        var output = process.StandardOutput.ReadToEnd();
        process.WaitForExit();
        return output.Contains("emulator-");
    }

    private static void WaitForBoot()
    {
        Log.Information("Waiting for emulator boot");
        while (true)
        {
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = Settings.AdbPath,
                    Arguments = "shell getprop sys.boot_completed",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }
            };
            process.Start();
            var result = process.StandardOutput.ReadToEnd().Trim();
            process.WaitForExit();

            if (result == "1")
            {
                Log.Information("Emulator boot completed");
                break;
            }
            
            Thread.Sleep(2000);
        }
    }

    public static void ClearAppData()
    {
        var packageName = Settings.AppPackage;
        
        RunAdbCommand($"shell pm clear {packageName}");
    }

    private static void RunAdbCommand(string arguments)
    {
        var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = Settings.AdbPath,
                Arguments = arguments,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };
        process.Start();
        process.WaitForExit();
    }

    public static void PushPhoto(string localPath, string devicePath = "/sdcard/Pictures/sharpiki.jpg")
    {
        RunAdbCommand($"push \"{localPath}\" {devicePath}");
        RunAdbCommand($"shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{devicePath}");
        
        Log.Information("Photo pushed to {DevicePath}", devicePath);
    }
}