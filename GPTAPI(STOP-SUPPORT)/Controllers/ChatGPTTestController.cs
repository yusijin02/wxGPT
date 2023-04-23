using System.IO;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace MyNamespace
{
    [ApiController]
    [Route("api/[controller]")]
    public class ChatGPTTestController : ControllerBase
    {
        private readonly string _openaiApiKey;

        public ChatGPTTestController()
        {
            /**********************随意盗用将被追究法律责任************************/
            //_openaiApiKey = "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";
            _openaiApiKey = "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";
            /**********************随意盗用将被追究法律责任************************/
        }

        [HttpGet]
        public async Task<string> Get()
        {
            var res = await CallOpenAPI();
            return res;
        }



        private async Task<string> CallOpenAPI()
        {

            HttpClientHandler clientHandler = new HttpClientHandler();
            clientHandler.ServerCertificateCustomValidationCallback = (sender, cert, chain, sslPolicyErrors) => { return true; };

            // Pass the handler to httpclient(from you are calling api)
            HttpClient client = new HttpClient(clientHandler);

            var requestUri = "https://api.openai.com/v1/engines/davinci-codex/completions";
            var prompt = "Please introduce yourself";
            var apiKey = "your-api-key"; // Replace with your own API key



            var requestBody = new StringContent($"{{\"prompt\": \"{prompt}\", \"max_tokens\": 5}}");
            requestBody.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/json");
            client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", apiKey);

            var response = await client.PostAsync(requestUri, requestBody);
            var responseBody = await response.Content.ReadAsStringAsync();

            return responseBody;
        }


    }
}
