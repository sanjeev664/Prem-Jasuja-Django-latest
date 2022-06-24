const msgExtrasBtn = document.querySelectorAll('.msg_extras_btn');
const msgExtrasList = document.querySelectorAll('.msg_extras_list');

for (let msgBtnIndex = 0; msgBtnIndex < msgExtrasBtn.length; msgBtnIndex++) {
    msgExtrasBtn[msgBtnIndex].onclick = () => {
        if (msgExtrasList[msgBtnIndex].classList.contains("hide")) {
            msgExtrasList[msgBtnIndex].classList.remove("hide");   
            return;   
        }
        msgExtrasList[msgBtnIndex].classList.add("hide");   
    }
}
document.body.onclick = (e) => {
    if (!(e.target.classList.contains("msg_extras_btn") || e.target.classList.contains("caret"))) {
        for (let msgBtnIndex = 0; msgBtnIndex < msgExtrasList.length; msgBtnIndex++) {
            if (!msgExtrasList[msgBtnIndex].classList.contains("hide")) msgExtrasList[msgBtnIndex].classList.add("hide");   
        }
    }

}