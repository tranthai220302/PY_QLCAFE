console.log("user", user)
console.log("user")
var loginBtn = document.getElementById("login-btn");
var logoutBtn = document.getElementById("logout-btn");
var payBtn = document.getElementById("pay");
if (user === "AnonymousUser") {
    logoutBtn.style.display = "none";
    loginBtn.style.display = "block";
}
else {
    logoutBtn.style.display = "block";
    loginBtn.style.display = "none";
}
// payBtn.addEventListener('click', function (){
//     var action = this.dataset.action;
//     console.log(action);
//     if(action == 'pay'){
//         alert("Bạn đã đặt hàng và thanh toán thành công!");
//         window.location.href = "{% url 'pay' %}";
//     }
// })

document.getElementById("myForm").addEventListener("submit", function() {
    window.location.href = 'pay';
    alert("Thanh toán thành công!");
    
})