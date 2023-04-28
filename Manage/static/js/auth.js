console.log("user", user)
console.log("user")
var loginBtn = document.getElementById("login-btn");
var logoutBtn = document.getElementById("logout-btn");
if (user === "AnonymousUser") {
    logoutBtn.style.display = "none";
    loginBtn.style.display = "block";
}
else {
    logoutBtn.style.display = "block";
    loginBtn.style.display = "none";
}