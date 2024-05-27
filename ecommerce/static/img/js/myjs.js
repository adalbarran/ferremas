




// const formulario = document.getElementById("Form_Contacto");

// const userName = document.getElementById("userName");
// const userEmail = document.getElementById("userEmail");
// const userMens = document.getElementById("userMens");
// const alertSuccess = document.getElementById("alertSuccess");

// const regUserName = /^[A-Za-zÑñÁáÉéÍíÓóÚúÜü\s]+$/;
// const regUserEmail = /^[a-z0-9]+(\.[_a-z0-9]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,15})$/;

// const pintarMensajeExito = () => {
//     alertSuccess.classList.remove("d-none");
//     alertSuccess.textContent = "Mensaje enviado con éxito";
// };

// const pintarMensajeError = (errores) => {
//     errores.forEach((item) => {
//         item.tipo.classList.remove("d-none");
//         item.tipo.textContent = item.msg;
//     });
// };

// formulario.addEventListener("submit", (e) => {
//     e.preventDefault();
//     alert("Validando Formulario");

//     alertSuccess.classList.add("d-none");
//     const errores = [];

//     // validar nombre
//     if (!regUserName.test(userName.value) || !userName.value.trim()) {
//         userName.classList.add("is-invalid");

//         errores.push({
//             tipo: alertName,
//             msg: "Formato no válido campo nombre, solo letras",
//         });
//     } else {
//         userName.classList.remove("is-invalid");
//         userName.classList.add("is-valid");
//         alertName.classList.add("d-none");
//     }

//     // validar email
//     if (!regUserEmail.test(userEmail.value) || !userEmail.value.trim()) {
//         userEmail.classList.add("is-invalid");

//         errores.push({
//             tipo: alertEmail,
//             msg: "Escriba un correo válido",
//         });
//     } else {
//         userEmail.classList.remove("is-invalid");
//         userEmail.classList.add("is-valid");
//         alertEmail.classList.add("d-none");
//     }

//     if (errores.length !== 0) {
//         pintarMensajeError(errores);
//         return;
//     }

//     console.log("Formulario enviado con éxito");
//     pintarMensajeExito();
// });

// $('.carousel').carousel({
//     interval: 2000
//   })

//   $('#myCarousel').on('slide.bs.carousel', function () {
//     slid.bs.carousel
//   })

function valForm1(){
    console.log("Pagina Funcionando");
    var vNom = $('#nombre').val();
    var vMail = $('#correo').val();
    var vMensaje = $('#mensaje').val();

    //Validar campo nombre

    if(vNom=="" || vNom==null ) {
        Err_color("nombre")
        Err_Contenido("Campo Nombre")
        return false;
    }

    else{
        var expresion = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]*$/;
        if(!expresion.test(vNom)){
            Err_color("nombre");
            Err_Contenido(" nombre, No se permiten caracteres especiales");
            return false;
        }
    }

    if(vMail=="" || vMail==null ) {
        Err_color("correo")
        Err_Contenido("correo")
        return false;
    }

    else{
        var expresion = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/;
        if(!expresion.test(vMail)){
            Err_color("correo");
            Err_Contenido(" formato de correo no admitido");
            return false;
        }
    }

    if(vMensaje=="" || vMensaje==null ) {
        Err_color("mensaje")
        Err_Contenido("mensaje")
        return false;
    }

    else{
        var expresion = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]*$/;
        if(!expresion.test(vMensaje)){
            Err_color("mensaje");
            Err_Contenido(" mensaje no admitido");
            return false;
        }
    }

    $('form').submit();
    return true;
}


function Err_color (dato) {
    $('#' + dato).css({border : '1px solid #dd5144'});
}

function Err_Contenido (dato) {
    alert("Error en el ingreso del campo " + dato);

}

function ColorDefault (dato){ 
    $('#' + dato).css({border : '1px solid #999'});
    
}

$('input').focus(function () { 
   ColorDefault('nombre');
   ColorDefault('correo');
   ColorDefault('mensaje');
    
})

$('#mensaje').css({resize : 'none'
});








function valForm2(){
    console.log("Pagina Funcionando");
    var vNom = $('#nombre').val();
    var vContra = $('#contraseña').val();
    var vMensaje = $('#mensaje').val();

    //Validar campo nombre

    if(vNom=="" || vNom==null ) {
        Err_color("nombre")
        Err_Contenido("Campo Nombre de usuario")
        return false;
    }

    else{
        var expresion = /^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]*$/;
        if(!expresion.test(vNom)){
            Err_color("nombre");
            Err_Contenido(" nombre, No se permiten caracteres especiales");
            return false;
        }
    }

    if(vContra=="" || vContra==null ) {
        Err_color("Contraseña")
        Err_Contenido("Contraseña")
        return false;
    }


    $('form').submit();
    return true;
}


function Err_color (dato) {
    $('#' + dato).css({border : '1px solid #dd5144'});
}

function Err_Contenido (dato) {
    alert("Error en el ingreso del campo " + dato);

}

function ColorDefault (dato){ 
    $('#' + dato).css({border : '1px solid #999'});
    
}

$('input').focus(function () { 
   ColorDefault('nombre');
   ColorDefault('contraseña');
   ColorDefault('mensaje');
    
})

$('#mensaje').css({resize : 'none'
});