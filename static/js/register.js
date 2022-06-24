const userEmail = document.querySelector("#user-email");
const userPasswords = document.querySelectorAll(".password");
const loginBtn = document.querySelector("#login");
const signupBtn = document.querySelector("#signup");
const passwordError = document.querySelector("#password_error");
const CpasswordError = document.querySelector("#confirm_password_error");
const emailError = document.querySelector("#email_error");
const tooglePasswords = document.querySelectorAll(".password-toogle");
let form = document.querySelector("form");
const feedback = document.querySelector(".alert");
const sendCodeBtn = document.querySelector(".code_btn");
const countdown = document.querySelector(".countdown");
const codeField = document.querySelector("#code");

form.onsubmit = e => e.preventDefault();

let userVerification = (action, btn) => {
    let emailValue = userEmail.value;
    let passwordValue = userPasswords[0].value;
    let CpasswordValue = userPasswords[userPasswords.length - 1].value;

    if (emailValue === "") {
        emailError.textContent = "Email is required";
        return;
    } else if (!(emailValue.includes("@") && emailValue.includes("."))) {
        emailError.textContent = "Invalid Email";
        return
    } else {
        emailError.textContent = "";
    }
    if (passwordValue === "") {
        passwordError.textContent = "Password is required";
        return;
    } else if (passwordValue.length < 5 || passwordValue.length > 32) {
        passwordError.textContent = "Password should be between the range of 5 to 32 characters";
        return
    } else {
        passwordError.textContent = "";
    }
    if (CpasswordValue !== passwordValue) {
        CpasswordError.textContent = "Password mismatch";
        return
    } else {
        CpasswordError ? CpasswordError.textContent = "" : ""
    }

    if (action === "login") {
        let userDetails = JSON.parse(sessionStorage.getItem("user-details"));
        if (!userDetails) {
            feedback.style.visibility = "visible"
            feedback.textContent = "You don't have an account, sign up. Redirecting ...";
            setTimeout(() => {
                window.location.pathname = "/signup.html";
            }, 3000);
            return
        }
        if (userDetails.email !== emailValue) {
            emailError.textContent = "Email is incorrect";
            return
        }
        if (userDetails.password !== passwordValue) {
            passwordError.textContent = "Password is incorrect";
            return
        }
        btn.classList.add("loading")
        window.location.pathname = "/";
        return;
    } else if (action === "signup") {
        let userDetails = JSON.parse(sessionStorage.getItem("user-details"));
        if (userDetails && userDetails.email === emailValue) {
            feedback.style.visibility = "visible";
            feedback.textContent = "You have an account, Sign In instead. Redirecting ...";
            setTimeout(() => {
                window.location.pathname = "/login.html";
            }, 3000);
            return

        }
        sessionStorage.setItem("user-details", JSON.stringify({
            email: emailValue,
            password: passwordValue
        }));
        btn.classList.add("loading")

        window.location.pathname = "/";
    }
}

let startCount = () => {
    let count = 40;
    let emailValue = userEmail.value;
    if (emailValue === "") {
        emailError.textContent = "Email is required";
        return;
    } else if (!(emailValue.includes("@") && emailValue.includes("."))) {
        emailError.textContent = "Invalid Email";
        return
    } else {
        emailError.textContent = "";
        setInterval(() => {
            countdown.textContent = `${count}s`;
            count > 0 && count--;
        }, 1000);
    }
}

for (let i = 0; i < tooglePasswords.length; i++) {
    tooglePasswords[i].onclick = () => {
        if (userPasswords[i].type === "password") {
            userPasswords[i].type = "text"
            tooglePasswords[i].classList.add("fa-eye")
            tooglePasswords[i].classList.remove("fa-eye-slash")

        } else {
            userPasswords[i].type = "password";
            tooglePasswords[i].classList.remove("fa-eye")
            tooglePasswords[i].classList.add("fa-eye-slash")
        }
    }
}

if (loginBtn) loginBtn.onclick = (e) => userVerification("login", e.target);
if (signupBtn) signupBtn.onclick = (e) => userVerification("signup", e.target);

if (sendCodeBtn) sendCodeBtn.onclick = startCount;