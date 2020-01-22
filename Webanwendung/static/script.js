// Verändert die URL des Ausgabe-iframe
function setURL(url){
    document.getElementById('iframe-output').src = url;
}

// Asynchrone Abfrage der gewünschten Modbus Register
function getRegister(element_id, register_number){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'register/' + register_number);
    xhr.send();
    var position = 0;

    // Bearbeite die neuen asynchronen Daten
    function handleNewData() {
        var messages = xhr.responseText.split('\n');
        messages.slice(position, -1).forEach(function(value) {
            document.getElementById(element_id).textContent = value;
        });
        position = messages.length - 1;
    }

    // Aktualisiere alle 100ms die Daten
    var timer;
    timer = setInterval(function() {
        handleNewData();
        if (xhr.readyState == XMLHttpRequest.DONE) {
            clearInterval(timer);
        }
    }, 100);
}

// Beim Seitenaufruf werden die Register 1 bis 3 asynchron abgefragt
// Ersetzt die HTML Elemente aus dem ersten Parameter mit den aktuellen Register-Werten
getRegister('register1', 0)
getRegister('register2', 1)
getRegister('register3', 2)
