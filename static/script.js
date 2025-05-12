function gebId(id) {
    return document.getElementById(id);
}


const water = JSON.parse(document.getElementById("waterData").innerText)
const beans = JSON.parse(document.getElementById("beansData").innerText)
const machine = JSON.parse(document.getElementById("machineData").innerText)
const esp_conn_infos = JSON.parse(document.getElementById("espData").innerText)

// console.log(water)
// console.log(beans)
// console.log(machine)
// console.log(esp_conn_infos)

gebId("beans-fill").innerText = beans.fill + "%"
gebId("water-fill").innerText = water.fill + "%"
gebId("beans-filled").innerText = beans.refilled
gebId("water-filled").innerText = water.refilled
gebId("ip_global").innerText = esp_conn_infos.ip_global
gebId("ip_local").innerText = esp_conn_infos.ip_local
gebId("valid_connection").innerText = esp_conn_infos.connection_valid
gebId("last_seen").innerText = esp_conn_infos.last_seen
machienReady = gebId("machine-ready-butt")
makeCoffee = gebId("make-coffee-butt")
if(machine.status == "OFF"){
    gebId("machine-status").innerText = "AUS";
    gebId("machine-status-butt").classList.add("initBackRed");
}
if(machine.berror){
    gebId("machine-error-butt").classList.add("initBackRed"); 
    gebId("machiene-error-text").innerText = machine.error;
}
if(machine.ready && machine.state == "ON" && !machine.berror && esp_conn_infos.connection_valid){
    makeCoffee.classList.remove("deniePress");
}
if(machine.ready){
    machienReady.classList.remove("initBackRed");
    machienReady.classList.add("initBackGreen");
    gebId("machiene-ready-text").innerText = "Bereit";
}
if (esp_conn_infos.connection_valid) {
    gebId("validButt").classList.add("deniePress");
    gebId("machine-status-butt").classList.remove("deniePress");
}else {
    gebId("infoMain").classList.add("blink-orange");
}
if (water.fill < 20) {
    gebId("water-fill").parentElement.classList.add("blink-orange");
}
if (beans.fill < 20) {
    gebId("beans-fill").parentElement.classList.add("blink-orange");
}
//all there given if generated html manipulations are not else-ed because the else condition is always in the dafult. 
//If later information is changed and should manipulate the html, it will come through socketio.js
stBut = gebId("machine-status-butt")
switch (machine.state) {
    case "ON":
        gebId("machine-status").innerText = "AN";        
        stBut.classList.remove("blink-orange");
        stBut.classList.remove("initBackRed");
        stBut.classList.add("initBackGreen");
        break;
    case "PENDING":
        gebId("machine-status").innerText = "WARTEN";
        stBut.classList.add("blink-orange");
        stBut.classList.remove("initBackRed");
        stBut.classList.remove("initBackGreen");
        break;
    case "OFF":
        gebId("machine-status").innerText = "AUS";        
        stBut.classList.remove("blink-orange");
        stBut.classList.add("initBackRed");
        stBut.classList.remove("initBackGreen");
        break;

    default:
        gebId("machine-status").innerText = "UNBEKANNT";
        stBut.classList.add("initBackRed");
}
// All there
function toggleMachine() {
    if (gebId("machine-status-butt").classList.contains("deniePress")){
        return;
    }
    // console.log("toggleMachine");
    const result = confirm("Möchtest du den Vorgang wirklich ausführen?");
    if (!result) {
        return;
    }
    // console.log("toggleMachine");
    fetch('/unsecure/esp/toggle-machine', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });
}

function waterRefill(){
    if (gebId("water-fill").parentElement.classList.contains("deniePress")){
        return;
    }
    console.log(water)
    if (water.fill == 100){
        alert("Wassertank ist bereits voll!");
        return;
    }
    console.log("waterRefill");
    fetch('/unsecure/refill-water', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });
}

function beansRefill(){
    if (gebId("beans-fill").parentElement.classList.contains("deniePress")){
        return;
    }
    if (beans.fill == 100){
        alert("Bohnentank ist bereits voll!");
        return;
    }
    console.log("beansRefill");
    fetch('/unsecure/refill-beans', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });
}
function showCoffeeHistory(){
    window.location.href = "/unsecure/coffees-made";
}
