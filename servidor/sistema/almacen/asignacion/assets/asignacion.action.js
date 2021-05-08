var class_item = '.item-form';
var id_table = '#data_table';
var sw_foto = false;
main_route = '/asignacion';

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

window.onload = function() {
    $('.fotos').fileinput({
        language: 'es',
        showCaption: false,
        showBrowse: true,
        showUpload: false,
        showUploadedThumbs: false,
        showPreview: true,
        'previewFileType': 'any',
        allowedFileExtensions: ['jpg', 'png', 'gif', 'ico', 'jfif', 'svg', 'webp']
    });

    $(".fotos").on('change', function () {
        setTimeout(function () {
            $('.kv-file-zoom').hide()
        }, 400);
    })
}

$('#fkpersonal').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})


$('#fkpersonal').change(function() {

    obj = JSON.stringify({
        'idPersonal': $('#fkpersonal').val()
    })
    ajax_call_get('personal_buscar', {
        _xsrf: getCookie("_xsrf"),
        object: obj
    }, function (response) {
        var self = response.response;

        if (self['foto']) {
            document.getElementById("imagen_show_img-foto").src = self['foto'];
        } else {
            document.getElementById("imagen_show_img-foto").src = "/resources/images/no_photo.png";
        }




    })

})



$('#switch_foto').change(function() {
   sw_foto = $(this).prop('checked')


    if(sw_foto){
        $('#div_foto').show()

    }else{
        $('#div_foto').hide()
        $('#foto').fileinput('clear');
    }

})


function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Fecha", data: "fechar" },
            { title: "Nombre", data: "fullname"},
            { title: "Descripcion", data: "descripcion"},
            { title: "Estado", data: "estado",
                render: function(data, type, row) {
                    return '\
                    <div title="' + row.estado + '">\
                        <input id="enabled' + row.id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable(this)" data-id="' + row.id + '" ' + row.check + ' ' + row.disable + '>\
                        <label for="enabled' + row.id + '"></label>\
                    </div>'
                }
            },
            { title: "Acciones", data: "id",
                render: function(data, type, row) {
                    a = ''
                    if (row.disable === '') {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-primary waves-effect" title="Editar" onclick="edit_item(this)">\
                                <i class="material-icons">edit</i>\
                            </button>'
                    }
                    if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item(this)">\
                                <i class="material-icons">clear</i>\
                            </button>'
                    }
                    if (a === '') a = 'Sin permisos';
                    return a
                }
            },
        ],
        dom: "Bfrtip",
        buttons: [
            {
                extend: 'excelHtml5',
                className: 'btn btn-sm cb-btn-teal',
                exportOptions: {
                    columns: [ 0, 1,2,3 ]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1,2,3 ]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1,2,3 ]
                },
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '30%', targets: [1, 2, 3] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function clean_data() {
    $(class_item).val('')
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'asignacion_list',
        dataType: 'json',
        data: {_xsrf: getCookie("_xsrf")},
        async: false,
        success: function (response) {
            load_table(response.data)
        },
        error: function (jqXHR, status, err) {
            show_message(jqXHR.responseText, 'danger', 'remove');
        }
    });
}


function get_detalle() {
    objeto = []
    objeto_inputs = $('.detalle')
    cant_ = 0

    // .attr('data-id')

    for (i = 0; i < objeto_inputs.length; i += 7) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value
        h4 = objeto_inputs[i + 4].value
        h5 = objeto_inputs[i + 5].value
        h6 = objeto_inputs[i + 6].value

        if(h6 <= h2){
            if (h6 !=''){
                objeto.push((function add_(h0, h1, h6) {

                if (h0 =='' ){
                    return {
                        'fkmaterialDetalle': h1,
                        'cantidad': h6

                    }

                }else{
                    return {
                    'id':h0,
                    'fkmaterialDetalle': h1,
                    'cantidad': h6
                    }
                }


            })(
                h0,
                h1,
                h6))



            }

        }else{
            return {
                    'objeto':'',
                    'success': false,
                    'mensaje': 'la Cantidad ingresada de '+h3+' '+h4+' '+h5+' es mayor al stock disponible'
                    }
        }



    }

    return {
            'objeto':objeto,
            'success': true,
            'mensaje': ''
            }
}

$('#new').click(function() {
    $(fkpersonal).val('')
    $(fkpersonal).selectpicker('render')
    $('#foto').fileinput('clear');
    $('#div_foto').hide()
    $('._cantidad').val('')
    document.getElementById('switch_foto').checked=false
    $('#switch_foto').change()
    document.getElementById("imagen_show_img-foto").src = "/resources/images/no_photo.png";

    clean_data()
    verif_inputs('')
    validationInputSelects("modal")
    $('.item-form').parent().removeClass('focused')

    $('#update').hide()
    $('#insert').show()
});

