namespace AndroidTests.Models.Emulator;

public class EmulatorSettings
{
    public required string Name { get; set; }
    public required string Path { get; set; } 
    public required string AdbPath { get; set; }
    public required string AppPackage { get; set; }
    public required string TestPhotoPath { get; set; }
}