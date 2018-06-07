function increment1(btn){
    var codpartida = btn.parentNode.parentNode.cells[0].innerText;
    var url = 'http://localhost:5000/increment?country=1&codpartida=' + codpartida;
    window.location.replace(url);
}

function increment2(btn){
    var codpartida = btn.parentNode.parentNode.cells[0].innerText;
    var url = 'http://localhost:5000/increment?country=2&codpartida=' + codpartida;
    window.location.replace(url);
}

function update_score(btn){
    var codpartida = btn.parentNode.parentNode.cells[0].innerText;
    var goal1 = btn.parentNode.parentNode.cells[2].innerText;
    var goal2 = btn.parentNode.parentNode.cells[4].innerText;
    var selecao1 = btn.parentNode.parentNode.cells[1].innerText;
    var selecao2 = btn.parentNode.parentNode.cells[6].innerText;
    var url = 'http://localhost:5000/modify_score?codpartida=' + codpartida + '&goal1=' + goal1 + '&goal2=' + goal2 + '&selecao1=' + selecao1 + '&selecao2=' + selecao2;
    window.location.replace(url);
}

function submit_score(){
    window.location.replace('http://localhost:5000/partidas');
}
