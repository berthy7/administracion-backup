var class_item = '.item-form';
var id_table = '#data_table';

$(document).ready( function () {
    reload_table();
    AddCheck()
});
validationKeyup("modal")

$('#fkalmacen').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

function AddCheck() {
    $('.empleado_checkbox').click(function () {

        cb_delete = this
        check = $(this)
        check.parent().waitMe({
            effect: 'timer',
            bg: 'rgba(255,255,255,0.90)',
            color: '#555'
        });
        if(check.html() == "check_box"){
            $.ajax({
                method: "POST",
                url: '/lista_delete',
                data: {'id': parseInt($(cb_delete).attr('data-id')),tipo: parseInt($(cb_delete).attr('data-tipo')),'enabled': $(cb_delete).is(':checked')},
                async: true
            }).done(function (response) {
                response = JSON.parse(response)
                if (response.success){
                    check.html("check_box_outline_blank").parent().waitMe('hide')
                }
            })
        }else{
            $.ajax({
                method: "POST",
                url: '/lista_delete',
                data: {'id': parseInt($(cb_delete).attr('data-id')),tipo: parseInt($(cb_delete).attr('data-tipo')),'enabled': $(cb_delete).is(':checked')},
                async: true
            }).done(function (response) {
                response = JSON.parse(response)
                if (response.success){
                    check.html("check_box").parent().waitMe('hide')
                }
            })
        }
    })
}

$('#fkmaterial').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fktalla').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkmaterial').change(function () {
    cargar_detalle(parseInt(JSON.parse($('#fkmaterial').val())))

    $(fkmaterial).val('')
    $(fkmaterial).selectpicker('render')
    
});

function cargar_detalle(id) {
    obj = JSON.stringify({
        'idMaterial': id,
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "material_listar_detalle";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        $('#detalle_div').empty()
        for (var i = 0; i < Object.keys(response.response).length; i++) {

            append_input_detalle(response.response[i]['id'])
            $('#fkcolor'+response.response[i]['id']).val(response.response[i]['fkcolor'])
            $('#fkcolor'+response.response[i]['id']).selectpicker('render')
            $('#fktalla'+response.response[i]['id']).val(response.response[i]['fktalla'])
            $('#fktalla'+response.response[i]['id']).selectpicker('render')


        }

    })

}

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Fechar", data: "fechar" },
            { title: "Nro° Boleta", data: "nroboleta" },
            { title: "Observacion", data: "observacion" },
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
                    columns: [ 0,1 ,2,3 ]
                },
            }
        ],
        "order": [ [0, 'desc'] ],
        columnDefs: [ { width: '5%', targets: [0] }, { width: '20%', targets: [1, 2] } ],
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
        url: 'stock_list',
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

$('#new_detalle').click(function () {
    append_input_detalle('')
})


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
            <div class="col-sm-3">\
                <div class="form-line">\
                    <input id="nombre'+id_in+'" data-id="'+id_in+'" class="form-control txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-line">\
                    <input id="color'+id_in+'" data-id="'+id_in+'" class="form-control txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <div class="form-line">\
                    <input id="talla'+id_in+'" data-id="'+id_in+'" class="form-control txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-line">\
                    <input id="cantidadNuevo'+id_in+'" data-id="'+id_in+'" class="form-control detalle txta-own">\
                </div>\
            </div>\
            <div class="col-sm-2">\
                <div class="form-line">\
                    <input id="cantidadUsado'+id_in+'" data-id="'+id_in+'" class="form-control detalle txta-own">\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect clear_detalle" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>\
        </br>'
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

        if (h2 ==''){
            h2 = 0
        }
        if (h3 ==''){
            h3 = 0
        }


        if (h2 !=''){
            objeto.push((function add_(h0, h1, h2,h3) {

            if (h0 =='' ){
                return {
                    'fkalmacen': $('#fkalmacen').val(),
                    'fkmaterialDetalle': h1,
                    'detallestock': [{
                        'fksubalmacen': 1,
                        'cantidad': h2
                        },
                        {
                        'fksubalmacen': 2,
                        'cantidad': h3
                        }]

                }

            }else{
                return {
                'id':h0,
                    'fkalmacen': $('#fkalmacen').val(),
                    'fkmaterialDetalle': h1,
                    'detallestock': [{
                        'fksubalmacen': 1,
                        'cantidad': h2
                        },
                        {
                        'fksubalmacen': 2,
                        'cantidad': h3
                        }]
                }
            }


        })(
            h0,
            h1,
            h2,
            h3))

        }


    }

    return objeto
}


function cargar_detalle(fkmaterial) {

    obj = JSON.stringify({
        'idMaterial': parseInt(JSON.parse(fkmaterial)),
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "material_listar_detalle";

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        console.log(response)
        console.log("cargar detalle")

        for (det in response.response ) {

            append_input_detalle(response.response[det]['id'])

            $('#fkdetallematerial' + response.response[det].id).val(response.response[det].id)
            $('#nombre' + response.response[det].id).val(response.response[det].material.nombre)
            $('#color' + response.response[det].id).val(response.response[det].color.nombre)
            $('#talla' + response.response[det].id).val(response.response[det].talla.nombre)


        }

    })

}

$('#new').click(function() {

    $('#detalle_div').empty()
    $('._cantidad').val('')
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
        
        objnroboleta = JSON.stringify({
             'nroboleta': $('#nroboleta').val(),
        })
    
        ajax_call_get('stock_nroboleta',{
            _xsrf: getCookie("_xsrf"),
            object: objnroboleta
        },function(response){

            if(response.success){
                objeto = JSON.stringify({
                    'nroboleta': $('#nroboleta').val(),
                    'observacion': $('#observacion').val(),
                    'fkalmacen': $('#fkalmacen').val(),
                    'detalle': get_detalle()
                })
        
                ajax_call('stock_insert', {
                    object: objeto,
                    _xsrf: getCookie("_xsrf")
                }, null, function (response) {
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
            }else{
                Swal.fire(
                    'Error de datos.',
                    'el nro de boleta ya fue registrado con anterioridad',
                    'warning'
                )
                
            }
            
        })
        
        
        

        
        
        
        
        
    }
    else show_toast('warning', 'Por favor, ingresa todos los campos requeridos (*).');
});

function edit_item(e) {
    clean_data()
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })

    ajax_call_get('stock_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#nroboleta').val(self.nroboleta)
        $('#observacion').val(self.observacion)

        for (i in self.detalle) {
            $('#id_detalle'+self.detalle[i].fkmaterialDetalle).val(self.detalle[i].id)
            $('#cantidadBackup'+self.detalle[i].fkmaterialDetalle).val(self.detalle[i].cantidadBackup)
            $('#cantidadUsado'+self.detalle[i].fkmaterialDetalle).val(self.detalle[i].cantidadUsado)

        }

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
            'nroboleta': $('#nroboleta').val(),
            'observacion': $('#observacion').val(),
            'fkalmacen': $('#fkalmacen').val(),
            'detalle': get_detalle()
        })

        ajax_call('stock_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja la stock?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la stock?"
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

            ajax_call('stock_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente la stock?",
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

            ajax_call('stock_delete', {
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
