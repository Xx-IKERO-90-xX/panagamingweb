let contentDiv = document.getElementById('content');


function clear() {
    contentDiv.innerHTML = "";
}

function loadFriendships() {
    clear();

    let friendshipsTemplate = document.getElementById('friendships-template').content.cloneNode(true);
    let friendships = friendshipsTemplate.getElementById('friendships-content');
    contentDiv.append(friendships);
}

function loadContacts() {
    clear();

    let contactsTemplate = document.getElementById('contacts-template').content.cloneNode(true);
    let contacts = contactsTemplate.getElementById('contacts-content');
    contentDiv.append(contacts);    
}

let btnFriends = document.getElementById('btn-friends');
let btnContacts = document.getElementById('btn-contacts');

btnFriends.addEventListener('click', loadFriendships);
btnContacts.addEventListener('click', loadContacts);

loadFriendships();