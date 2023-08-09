exports.workload = async (event) => {
  // START FUNCTION
  const { v4: uuidv4 } = require('uuid');
  var Client = require('ftp');
  const fileSizes = [256000, 512000, 768000, 1024000];
  const fileSize = fileSizes[~~(Math.random() * 4)];
  const data = []
  for (let i = 0; i < fileSize; i++) {
    data.push(~~(Math.random() * 256));
  }
  var c = new Client();
  c.on('ready', function() {
    c.put(Buffer.from(data), 'files/' + uuidv4(), function(err) {
      if (err) throw err;
      c.end();
    });
  });
  c.connect({
    host:"localhost", 
    user:"ftpuser", 
    password:"ftpuser"
  });
  // END FUNCTION
}