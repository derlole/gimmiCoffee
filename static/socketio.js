function gebId(id) {
    return document.getElementById(id);
}

const socket = io();
    
socket.on('static_data', (data) => {
    console.log(data); 
    console.log("1");
    gebId("beans-fill").innerText = data.beans.fill + "%"
    gebId("water-fill").innerText = data.water.fill + "%"
    gebId("beans-filled").innerText = data.beans.refilled
    gebId("water-filled").innerText = data.water.refilled
    gebId("ip_global").innerText = data.esp_conn_infos.ip_global
    gebId("ip_local").innerText = data.esp_conn_infos.ip_local
    gebId("valid_connection").innerText = data.esp_conn_infos.connection_valid
    gebId("last_seen").innerText = data.esp_conn_infos.last_seen
    switch (data.machine.state) {
        case "ON":
            gebId("machine-status").innerText = "AN";        
            gebId("machine-status-butt").classList.remove("blink-orange");
            gebId("machine-status-butt").classList.remove("initBackRed");
            gebId("machine-status-butt").classList.add("initBackGreen");
            break;
        case "PENDING":
            gebId("machine-status").innerText = "WARTEN";
            gebId("machine-status-butt").classList.add("blink-orange");
            gebId("machine-status-butt").classList.remove("initBackRed");
            gebId("machine-status-butt").classList.remove("initBackGreen");
            break;
        case "OFF":
            gebId("machine-status").innerText = "AUS";        
            gebId("machine-status-butt").classList.remove("blink-orange");
            gebId("machine-status-butt").classList.add("initBackRed");
            gebId("machine-status-butt").classList.remove("initBackGreen");
            break;
    
        default:
            gebId("machine-status").innerText = "UNBEKANNT";
            gebId("machine-status-butt").classList.add("initBackRed");
    }
    if (data.water.fill < 20) {
        gebId("water-fill").parentElement.classList.add("blink-orange");
    }else {
        gebId("water-fill").parentElement.classList.remove("blink-orange");
    }
    if (data.beans.fill < 20) {
        gebId("beans-fill").parentElement.classList.add("blink-orange");
    }else {
        gebId("beans-fill").parentElement.classList.remove("blink-orange");
    }
    if (data.esp_conn_infos.connection_valid) {
        gebId("validButt").classList.add("deniePress");
        gebId("infoMain").classList.remove("blink-orange");
        gebId("machine-status-butt").classList.remove("deniePress");
    }else {
        gebId("validButt").classList.remove("deniePress");
        gebId("infoMain").classList.add("blink-orange");
        gebId("machine-status-butt").classList.add("deniePress");
    }
    if(data.machine.berror){
        gebId("machine-error-butt").classList.add("initBackRed"); 
        gebId("machiene-error-text").innerText = machine.error;
    }
    else {
        gebId("machine-error-butt").classList.remove("initBackRed"); 
        gebId("machiene-error-text").innerText = "";
    }
    machienReady = gebId("machine-ready-butt")
    makeCoffee = gebId("make-coffee-butt")
    if(data.machine.ready && data.machine.state == "ON" && !data.machine.berror && data.esp_conn_infos.connection_valid){
        makeCoffee.classList.remove("deniePress");
    }else {
        makeCoffee.classList.add("deniePress");
    }
    if(data.machine.ready){
        machienReady.classList.add("initBackRed");
        machienReady.classList.remove("initBackGreen");
        gebId("machiene-ready-text").innerText = "Bereit";
    }else {
        machienReady.classList.remove("initBackRed");
        machienReady.classList.add("initBackGreen");
        gebId("machiene-ready-text").innerText = "Nicht bereit";
    }
});
