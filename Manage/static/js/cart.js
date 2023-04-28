console.log("heloo")
// Đăng ký sự kiện nhấn nút "Thêm vào giỏ hàng"
var addBtns = document.querySelectorAll('.update-cart');
addBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
        var id = this.dataset.id;
        var action = this.dataset.action;
        console.log('Dish ID: ' + id + ', Action: ' + action);
        console.log("user", user)
        if (user === "AnonymousUser") {
            console.log("1")
        }
        else {
            console.log("1")
            updatecart(id, action)
        }
    });
});
function updatecart(id, action) {
    console.log("login")
    var url = 'updatecart'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'id': id, 'action': action })
    })
        .then(response => response.json())
        .then(data => {
            var data = JSON.parse(data);
            var cartInfo = document.getElementById("cart-info");
            cartInfo.innerHTML = "$" + data.cart;
            console.log(data);
            var cartInfo = document.getElementById("dish_amount" + id);
            cartInfo.innerHTML = data.amount;
        });
}