const http = require('http');
const fs = require('fs');
const path = require('path');

const GATEWAY_URL = 'http://127.0.0.1:18789';
const AUTH_TOKEN = 'd393c3ce17a9add5233ef964e262bf271edd3167dc9ad790';
const PORT = 8888;

const server = http.createServer(async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // Proxy API calls to gateway
  if (req.url === '/api/chat' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const { message } = JSON.parse(body);
        
        const response = await fetch(`${GATEWAY_URL}/tools/invoke`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${AUTH_TOKEN}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            tool: 'sessions_send',
            args: {
              message: message,
              label: 'voice-chat',
              timeoutSeconds: 120
            }
          })
        });
        
        const data = await response.json();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        
        if (data.ok && data.result) {
          // Extract the reply text from the response
          let reply = '';
          
          // Handle nested content structure
          if (data.result.content) {
            for (const item of data.result.content) {
              if (item.type === 'text') {
                // The text might be JSON with a reply field
                try {
                  const parsed = JSON.parse(item.text);
                  if (parsed.reply) {
                    reply = parsed.reply;
                    break;
                  }
                } catch {
                  reply += item.text;
                }
              }
            }
          }
          
          // Direct reply field
          if (!reply && data.result.reply) {
            reply = data.result.reply;
          }
          
          // Details might have reply
          if (!reply && data.result.details?.reply) {
            reply = data.result.details.reply;
          }
          
          if (!reply) {
            reply = "I received your message but couldn't parse the response.";
          }
          
          res.end(JSON.stringify({ ok: true, reply }));
        } else {
          res.end(JSON.stringify({ ok: false, error: data.error?.message || 'Unknown error' }));
        }
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: error.message }));
      }
    });
    return;
  }
  
  // Serve static files
  let filePath = req.url === '/' ? '/index.html' : req.url;
  filePath = path.join(__dirname, filePath);
  
  const extname = path.extname(filePath);
  const contentTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json'
  };
  
  try {
    const content = fs.readFileSync(filePath);
    res.writeHead(200, { 'Content-Type': contentTypes[extname] || 'text/plain' });
    res.end(content);
  } catch (e) {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(PORT, () => {
  console.log(`Voice chat server running at http://localhost:${PORT}`);
});
