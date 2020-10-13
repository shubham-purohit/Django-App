console.log("App loaded!!");

var updateBtns = document.getElementsByClassName('update-cart');
console.log("USER:", user)
for(var i=0; i< updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function() {
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productID:', productId, "action:", action);
	})
}