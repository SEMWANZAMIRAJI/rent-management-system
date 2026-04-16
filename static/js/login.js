// Show / Hide password
function togglePassword(){

let input = document.getElementById("password");
let icon = document.getElementById("toggleIcon");

if(input.type === "password"){
input.type = "text";
icon.classList.remove("fa-eye");
icon.classList.add("fa-eye-slash");
}else{
input.type = "password";
icon.classList.remove("fa-eye-slash");
icon.classList.add("fa-eye");
}

}