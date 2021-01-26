document.addEventListener('DOMContentLoaded', function() {

    document.getElementById("reg_form").addEventListener("submit", regUser);

});

async function regUser(e) {
    e.preventDefault();

    addClient()
        .then(data => {
            console.log(data);
        })
        .catch(e => console.log(e));
}

async function addClient() {

    let firstName = document.getElementById("firstName").value;
    let lastName = document.getElementById("lastName").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let phoneNumber = document.getElementById("phoneNumber").value;


    let response = await fetch('http://localhost:8080/masters', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            phoneNumber: phoneNumber,
            name: firstName + " " + lastName,
            email: email,
            password: password
        })
    });


    console.log(response);

    if(response.status === 409) return null;

    return await response.json();
}