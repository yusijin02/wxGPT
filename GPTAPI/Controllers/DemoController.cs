using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace GPTAPI.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class DemoController : ControllerBase
    {
        [HttpGet]
        public string Demo_1()
        {
            return "Test Pass.\nBy Sijin Yu.\n测试通过.\n余思进.";
        }
        [HttpGet]
        public string Demo_2(string userName, string t)
        {
            return "userName=" + userName + "\nt=" + t;
        }
    }
}
