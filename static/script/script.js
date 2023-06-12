let btn = document.querySelectorAll("button");
let proses_box = document.querySelector("p");

for(let i = 0; i < btn.length; i++){
    btn[i].addEventListener("click", function(){
        btn[i].innerHTML = 'Memproses . . . .';
        btn[i].style.cursor = "not-allowed";
        proses_box.style.display = "initial";
    })
}