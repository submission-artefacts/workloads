exports.workload = async (event) => {
  // START FUNCTION
  var Client = require('ftp');
  var fs = require('fs');

  const fileId = ~~(Math.random() * 4);
  const files = ["100mb", "50mb", "10mb", "5mb"]
  var c = new Client();
  c.on('ready', function() {
    c.get('files/file/' + files[fileId], function(err, stream) {
      if (err) throw err;
      stream.once('close', function() { c.end(); });
      stream.pipe(fs.createWriteStream(files[fileId]));
    });
  });
  c.connect({
    host:"localhost", 
    user:"ftpuser", 
    password:"ftpuser"
  });
  // END FUNCTION
}