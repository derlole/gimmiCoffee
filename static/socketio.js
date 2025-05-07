function gebId(id) {
    return document.getElementById(id);
}

const socket = io();
    
socket.on('static_data', (data) => {
    gebId("beans-fill").innerText = data.beans.fill + "%"
    gebId("water-fill").innerText = data.water.fill + "%"
    gebId("beans-filled").innerText = data.beans.refilled
    gebId("water-filled").innerText = data.water.refilled
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
    if (esp_conn_infos.connection_valid) {
        gebId("validButt").classList.add("deniePress");
        gebId("infoMain").classList.remove("blink-orange");
        gebId("machine-status-butt").classList.remove("deniePress");
    }else {
        gebId("validButt").classList.remove("deniePress");
        gebId("infoMain").classList.add("blink-orange");
        gebId("machine-status-butt").classList.add("deniePress");
    }
});
