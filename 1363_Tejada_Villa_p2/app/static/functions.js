function verifyRegister(){
    var username = document.getElementById("usernamer").value;
    var pass = document.getElementById("passr").value;
    var reppass = document.getElementById("repassr").value;
    var tarjeta = document.getElementById("tarjetar").value;
    var email = document.getElementById("emailr").value;
    var er = /^[a-zA-Z0-9_-]{0,}$/;
    var ercard = /^[0-9]{16,16}$/;
    if(username === "" || pass === "" || reppass === "" || email === "" || tarjeta === ""){
        alert("Todos los campos son obligatorios");
        return false;
    }
    if(pass.length < 8){
        alert("La contraseña debe tener, al menos, 8 caracteres");
        return false;
    }
    if(pass != reppass){
        alert("Las contraseñas no coinciden");
        return false;
    }
    if(!er.test(username)){
        alert("Caracteres no validos en el nombre de usuario");
        return false;
    }
    if(!ercard.test(tarjeta)){
        alert("Introduce un numero de tarjeta válido");
        return false;
    }
    return true;

}

function confirmPurchase(){
    return confirm("¿Estás seguro?");
}

function verifyMoney(){
    var er = /^\d*(\.\d{1})?\d{0,1}$/;
    var amount = document.getElementById("cantidad").value;

    if(amount === ""){
        alert("Introduce una cantidad");
        return false;
    }
    if(er.test(amount)){
        return true;
    }else{
        alert("Introduce una cantidad valida (ej: 12, 3.7, 4.66)");
        return false;
    }
}

function rand(url){
    if(window.XMLHttpRequest) {
        connection = new XMLHttpRequest();
      }
      else if(window.ActiveXObject) {
        connection = new ActiveXObject("Microsoft.XMLHTTP");
      }
      connection.onreadystatechange = response;
      connection.open("GET", url,true);

      connection.send();

    }

function callrand(url){
    setInterval("rand(url)",3000,true);
}

function response() {
    if(connection.readyState == 4) {
        document.getElementById("onlinecont").value = connection.responseText ;

    }
}

$(document).ready(function() {
    $('#passr').keyup(function() {
    $('#result').html(checkStrength($('#passr').val()));
    });
    function checkStrength(passr) {

        if (passr.length < 8) {
            $('#result').removeClass();
            $('#result').addClass('no_permitida');
            return 'No permitida';
        }
        else if(passr.length >= 8 && passr.length < 12){
            $('#result').removeClass();
            $('#result').addClass('debil');
            return 'Débil';
        }
        else if(passr.length >= 12 && passr.length < 16){
            $('#result').removeClass();
            $('#result').addClass('buena');
            return 'Buena';
        }
        else{
            $('#result').removeClass();
            $('#result').addClass('muy_buena');
            return 'Muy buena';
        }

    }

    $(".flip").click(function(){
        $(this).next().find(".panel").slideToggle("slow");
    });


});
            
