let USER_SIGNED_IN = false;

function check_sign_in(game) {
    const is_user_signed_in = localStorage.getItem("USER_SIGNED_IN");

    if (is_user_signed_in !== null && is_user_signed_in === 'true') {
        window.location.href = "./buy.html?game=" + game;
    } else {
        window.location.href = "./signin.html";
    }
}

function set_user_signed_in() {
    localStorage.setItem('USER_SIGNED_IN', true);
}