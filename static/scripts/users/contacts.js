let contentDiv = document.getElementById('content');
let friendshipsBtn = document.getElementById('friendships-btn');
let requestsBtn = document.getElementById('requests-btn');

function clear() {
    contentDiv.innerHTML = "";
}

function loadFriendships() {
    clear();
    let template = document.getElementById('frinships-template').content.cloneNode(true);
    let friendshipsContent = template.getElementById('friendships-content');

    contentDiv.appendChild(friendshipsContent)
}

function loadFriendshipRequests() {
    clear();
    let template = document.getElementById('friendship-pending-template').content.cloneNode(true);
    let friendshipPendingRequest = template.getElementById('friendship-pending-request');

    contentDiv.appendChild(friendshipPendingRequest);
}

friendshipsBtn.addEventListener('click', loadFriendships);
requestsBtn.addEventListener('click', loadFriendshipRequests);  

loadFriendships();

