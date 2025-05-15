document.getElementById('login-btn').addEventListener('click', function () {
    const username = document.getElementById('usrnm').value.trim();
    const password = document.getElementById('pw').value;

    if (!username || !password) {
        alert("Bitte Benutzername und Passwort eingeben.");
        return;
    }
    fetch(`/unsecure/verify?username=${username}&pass=${password}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        //console.log(data)
        window.location.href = data.route

    });
});
document.getElementById('create-btn').addEventListener('click', function () {
    const username = document.getElementById('usrnm').value.trim();
    const password = document.getElementById('pw').value;
    if (!username || !password) {
        alert("Bitte Benutzername und Passwort eingeben.");
        return;
    }

    const result = confirm(`Möchtest du einen Nutzer mit ${username} erstellen?`);
    if (!result) {
        return;
    }
    fetch(`/unsecure/register?username=${username}&pass=${password}`, { method: 'POST' })
    .then(res => res.json)
    .then(data => {
        console.log(data)
    })
})