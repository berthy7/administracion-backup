var class_item = '.item-form';
var id_table = '#data_table';

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

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
                    columns: [ 0, 1 ]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1 ]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1 ]
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
        url: 'traspaso_list',
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

$('#fkalmacen_origen').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkalmacen_destino').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fksubalmacen_origen').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fksubalmacen_destino').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fktipo').selectpicker({
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

$('#fkalmacen_origen').change(function () {
    obj = JSON.stringify({
        'fkalmacen': $( "#fkalmacen_origen" ).val(),
        '_xsrf': getCookie("_xsrf")
    })
    
    ruta = "subalmacen_listar_x_almacen";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        $('#fksubalmacen_origen').html('');
        var select = document.getElementById("fksubalmacen_origen")
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['subalmacen']['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fksubalmacen_origen').selectpicker('refresh');

    })

});

$('#fkalmacen_destino').change(function () {
    obj = JSON.stringify({
        'fkalmacen': $( "#fkalmacen_destino" ).val(),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "subalmacen_listar_x_almacen";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        $('#fksubalmacen_destino').html('');
        var select = document.getElementById("fksubalmacen_destino")
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['subalmacen']['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fksubalmacen_destino').selectpicker('refresh');

    })

});

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
                <h5 class="label_normal" id="cantidad_label'+id_in+'"></h5>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-line">\
                    <input id="cantidad'+id_in+'" type="hidden" data-id="'+id_in+'" class="form-control detalle txta-own">\
                    <input id="cantidadNuevo'+id_in+'" data-id="'+id_in+'" class="form-control detalle txta-own">\
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

function get_detalle() {
    objeto = []
    objeto_inputs = $('.detalle')
    cant_ = 0

    // .attr('data-id')

    for (i = 0; i < objeto_inputs.length; i += 4) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 3].value

        if (h3 ==''){
            h3 = 0
        }


        if(parseInt(h3) <= parseInt(h2)){
                if (parseInt(h3) != 0){
                    objeto.push((function add_(h0, h1, h3) {
                    if (h0 =='' ){
                        return {
                            'fkmaterialDetalle': h1,
                            'cantidad': h3
                        }
                    }else{
                        return {
                        'id':h0,
                        'fkmaterialDetalle': h1,
                        'cantidad': h3

                        }
                    }
                })(
                    h0,
                    h1,
                    h3))
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

$('#fkalmacen_origen').change(function () {
    $('#detalle_div').empty()
});

$('#fksubalmacen_origen').change(function () {
    $('#detalle_div').empty()
});

$('#fktipo').change(function () {
    obj = JSON.stringify({
        'fktipo': $( "#fktipo" ).val(),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "material_listar_x_tipo";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)

        $('#fkmaterial').html('');
        var select = document.getElementById("fkmaterial")
        for (var i = 0; i < Object.keys(response.response).length; i++) {
            var option = document.createElement("OPTION");
            option.innerHTML = response['response'][i]['nombre'];
            option.value = response['response'][i]['id'];
            select.appendChild(option);
        }
        $('#fkmaterial').selectpicker('refresh');

    })

});

$('#fkmaterial').change(function () {
    cargar_detalle(parseInt(JSON.parse($('#fkmaterial').val())),parseInt(JSON.parse($('#fkalmacen_origen').val())),parseInt(JSON.parse($('#fksubalmacen_origen').val())))

    $(fkmaterial).val('')
    $(fkmaterial).selectpicker('render')

});

function cargar_detalle(fkmaterial,fksubalmacen) {

    obj = JSON.stringify({
        'idMaterial':fkmaterial,
        'fksubalmacen': fksubalmacen,
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "material_listar_detalle_saldo_subalmacen";

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
            $('#cantidad_label' + response['response'][det].id).html(response['response'][det].cantidad)
            $('#cantidad' + response['response'][det].id).val(response['response'][det].cantidad)

        }

    })

}

$('#new').click(function() {
        $(fkalmacen_origen).val('')
    $(fkalmacen_origen).selectpicker('render')
        $(fksubalmacen_origen).val('')
    $(fksubalmacen_origen).selectpicker('render')
        $(fkalmacen_destino).val('')
    $(fkalmacen_destino).selectpicker('render')
        $(fksubalmacen_destino).val('')
    $(fksubalmacen_destino).selectpicker('render')
            $(fktipo).val('')
    $(fktipo).selectpicker('render')
    $('#detalle_div').empty()
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
                    'descripcion': $('#descripcion').val(),
                    'fksubalmacenorigen': $('#fksubalmacen_origen').val(),
                    'fksubalmacendestino': $('#fksubalmacen_destino').val(),
                    'detalle': respuestaDetalle['objeto']
                })

                ruta = "traspaso_insert";
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

    ajax_call_get('traspaso_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#nombre').val(self.nombre)

        clean_form()
        verif_inputs('')
        $('.item-form').parent().addClass('focused')
        $('#insert').hide()
        $('#update').show()
        $('#modal').modal('show')
    })
}

$('#update').click(function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {
        objeto = JSON.stringify({
            'id': $('#id').val(),
            'nombre': $('#nombre').val()
        })

        ajax_call('traspaso_update', {
            _xsrf: getCookie("_xsrf"),
            object: objeto
        }, null, function(response) {
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
})

function set_enable(e) {
    cb_delete = e
    b = $(e).prop('checked')

    if (!b) {
        cb_title = "¿Está seguro de que desea dar de baja la traspaso?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la traspaso?"
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

            ajax_call('traspaso_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente la traspaso?",
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

            ajax_call('traspaso_delete', {
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
