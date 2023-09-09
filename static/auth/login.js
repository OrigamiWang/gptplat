function doLogin() {
    console.log("login begin...")
    let u_val = document.getElementById('username').value
    let p_val = document.getElementById('password').value
    fetch('/auth/login?username=' + u_val + '&password=' + p_val, {method: 'POST'})
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
}
