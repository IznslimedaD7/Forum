const menulist = document.getElementsByClassName('menu-list-block')[0]
const menubut = document.getElementsByClassName('menu-button')[0]

console.log(menubut.classList, menubut.classList[4])

menubut.onclick = function(){
    if( menubut.classList[8] == undefined){
        menubut.classList.add('anim')
        menulist.classList.add('vis')
    }
    else{
        menubut.classList.remove('anim')
        menulist.classList.remove('vis')
    }
}
