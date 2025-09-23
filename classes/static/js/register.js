const usernamefield = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid-feedback');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.email-invalid-feedback'); //emailFeedBackArea
const passwordField = document.querySelector('#passwordField');
const passwordFeedBackArea = document.querySelector('.password-invalid-feedback');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit_btn');




const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }
    else {showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");}
};

showPasswordToggle.addEventListener('click', handleToggleInput);



emailField.addEventListener("keyup", (e) => {
    console.log("Key up event fired");
    const emailval = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";     


    if (emailval.length > 0) {
        fetch("/authentication/validate-email/", {
            method: "POST",
            body: JSON.stringify({ email: emailval }),
            
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data:", data);
            if (data.email_error) {
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                }else {
                submitBtn.removeAttribute("disabled");
                }
        })
        
    }
});








usernamefield.addEventListener("keyup", (e) => {
    console.log("Key up event fired");
    const usernameval = e.target.value;

    usernamefield.classList.remove("is-invalid");
    feedBackArea.style.display = "none";     


    if (usernameval.length > 0) {
        fetch("/authentication/validate-username/", {
            method: "POST",
            body: JSON.stringify({ username: usernameval }),
            
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data:", data);
            if (data.username_error) {
                usernamefield.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitBtn.disabled = true;
                }else {
                submitBtn.removeAttribute("disabled");
                }
        })
        
    }
});
