var class_item = '.item-form';
var id_table = '#data_table';

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

$('#fktipo').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
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
            { title: "Tipo", data: "tipo" },
            { title: "Nombre", data: "nombre" },
            { title: "Cant. Backup", data: "cantidadBackup" },
            { title: "Cant. Usado", data: "cantidadUsado" },
            { title: "Cant. Descarte", data: "cantidadDescarte" },
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
                    columns: [ 0, 1,2 ]
                },
                sheetName: 'Logs',
            },
            {
                extend: 'csvHtml5',
                className: 'btn btn-sm cb-btn-info',
                exportOptions: {
                    columns: [ 0, 1,2 ]
                },
            },
            {
                extend: 'pdfHtml5',
                className: 'btn btn-sm cb-btn-red',
                exportOptions: {
                    columns: [ 0, 1,2 ]
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
        url: 'material_list',
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
    $('.div_cantidad').hide()
})

function get_detalle() {
    objeto = []
    objeto_inputs = $('.detalle')
    cant_ = 0

    for (i = 0; i < objeto_inputs.length; i += 5) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 2].value
        h2 = objeto_inputs[i + 4].value


        objeto.push((function add_(h0, h1, h2) {

            if (h0 ==''){
                return {
                    'fkcolor': h1,
                    'fktalla': h2

                }

            }else{
                return {
                'id':h0,
                'fkcolor': h1,
                'fktalla': h2
                }
            }


        })(
            h0,
            h1,
            h2))
    }

    return objeto
}

$('#new').click(function() {
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
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'fktipo': $('#fktipo').val(),
            'detalle': get_detalle()
        })

        ajax_call('material_insert', {
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

    ajax_call_get('material_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;
        $('.div_cantidad').show()
        $('#id').val(self.id)
        $('#nombre').val(self.nombre)
        $(fktipo).val(self.fktipo)
        $(fktipo).selectpicker('render')
        $('#detalle_div').empty()
        for (i in self.detalle) {

            append_input_detalle(self.detalle[i].id)
            $('#id_detalle'+self.detalle[i].id).val(self.detalle[i].id)
            $('#fkcolor'+self.detalle[i].id).val(self.detalle[i].fkcolor)
            $('#fkcolor'+self.detalle[i].id).selectpicker('render')
            $('#fktalla'+self.detalle[i].id).val(self.detalle[i].fktalla)
            $('#fktalla'+self.detalle[i].id).selectpicker('render')

            for (mat in self.detalle[i].materialdetallestock){

                // if (self.detalle[i].materialdetallestock[mat].fkalmacen == 1){
                //     $('#cantidadBackup'+self.detalle[i].id).val(self.detalle[i].materialdetallestock[mat].cantidad)
                // }
                // if (self.detalle[i].materialdetallestock[mat].fkalmacen == 2){
                //     $('#cantidadUsado'+self.detalle[i].id).val(self.detalle[i].materialdetallestock[mat].cantidad)
                // }
                // if (self.detalle[i].materialdetallestock[mat].fkalmacen == 3){
                //     $('#cantidadDescarte'+self.detalle[i].id).val(self.detalle[i].materialdetallestock[mat].cantidad)
                // }

                switch(self.detalle[i].materialdetallestock[mat].fkalmacen) {
                  case 1:
                    $('#cantidadBackup'+self.detalle[i].id).val(self.detalle[i].materialdetallestock[mat].cantidad)
                    break;
                  case 2:
                    $('#cantidadUsado'+self.detalle[i].id).val(self.detalle[i].materialdetallestock[mat].cantidad)
                    break;
                  case 3:
                    $('#cantidadDescarte'+self.detalle[i].id).val(self.detalle[i].materialdetallestock[mat].cantidad)
                    break;
                  default:
                    // code block
                }


            }

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
            'nombre': $('#nombre').val(),
            'fktipo': $('#fktipo').val(),
            'detalle': get_detalle()
        })

        ajax_call('material_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja la material?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la material?"
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

            ajax_call('material_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente la material?",
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

            ajax_call('material_delete', {
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
