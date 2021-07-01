const { PythonShell } = require('python-shell');

g = "hai"
window.onload = function() {
    var url = document.location.href,
        params = url.split('?')[1].split('&'),
        data = {},
        tmp;
    alert(params)
    for (var i = 0, l = params.length; i < l; i++) {
        tmp = params[i].split('=');
        data[tmp[0]] = tmp[1];
    }

    document.getElementById('here').innerHTML = data.search;
}


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
    // url = './child.html?name=' + encodeURIComponent(results);

    PythonShell.run('one_way_client.py', options, function(err, results) {
        if (err) throw err;
        window.location.href = "child.html?data=" + results;

    });
});