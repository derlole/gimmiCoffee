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

function toggleMachine() {
    if (gebId("machine-status-butt").classList.contains("deniePress")){
        return;
    }
    // console.log("toggleMachine");
    const result = confirm("Möchtest du den Vorgang wirklich ausführen?");
    if (!result) {
        return;
    }
    console.log("toggleMachine");
    document.getElementById("machine-status").innerText = "PENDING";
    document.getElementById("machine-status-butt").classList.add("blink-orange");
    fetch('/unsecure/esp/toggle-machine', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });
}