const openCategoriesBtn = document.querySelectorAll('.open-categories-btn');
const closeCategoriesBtn = document.querySelector('.close-categories-btn');
const categoriesContainer = document.querySelector('.categories');
const profileLinks = document.querySelectorAll('.profile-link');
const profileContent = document.querySelectorAll('.profile');

for (let i = 0; i < openCategoriesBtn.length; i++) {
    openCategoriesBtn[i].onclick = () => categoriesContainer.classList.remove('hide');
    
}
    closeCategoriesBtn.onclick = () => categoriesContainer.classList.add('hide');

for (let i = 0; i < profileLinks.length; i++) {
    profileLinks[i].onclick = () => {
        for (let j = 0; j < profileLinks.length; j++) {
           profileLinks[j].classList.remove('active');
            
        }
        profileLinks[i].classList.add('active');

        for (let index = 0; index < profileContent.length; index++) {
            profileContent[index].classList.remove('active');
             if(profileLinks[i].getAttribute('data-target') === profileContent[index].id){
                profileContent[index].classList.add('active');
                categoriesContainer.classList.add('hide');
             }       
        }
    }
    
}