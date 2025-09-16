import express from 'express';
import axios from 'axios';
import morgan from 'morgan';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || 3050;
const ANTHROPIC_API_URL = 'https://api.anthropic.com';

app.use(express.raw({ type: '*/*', limit: '50mb' }));
app.use(morgan('dev'));

function getLogFileName(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day}-${hours}-${minutes}-${seconds}-proxy-logs.txt`;
}

async function logRequestResponse(
  method: string,
  url: string,
  headers: any,
  requestBody: any,
  responseStatus: number,
  responseHeaders: any,
  responseBody: any
) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    request: {
      method,
      url,
      headers,
      body: requestBody
    },
    response: {
      status: responseStatus,
      headers: responseHeaders,
      body: responseBody
    }
  };

  const logDir = path.join(__dirname, '..', 'logs');
  await fs.mkdir(logDir, { recursive: true });

  const logFile = path.join(logDir, getLogFileName());
  await fs.appendFile(logFile, JSON.stringify(logEntry, null, 2) + '\n');
}

app.use(async (req, res) => {
  const targetUrl = `${ANTHROPIC_API_URL}${req.originalUrl}`;

  try {
    let requestBody: any;
    if (req.body && Buffer.isBuffer(req.body)) {
      const bodyStr = req.body.toString('utf-8');
      try {
        requestBody = JSON.parse(bodyStr);
      } catch {
        requestBody = bodyStr;
      }
    }

    const requestHeaders = { ...req.headers };
    delete requestHeaders['host'];
    delete requestHeaders['content-length'];

    console.log(`Proxying ${req.method} ${req.originalUrl} -> ${targetUrl}`);

    const response = await axios({
      method: req.method as any,
      url: targetUrl,
      headers: requestHeaders,
      data: req.body,
      responseType: 'arraybuffer',
      validateStatus: () => true,
      decompress: true,
      maxBodyLength: Infinity,
      maxContentLength: Infinity
    });

    let responseBody: any;
    const responseBuffer = Buffer.from(response.data);
    const responseStr = responseBuffer.toString('utf-8');
    try {
      responseBody = JSON.parse(responseStr);
    } catch {
      responseBody = responseStr;
    }

    await logRequestResponse(
      req.method,
      targetUrl,
      requestHeaders,
      requestBody,
      response.status,
      response.headers,
      responseBody
    );

    Object.entries(response.headers).forEach(([key, value]) => {
      if (key.toLowerCase() !== 'content-encoding' &&
          key.toLowerCase() !== 'transfer-encoding') {
        res.setHeader(key, value as string);
      }
    });

    res.status(response.status).send(response.data);
  } catch (error) {
    console.error('Proxy error:', error);

    const errorResponse = {
      error: 'Proxy error',
      message: error instanceof Error ? error.message : 'Unknown error'
    };

    await logRequestResponse(
      req.method,
      targetUrl,
      req.headers,
      req.body,
      500,
      {},
      errorResponse
    );

    res.status(500).json(errorResponse);
  }
});

app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}`);
  console.log(`Forwarding requests to ${ANTHROPIC_API_URL}`);
  console.log(`Logs will be written to logs/YYYY-MM-DD-HH-MM-SS-proxy-logs.txt`);
});