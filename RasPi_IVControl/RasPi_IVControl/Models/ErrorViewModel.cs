namespace RasPi_IVControl.Models
{
    public class ErrorViewModel
    {
        public string? RequestId { get; set; }

        public bool ShowRequestId => !string.IsNullOrEmpty(RequestId);
    }
    public class CarCommand
    {
        public string Command { get; set; }
    }
}
