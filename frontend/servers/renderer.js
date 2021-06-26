const { exec } = require("child_process");

server = "false"
proxy = "false"

document.getElementById("bserver").addEventListener("click", function() {

    if(server == "false"){
      server = "true"
      exec("python3 server.py")
    }
    else if(server == "true"){
      server = "false"
      exec("python3 stop_server.py")
    }
    
});


document.getElementById("bproxy").addEventListener("click", function() {

    if(proxy == "false"){
      proxy = "true"
      exec("python3 proxy.py")
      
    }
    else if(proxy == "true"){
      proxy = "false"
      exec("python3 stop_proxy.py")
      
    }

    
});
