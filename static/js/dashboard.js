document.querySelectorAll(".submenu-toggle").forEach(btn=>{

btn.addEventListener("click",()=>{

let submenu = btn.nextElementSibling;

submenu.classList.toggle("hidden");

})

});