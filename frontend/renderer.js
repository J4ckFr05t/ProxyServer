const {PythonShell} =require('python-shell');

document.getElementById("search").addEventListener("click", function() {
          
    var filename = document.getElementById("filein").value;
    let options = {
      mode: 'text',
      pythonPath: 'python3',
      pythonOptions: ['-u'],
      scriptPath: './',
      args: [filename]
    };

    PythonShell.run('hello.py', options, function(err,results){
      if (err) throw err;
      alert(results);
    });
});