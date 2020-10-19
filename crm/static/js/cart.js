console.log("App loaded!!");

var updateBtns = document.getElementsByClassName('update-cart');
console.log("USER:", user)
for(var i=0; i< updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function() {
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productID:', productId, "action:", action);

		updateUserOrder(productId, action)
	})
}

function updateUserOrder(productId, action) {

	console.log("User is authenticated!!");

	var  url = "/update_item/"

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-type': 'application/json',
			'X-CSRFToken' : csrftoken,
		},
		body:JSON.stringify({'productId':productId, 'action': action})
	})
	.then((response) => {
		return response.json()
	})
	.then((data) => {
		console.log('data loaded: ', data)
		location.reload()
	})

}