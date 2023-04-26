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
            console.log("user   no  login")
        }
        else {
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
            'Content-Type': 'aplication/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify({'id':id,'action':action})
    })
}