//variables
const backBtn = document.querySelector('.back-btn');
const userFriendsList = document.querySelector('.friends');
const extraBtn = document.querySelector('.extras');
const extrasList = document.querySelector('.extras-list');
const closeBtn = document.querySelector('.close-btn');
let currentFriend = document.querySelector('.current-friend .title h3');
let currentFriendAvatar = document.querySelector('.current-friend .avatar img');
const userFriends = document.querySelectorAll('.user-friend');
const userFriendsNames = document.querySelectorAll('.user-friends .title h5');
const userFriendsImages = document.querySelectorAll('.user-friends .avatar img');

//functions
let showFriendsList = () => {
  userFriendsList.classList.remove('hide');
}
let hideFriendsList = () => {
  userFriendsList.classList.add('hide');
}
let showExtrasList = () => {
  extrasList.classList.toggle('hidden');
}

//events
backBtn.onclick = showFriendsList;
extraBtn.onclick = showExtrasList;
closeBtn.onclick = hideFriendsList;

for (let friendIndex = 0; friendIndex < userFriends.length; friendIndex++) {
  userFriends[friendIndex].onclick = () => {
    currentFriend.innerHTML = `Chat with ${userFriendsNames[friendIndex].innerHTML}`;
    currentFriendAvatar.src = userFriendsImages[friendIndex].src;
    hideFriendsList();
  }
}

document.body.onclick = e => {
  if(!e.target.classList.contains('extras') && !e.target.classList.contains('caret')){
    if(!extrasList.classList.contains('hidden')) {
      extrasList.classList.add('hidden');
     }
  }
}


const messages = document.querySelectorAll(".message-container");
let delay = 0;
messages.forEach(el=>{
  el.style.animation = "fade-in 1s ease forwards";
  el.style.animationDelay= delay +"s";
  delay += 0.33;
});
