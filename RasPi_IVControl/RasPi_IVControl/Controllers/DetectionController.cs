using Microsoft.AspNetCore.Mvc;
using RasPi_IVControl.Models;

namespace RasPi_IVControl.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DetectionController : ControllerBase
    {
        private static readonly List<DetectionResult> DetectionResults = new List<DetectionResult>();

        [HttpPost]
        public IActionResult Post([FromBody] DetectionResult result)
        {
            DetectionResults.Add(result);
            return Ok();
        }

        [HttpGet]
        public ActionResult<IEnumerable<DetectionResult>> Get()
        {
            return DetectionResults;
        }
    }
}
