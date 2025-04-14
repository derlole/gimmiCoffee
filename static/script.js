document.getElementById('befehlForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Seite nicht neu laden!

    const befehl = document.getElementById('befehl').value;

    fetch(`/send?befehl=${encodeURIComponent(befehl)}`)
        .then(response => response.text())
        .then(text => {
            document.getElementById('status').textContent = text;
        })
        .catch(err => {
            document.getElementById('status').textContent = 'Fehler beim Senden.';
        });
});
