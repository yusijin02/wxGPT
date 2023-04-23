using System;
using System.Security.Cryptography;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using RestSharp;

namespace MyNamespace
{
    [ApiController]
    [Route("api/[controller]")]
    public class ChatGPTController : ControllerBase
    {
        private readonly string _openaiApiKey;

        public ChatGPTController()
        {
            /**********************随意盗用将被追究法律责任************************/
            _openaiApiKey = "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";
            /**********************随意盗用将被追究法律责任************************/
        }

        [HttpGet]
        public ActionResult<string> Get(string prompt, string model, string myToken, string t)
        {
            // 验证 Token 和时间戳
            if (!VerifyToken(myToken, t))
            {
                return StatusCode(403);
            }

            // 验证时间戳是否在10分钟以内
            DateTime timestamp;
            if (!DateTime.TryParseExact(t, "yyyyMMddHHmmss", System.Globalization.CultureInfo.InvariantCulture, System.Globalization.DateTimeStyles.None, out timestamp))
            {
                return StatusCode(405);
            }

            TimeSpan diff = DateTime.Now - timestamp;
            if (diff.TotalMinutes > 10 || diff.TotalMinutes < -10)
            {
                return StatusCode(405);
            }

            // 调用 OpenAI API
            RestClient client = new RestClient("https://api.openai.com/v1");
            RestRequest request = new RestRequest("/engines/" + model + "/completions", Method.POST);
            request.AddHeader("Content-Type", "application/json");
            request.AddHeader("Authorization", "Bearer " + _openaiApiKey);
            request.AddJsonBody(new { prompt = prompt, max_tokens = 50 });

            IRestResponse response = client.Execute(request);
            if (response.StatusCode != System.Net.HttpStatusCode.OK)
            {
                return StatusCode(500);
            }

            // 返回结果
            return response.Content;
        }

        private bool VerifyToken(string myToken, string timestamp)
        {
            // 从文件中读取 myApiKey
            string myApiKey = "yusijin-i2J9bRXFTZcXUmxfT3BlbkFJbDwC2OMLMGstbcOkRPkRPwXUmxfT3BlbkFJbDwCSDDPE";

            // 计算哈希值
            string toBeHashed = myApiKey + timestamp;
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(toBeHashed));
                string hash = BitConverter.ToString(hashBytes).Replace("-", "").ToLower();

                return hash == myToken;
            }
        }
    }
}
