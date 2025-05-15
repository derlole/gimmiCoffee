document.getElementById('login-btn').addEventListener('click', function () {
    const username = document.getElementById('usrnm').value.trim();
    const password = document.getElementById('pw').value;

    if (!username || !password) {
        alert("Bitte Benutzername und Passwort eingeben.");
        return;
    }

    // Beispiel: Zufällige User-ID generieren (normalerweise kommt das vom Server)
    const userid = Math.floor(Math.random() * 100000);

    // Weiterleitung zur Startseite mit Parametern
    window.location.href = `/unsecure/?username=${encodeURIComponent(username)}&userid=${userid}`;
});