$('#insert').on('click', function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {

        var respuestaDetalle = get_detalle()
        console.log(respuestaDetalle)

        if(respuestaDetalle['success']){

            var data = new FormData($('#form_submit')[0]);

                objeto = JSON.stringify({
                    'nombre': $('#nombre').val(),
                    'fkpersonal': $('#fkpersonal').val(),
                    'descripcion': $('#descripcion').val(),
                    'detalle': respuestaDetalle['objeto']
                })

                ruta = "asignacion_insert";
                data.append('object', objeto)
                data.append('_xsrf', getCookie("_xsrf"))

                $.ajax({
                    url: ruta,
                    type: "post",
                    data: data,
                    contentType: false,
                    processData: false,
                    cache: false,
                    async: true
                }).done(function (response) {
                    self = JSON.parse(response);

                    if (self.success) {
                        show_msg_lg('success', self.message, 'center')
                        setTimeout(function () {
                            $('#modal').modal('hide')
                            reload_table()
                            window.location = main_route


                        }, 2000);
                    }
                    else show_toast('warning', self.message);
                 })
        }else{
            swal(
                'Error de datos.',
                 respuestaDetalle['mensaje'],
                'warning'
            )
        }






    }
    else show_toast('warning', 'Por favor, ingresa todos los campos requeridos (*).');

});

function edit_item(e) {
    clean_data()
    
    
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })

    ajax_call_get('asignacion_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#nombre').val(self.nombre)
        $('#descripcion').val(self.descripcion)
        $('#fkpersonal').val(self.fkpersonal)
        $('#fkpersonal').selectpicker('refresh')

        for (i in self.detalle) {
            $('#id_detalle'+self.detalle[i].fkmaterialDetalle).val(self.detalle[i].id)
            $('#cantidad'+self.detalle[i].fkmaterialDetalle).val(self.detalle[i].cantidad)

        }

        clean_form()
        verif_inputs('')
        $('.item-form').parent().addClass('focused')
        $('#insert').hide()
        $('#update').show()
        $('#modal').modal('show')
    })
}

$('#update').on('click', function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {

        var data = new FormData($('#form_submit')[0]);

        objeto = JSON.stringify({
            'id': $('#id').val(),
            'nombre': $('#nombre').val(),
            'fkpersonal': $('#fkpersonal').val(),
            'descripcion': $('#descripcion').val(),
            'detalle': get_detalle()

        })
        ruta = "asignacion_update";
        data.append('object', objeto)
        data.append('_xsrf', getCookie("_xsrf"))

        $.ajax({
            url: ruta,
            type: "post",
            data: data,
            contentType: false,
            processData: false,
            cache: false,
            async: true
        }).done(function (response) {
            self = JSON.parse(response);

            if (self.success) {
                show_msg_lg('success', self.message, 'center')
                setTimeout(function () {
                    $('#modal').modal('hide')
                    reload_table()
                }, 2000);
            }
            else show_toast('warning', self.message);

        })

    }
    else show_toast('warning', 'Por favor, ingresa todos los campos requeridos (*).');
});

function set_enable(e) {
    cb_delete = e
    b = $(e).prop('checked')

    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja la asignacion?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la asignacion?"
        cb_text = ""
        cb_type = "info"
    }

    Swal.fire({
        icon: cb_type,
        title: cb_title,
        text: cb_text,
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#1565c0',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            $(cb_delete).prop('checked', !$(cb_delete).is(':checked'))

            if (b) $(cb_delete).parent().prop('title', 'Activo');
            else $(cb_delete).parent().prop('title', 'Inhabilitado');

            objeto =JSON.stringify({
                id: parseInt($(cb_delete).attr('data-id')),
                estado: b
            })

            ajax_call('asignacion_state', {
                object: objeto, _xsrf: getCookie("_xsrf")}, null,
                function (response) {
                    self = JSON.parse(response)
                    icono = self.success? 'success': 'warning'
                    show_msg_lg(icono, self.message, 'center')
                    setTimeout(function() {
                        reload_table()
                    }, 2000);
                }
            )
        }
        else if (result.dismiss === 'cancel') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
        else if (result.dismiss === 'esc') $(cb_delete).prop('checked', !$(cb_delete).is(':checked'));
    })
}

function delete_item(e) {
    Swal.fire({
        icon: "warning",
        title: "¿Está seguro de que desea eliminar permanentemente la asignacion?",
        text: "",
        showCancelButton: true,
        allowOutsideClick: false,
        confirmButtonColor: '#1565c0',
        cancelButtonColor: '#ef5350',
        confirmButtonText: 'Aceptar',
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.value) {
            objeto = JSON.stringify({
                'id': parseInt(JSON.parse($(e).attr('data-json')))
            })

            ajax_call('asignacion_delete', {
                object: objeto,_xsrf: getCookie("_xsrf")}, null,
                function (response) {
                    self = JSON.parse(response);

                    if (self.success) {
                        show_msg_lg('success', self.message, 'center')
                        setTimeout(function () {
                            reload_table()
                        }, 2000);
                    }
                    else show_toast('warning', self.message);
                }
            );
        }
    })
}
