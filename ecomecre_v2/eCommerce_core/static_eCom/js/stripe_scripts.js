// Create an instance of the Stripe object with your publishable API key

// var stripe = Stripe("{{ stripe_key }}");


var stripe = Stripe("pk_test_51HfQZqEVa7KrzHgTgqkamdkzgINVOPISYba6Jjo8yjF3KvQslC8R" +
    "Vpgm1qA79Yt9MA396lxSPpk5wmS3UakvpIna00BjEUpDLp");
var checkoutButton = document.getElementById("checkout-button");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

checkoutButton.addEventListener("click", function () {
    fetch("{% url 'cart:payment_redirect' pk=order.pk %}", {
        method: "POST",
        headers: {"X-CSRFToken": csrftoken},
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (session) {
            return stripe.redirectToCheckout({sessionId: session.id});
        })
        .then(function (result) {
            // If redirectToCheckout fails due to a browser or network
            // error, you should display the localized error message to your
            // customer using error.message.
            if (result.error) {
                alert(result.error.message);
            }
        })
        .catch(function (error) {
            console.error("Error:", error);
        });
});