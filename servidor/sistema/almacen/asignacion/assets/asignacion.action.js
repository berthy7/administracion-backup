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

$('#fkalmacen').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkmaterial').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkpersonalDevolucion').selectpicker({
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
                    if (row.disable === '') {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-primary waves-effect" title="Devolucion" onclick="devolucion_item(this)">\
                                Devolucion\
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
        columnDefs: [ { width: '5%', targets: [0] }, { width: '20%', targets: [1, 2, 3,4] }, { width: '35%', targets: [5] } ],
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

function append_input_detalle(id_in) {

    $('#detalle_div').append(
        '<div class="row">\
            <div class="col-sm-1" hidden>\
                <div class="input-group">\
                <input  id="id'+id_in+'" class="form-control subalmacen detalle txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-1" hidden>\
                <div class="input-group">\
                <input  id="fkdetallematerial'+id_in+'" class="form-control subalmacen detalle txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <h5 class="label_normal" id="nombre'+id_in+'"></h5>\
            </div>\
            <div class="col-sm-2">\
                <h5 class="label_normal" id="color'+id_in+'"></h5>\
            </div>\
            <div class="col-sm-1">\
                <h5 class="label_normal" id="talla'+id_in+'"></h5>\
            </div>\
            <div class="col-sm-1">\
                <h5 class="label_normal" id="nuevo'+id_in+'"></h5>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-line">\
                    <input id="saldonuevo'+id_in+'" type="hidden" data-id="'+id_in+'" class="form-control detalle txta-own">\
                    <input id="cantidadNuevo'+id_in+'" data-id="'+id_in+'" class="form-control detalle txta-own">\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <h5 class="label_normal" id="usado'+id_in+'"></h5>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-line">\
                    <input id="saldousado'+id_in+'" type="hidden" data-id="'+id_in+'" class="form-control detalle txta-own">\
                    <input id="cantidadUsado'+id_in+'" data-id="'+id_in+'" class="form-control detalle txta-own">\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_detalle" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>'
    )

            $('.clear_detalle').last().click(function () {
            $(this).parent().parent().remove()
        })


}
function get_detalle2() {
    objeto = []
    objeto_inputs = $('.detalle')
    cant_ = 0

    for (i = 0; i < objeto_inputs.length; i += 9) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value
        h4 = objeto_inputs[i + 4].value
        h5 = objeto_inputs[i + 5].value
        h6 = objeto_inputs[i + 6].value
        h7 = objeto_inputs[i + 7].value
        h8 = objeto_inputs[i + 8].value

        if (h7 ==''){
            h7 = 0
        }
        if (h8 ==''){
            h8 = 0
        }

        if(h7 <= h2){
            if (h7 !=''){
                objeto.push((function add_(h0, h1, h7,h8) {

                if (h0 =='' ){
                    return {
                        'fkmaterialDetalle': h1,
                        'asignacionstock': [{
                            'fkalmacen': 1,
                            'cantidad': h7
                            },
                            {
                            'fkalmacen': 2,
                            'cantidad': h8
                            }]

                    }

                }else{
                    return {
                    'id':h0,
                    'fkmaterialDetalle': h1,
                    'asignacionstock': [{
                            'fkalmacen': 1,
                            'cantidad': h7
                            },
                            {
                            'fkalmacen': 2,
                            'cantidad': h8
                            }]
                    }
                }


            })(
                h0,
                h1,
                h7,
                h8))



            }

        }else{
            return {
                    'objeto':'',
                    'success': false,
                    'mensaje': 'la Cantidad ingresada de '+h4+' '+h5+' '+h6+' es mayor al stock disponible'
                    }
        }

    }

    return {
            'objeto':objeto,
            'success': true,
            'mensaje': ''
            }
}

function get_detalle() {
    objeto = []
    objeto_inputs = $('.detalle')
    cant_ = 0

    // .attr('data-id')

    for (i = 0; i < objeto_inputs.length; i += 6) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value
        h4 = objeto_inputs[i + 4].value
        h5 = objeto_inputs[i + 5].value

        if (h3 ==''){
            h3 = 0
        }
        if (h5 ==''){
            h5 = 0
        }

        if(parseInt(h3) <= parseInt(h2)){
            if(parseInt(h5) <= parseInt(h4)){
                if (parseInt(h3) != 0 || parseInt(h5) != 0){
                    objeto.push((function add_(h0, h1, h3,h5) {
                    if (h0 =='' ){
                        return {
                            'fkalmacen': $('#fkalmacen').val(),
                            'fkmaterialDetalle': h1,
                            'asignacionstock': [{
                                'fksubalmacen': 1,
                                'cantidad': h3
                                },
                                {
                                'fksubalmacen': 2,
                                'cantidad': h5
                                }]
                        }
                    }else{
                        return {
                        'id':h0,
                            'fkalmacen': $('#fkalmacen').val(),
                            'fkmaterialDetalle': h1,
                                'asignacionstock': [{
                                    'fksubalmacen': 1,
                                    'cantidad': h3
                                    },
                                    {
                                    'fksubalmacen': 2,
                                    'cantidad': h5
                                    }]
                        }
                    }
                })(
                    h0,
                    h1,
                    h3,
                    h5))
                }
            }else{
                return {
                'objeto':'',
                'success': false,
                'mensaje': 'la Cantidad ingresada de '+h5+' es mayor al stock disponible'
                }
            }


        }else{
            return {
            'objeto':'',
            'success': false,
            'mensaje': 'la Cantidad ingresada de '+h3+' es mayor al stock disponible'
            }
        }

    }

        return {
            'objeto':objeto,
            'success': true,
            'mensaje': ''
            }
}

$('#fkalmacen').change(function () {
    $('#detalle_div').empty()
});

$('#fkmaterial').change(function () {
    cargar_detalle(parseInt(JSON.parse($('#fkmaterial').val())),parseInt(JSON.parse($('#fkalmacen').val())))

    $(fkmaterial).val('')
    $(fkmaterial).selectpicker('render')
    
});

function cargar_detalle(fkmaterial,fkalmacen) {

    obj = JSON.stringify({
        'idMaterial':fkmaterial,
        'fkalmacen': fkalmacen,
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "material_listar_detalle_saldos";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        for (det in response['response'] ) {

            append_input_detalle(response['response'][det]['id'])

            $('#fkdetallematerial' + response['response'][det].id).val(response['response'][det].id)
            // $('#nombre' + response.response[det].id).val(response.response[det].material.nombre)
            $('#nombre' + response['response'][det].id).html(response['response'][det].material);
            $('#color' + response['response'][det].id).html(response['response'][det].color)
            $('#talla' + response['response'][det].id).html(response['response'][det].talla)
            $('#nuevo' + response['response'][det].id).html(response['response'][det].nuevo)
            $('#saldonuevo' + response['response'][det].id).val(response['response'][det].nuevo)
            $('#usado' + response['response'][det].id).html(response['response'][det].usado)
            $('#saldousado' + response['response'][det].id).val(response['response'][det].usado)



        }

    })

}

$('#new').click(function() {
    $('#detalle_div').empty()
    $(fkpersonal).val('')
    $(fkpersonal).selectpicker('render')
    $(fkalmacen).val('')
    $(fkalmacen).selectpicker('render')
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
                    'fkalmacen': $('#fkalmacen').val(),
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
            Swal.fire(
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
        $('#fkalmacen').val(self.fkalmacen)
        $('#fkalmacen').selectpicker('refresh')
        
        if (self.personal.foto) {
            console.log("entro")
            document.getElementById("imagen_show_img-foto").src =self.personal.foto;
        } else {
            console.log("nulo")
            document.getElementById("imagen_show_img-foto").src = "/resources/images/no_photo.png";
        }

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

function devolucion_item(e) {
    clean_data()


    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })

    ajax_call_get('asignacion_devolucion',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        console.log(self)

        $('#idDevolucion').val(self.id)
        $('#descripcionDevolucion').val(self.descripcion)
        $('#fkalmacen').val(self.fkalmacen)
        $('#fkpersonalDevolucion').val(self.fkpersonal)
        $('#fkpersonalDevolucion').selectpicker('refresh')

        if (self.fotoPersonal) {
        
            document.getElementById("imagen_show_img-fotoDevolucion").src =self.fotoPersonal;
        } else {
      
            document.getElementById("imagen_show_img-fotoDevolucion").src = "/resources/images/no_photo.png";
        }

        $('#detalle_divDevolucion').empty()

        for (i in self.detalle) {

            append_input_detalleDevolucion(self.detalle[i].id)
            $('#id_detalleDevolucion'+self.detalle[i].id).val(self.detalle[i].id)
            $('#materialDevolucion'+self.detalle[i].id).val(self.detalle[i].material)
            $('#colorDevolucion'+self.detalle[i].id).val(self.detalle[i].color)
            $('#tallaDevolucion'+self.detalle[i].id).val(self.detalle[i].talla)
            $('#backupDevolucion'+self.detalle[i].id).val(self.detalle[i].backup)
            $('#usadoDevolucion'+self.detalle[i].id).val(self.detalle[i].usado)


        }

        clean_form()
        verif_inputs('')
        $('.item-form').parent().addClass('focused')
        $('#devolucion').show()
        $('#modalDevolucion').modal('show')
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
            'fkalmacen': $('#fkalmacen').val(),
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
