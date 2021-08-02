const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

function show_toast(category, message, posicion='top-end') {
    Toast.fire({ icon: category, title: message, position: posicion })
}

function show_msg_lg(icono, mensaje, posicion) {
    Swal.fire({
      position: posicion,
      icon: icono,
      title: mensaje,
      showConfirmButton: false,
      timer: 2000
    })
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function get_current_date() {
    let current_date = moment()
    return current_date.format('DD/MM/YYYY hh:mm')
}

function open_docs(url_file) {
    window.open(url_file);
}

function select_search(lista, nombre) {
    for (let dt of lista) {
        let identificador = '#' + nombre + (dt).toString()
        $(identificador).selectpicker({liveSearch: true})
        $(identificador).selectpicker('refresh')
        $(identificador).val('-1')
        $(identificador).selectpicker('render')
    }
}

function get_extension(ruta) {
    var n = ruta.lastIndexOf(".")
    var tail = ruta.indexOf("?raw=1")
    var res = ruta.substring(n + 1, tail)

    return res.toLowerCase()
}

