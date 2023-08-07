const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  if(req.method === 'PUT'){
    let body = '';

    req.on('data', (chunk) => {
      body += chunk;
    });

    req.on('end', () => {
      const obj = JSON.parse(body);
      if(obj['todo'] == "HoleLogdaten"){
	 let rawdata = fs.readFileSync('./log.json');
	 res.writeHead(200, { 'Content-Type': 'application/json' });
         res.end(rawdata);
      }else if (obj['todo'] == "HoleMail"){
	 let rawdata = fs.readFileSync('./mails.json');
         res.writeHead(200, { 'Content-Type': 'application/json' });
         res.end(rawdata);
      }else if (obj['todo'] == "AddMail"){
         let rawdata = fs.readFileSync('./mails.json');
	 newData = JSON.parse(rawdata);
	 newData['mail'].push(obj['Mail']);
	 rawData = JSON.stringify(newData);
	 fs.writeFileSync("./mails.json", rawData);
	 res.writeHead(200, { 'Content-Type': 'application/json' });
         res.end("OK");
      }else if (obj['todo'] == "RemoveMail"){
         let rawdata = fs.readFileSync('./mails.json');
         newData = JSON.parse(rawdata);
         newData['mail'].splice(obj['index'],1);
         rawData = JSON.stringify(newData);
         fs.writeFileSync("./mails.json", rawData);
         res.writeHead(200, { 'Content-Type': 'application/json' });
         res.end("OK");
      }


    });
}else{


  // Get the file path of the requested resource
  const filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);

  // Check if the requested file exists
  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      // If the file does not exist, return a 404 Not Found response
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    } else {
      // If the file exists, read and serve it
      fs.readFile(filePath, (err, content) => {
        if (err) {
          // If there's an error reading the file, return a 500 Internal Server Error response
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('500 Internal Server Error');
        } else {
          // Determine the content type based on the file extension
          const ext = path.extname(filePath);
          let contentType = 'text/html';

          switch (ext) {
            case '.js':
              contentType = 'text/javascript';
              break;
            case '.css':
              contentType = 'text/css';
              break;
            case '.json':
              contentType = 'application/json';
              break;
          }

          // Set the content type in the response header
          res.writeHead(200, { 'Content-Type': contentType });

          // Serve the file content
          res.end(content);
        }
      });
    }
  });
}
});

// Start the server and listen on port 3000 (you can change the port if needed)
const port = 3000;
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
