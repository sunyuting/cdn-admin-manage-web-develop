function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // 发送 AJAX 请求到 Flask 后端的登录接口
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function register() {
    var username = document.getElementById('username').value; // 获取用户名
    var password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password }) // 包含 username
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function resetPassword() {
    var username = document.getElementById('username').value;
    var newPassword = document.getElementById('new_password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
    if (newPassword !== confirmPassword) {
        alert('Passwords do not match.');
        return; // 不继续执行，因为密码不匹配
    }
    // 发送 AJAX 请求到 Flask 后端的密码重置接口
    fetch('http://127.0.0.1:5000/reset-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, new_password: newPassword })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
