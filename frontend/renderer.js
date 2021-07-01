const { PythonShell } = require('python-shell');

document.getElementById("search").addEventListener("click", function() {

    var filename = document.getElementById("filein").value;
    // alert(filename)
    let options = {
        mode: 'text',
        pythonPath: 'python',
        pythonOptions: ['-u'],
        scriptPath: './',
        args: [filename]
    };
    // url = 'C://Users/91974/Desktop/Projects/ProxyServer/frontend/child.html?name=' + encodeURIComponent(filename);

    // document.location.href = filename;
    PythonShell.run('one_way_client.py', options, function(err, results) {
        if (err) throw err;
        // alert(results)
        url = 'C://Users/91974/Desktop/Projects/ProxyServer/frontend/child.html?name=' + encodeURIComponent(results);
        document.location.href = url;
    });
    // alert(filename)
});