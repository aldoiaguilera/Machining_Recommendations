async function getCreator() {
    let creator = await fetch("https://api.github.com/users/aldoiaguilera")
        .then( response => response.json() );
    position = document.getElementsByClassName("creator-container");
    position = position[0]
    position.innerHTML = `
    <p><strong>About the creator</strong></p>
    <img src="${creator['avatar_url']}" alt="Creator avatar" id="creator-avatar">
    <p>${creator['name']}</p>
    <a href="${creator['html_url']}"><button id="creator-button">Go to creator's GitHub</button></a>
    `
    console.log(creator)
}

function demo() {
    document.getElementById('email').value = 'test@gmail.com';
    document.getElementById('password').value = 'password';
}

getCreator()