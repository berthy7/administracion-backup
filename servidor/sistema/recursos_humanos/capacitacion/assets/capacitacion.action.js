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
            { title: "Tema", data: "tema" },
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
                    columns: [ 0, 1]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1]
                },
            }
        ],
        "order": [ [1, 'asc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '30%', targets: [1, 2, 3] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function clean_data() {
    $(class_item).val('')
}

$('.date').bootstrapMaterialDatePicker({
    format: 'DD/MM/YYYY',
    clearButton: false,
    weekStart: 1,
    locale: 'es',
    time: false
}).on('change', function (e, date) {
    $(this).parent().addClass('focused');
    eraseError(this)
});

$(".hr").inputmask("h:s",{ "placeholder": "__/__" });

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'capacitacion_list',
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
$('#fkpersonal').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

function append_input_integrante(id_in) {

        $('#integrante_div').append(
        '<div class="row">\
            <div class="col-sm-1" hidden>\
                <div class="input-group">\
                <input  id="id'+id_in+'" class="form-control integrante txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-1">\
            </div>\
            <div class="col-sm-1" hidden>\
                <div class="input-group">\
                <input  id="fkpersonal'+id_in+'" class="form-control integrante  txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-3">\
                <div class="form-line">\
                    <input id="nombre'+id_in+'" data-id="'+id_in+'" class="form-control txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-md-2 ">\
                <input id="c_'+id_in+'" type="checkbox" class="regular-checkbox big-checkbox  " data-id="1" >\
                <label for="c_'+id_in+'"></label>\
            </div>\
        </div>\
        </br>'
    )


}

function obtener_integrantes() {
        objeto = []
        objeto_inputs = $('.integrante')

        for(i=0;i<objeto_inputs.length;i+=2){
            h0 = objeto_inputs[i].value
            h1 = objeto_inputs[i+1].value


            objeto.push((function add_hours(h0,h1) {

                if (h0 ==''){
                    return {
                    'fkpersonal': h1,

                    }

                }else{
                    return {
                    'id':h0,
                    'fkpersonal': h1,
                    }
                }

            })(
                    h0,
                    h1))


        }
        return objeto
    }

function cargar_subalmacen() {

    obj = JSON.stringify({
        '_xsrf': getCookie("_xsrf")
    })

    ruta = "subalmacen_listar";
    //data.append('object', obj)
    //data.append('_xsrf',getCookie("_xsrf"))

    $.ajax({
        method: "POST",
        url: ruta,
        data: {_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function (response) {
        response = JSON.parse(response)
        console.log(response)
        for (sub in response.response ) {

            append_input_subalmacen(response.response[sub]['id'])
            $('#fksubalmacen' + response.response[sub]['id']).val(response.response[sub]['id'])
            $('#nombre' + response.response[sub]['id']).val(response.response[sub]['nombre'])
            $('#c_' + response.response[sub]['id']).prop('checked', false)

        }


    })


}

$('#fkpersonal').change(function () {
    
    append_input_integrante(parseInt(JSON.parse($('#fkpersonal').val())))
    $('#fkpersonal' + parseInt(JSON.parse($('#fkpersonal').val()))).val(parseInt(JSON.parse($('#fkpersonal').val())))
    $('#nombre' + parseInt(JSON.parse($('#fkpersonal').val()))).val($("#fkpersonal option:selected").text())
    
    $(fkpersonal).val('')
    $(fkpersonal).selectpicker('render')

});

$('#new').click(function() {
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
        objeto = JSON.stringify({
            'tema': $('#tema').val(),
            'fecha': $('#fecha').val(),
            'hora': $('#hora').val(),
            'relator': $('#hora').val(),
            'integrantes': obtener_integrantes()
        })

        ajax_call('capacitacion_insert', {
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
    }
    else show_toast('warning', 'Por favor, ingresa todos los campos requeridos (*).');
});

function edit_item(e) {
    clean_data()
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })

    ajax_call_get('capacitacion_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#tema').val(self.tema)
        $('#fecha').val(self.fecha)
        $('#hora').val(self.hora)
        $('#relator').val(self.relator)


        for (i in self.integrantes) {

            append_input_integrante(self.integrantes[i]['id'])
            $('#id' + self.integrantes[i]['id']).val(self.integrantes[i]['id'])
            $('#fkpersonal' + self.integrantes[i]['id']).val(self.integrantes[i]['fkpersonal'])
            $('#nombre' + self.integrantes[i]['id']).val(self.integrantes[i]['personal']['nombre'] +' '+self.integrantes[i]['personal']['apellidop'] + ' '+ self.integrantes[i]['personal']['apellidom'])

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
            'tema': $('#tema').val(),
            'fecha': $('#fecha').val(),
            'hora': $('#hora').val(),
            'relator': $('#hora').val(),
            'integrantes': obtener_integrantes()
        })

        ajax_call('capacitacion_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja la capacitacion?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la capacitacion?"
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

            ajax_call('capacitacion_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente la capacitacion?",
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

            ajax_call('capacitacion_delete', {
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
