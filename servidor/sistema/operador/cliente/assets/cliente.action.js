var class_item = '.item-form';
var id_table = '#data_table';

$(document).ready( function () {
    reload_table();
});
validationKeyup("modal")

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

$('#fkpersonal').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})


var fechahoy = new Date();
var hoy = fechahoy.getDate()+"/"+(fechahoy.getMonth()+1) +"/"+fechahoy.getFullYear()

document.getElementById("fecha").value=hoy


// function load_table(data_tb) {
//     var tabla = $(id_table).DataTable({
//         destroy: true,
//         data: data_tb,
//         deferRender:    true,
//         scrollCollapse: true,
//         scroller:       true,
//         columns: [
//             { title: "ID", data: "id" },
//             { title: "Nombre", data: "nombre" },
//             { title: "Turno Diurno", data: "dia",
//                 render: function(data, type, row) {
//                     a = ''
//
//                     for (var i = 0; i < Object.keys(row.personal_dia).length; i++) {
//
//                         a += '<p>' +row.personal_dia[i].personal.nombre +" " +
//                                 row.personal_dia[i].personal.apellidop +" " +
//                                 row.personal_dia[i].personal.apellidom+
//                             '<input id="enabled' + row.personal_dia[i].fkpersonal + row.personal_dia[i].id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable(this)" data-id="' + row.personal_dia[i].id + '" ' + row.check + ' ' + row.disable + '>\
//                                 <label for="enabled' + row.personal_dia[i].id + '"> </label>\
//                             </p>'
//                     }
//
//                     return a
//                 }
//
//
//             },
//             { title: "Turno Nocturno", data: "noche",
//                 render: function(data, type, row) {
//                     a = ''
//
//                     for (var i = 0; i < Object.keys(row.personal_noche).length; i++) {
//
//                         a += '<p>' +row.personal_noche[i].personal.nombre +" " +
//                                 row.personal_noche[i].personal.apellidop +" " +
//                                 row.personal_noche[i].personal.apellidom +
//                             '<input id="enabled' + row.personal_noche[i].id + '" type="checkbox" class="chk-col-indigo enabled" onclick="set_enable(this)" data-id="' + row.personal_noche[i].id + '" ' + row.check + ' ' + row.disable + '>\
//                                 <label for="enabled' + row.personal_noche[i].id + '"> </label>\
//                                 <select id="turno'+row.personal_noche[i].id+'" class="form-control detalle select_" >\
//                                         <option value="1">PRESENTE = PR</option>\
//                                         <option value="2">FRANCO = L</option>\
//                                         <option value="3">FALTA = F</option>\
//                                         <option value="4">PERMISO = X</option>\
//                                         <option value="5">BAJA MEDICA = BJM</option>\
//                                         <option value="6">VACACION = V</option>\
//                                         <option value="7">RETIRADOS = R</option>\
//                                         <option value="8">PERMISO SIN GOSE DE HABER = PSG</option>\
//                                  </select>\
//                             </p>'
//                     }
//
//                     return a
//                 }
//
//             },
//             { title: "Acciones", data: "id",
//                 render: function(data, type, row) {
//                     a = ''
//                     if (row.disable === '') {
//                         a += '\
//                             <button data-json="' + data + '"  type="button" class="btn btn-primary waves-effect" title="Editar" onclick="edit_item(this)">\
//                                 <i class="material-icons">edit</i>\
//                             </button>'
//                     }
//                     if (row.delete) {
//                         a += '\
//                             <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Eliminar" onclick="delete_item(this)">\
//                                 <i class="material-icons">clear</i>\
//                             </button>'
//                     }
//                     if (a === '') a = 'Sin permisos';
//                     return a
//                 }
//             },
//         ],
//         dom: "Bfrtip",
//         buttons: [
//             {
//                 extend: 'excelHtml5',
//                 className: 'btn btn-sm cb-btn-teal',
//                 exportOptions: {
//                     columns: [ 0, 1,2,3 ]
//                 },
//                 sheetName: 'Logs',
//             },
//             {
//                 extend: 'csvHtml5',
//                 className: 'btn btn-sm cb-btn-info',
//                 exportOptions: {
//                     columns: [ 0, 1,2,3 ]
//                 },
//             },
//             {
//                 extend: 'pdfHtml5',
//                 className: 'btn btn-sm cb-btn-red',
//                 exportOptions: {
//                     columns: [ 0, 1,2,3 ]
//                 },
//             }
//         ],
//         "order": [ [0, 'asc'] ],
//         columnDefs: [ { width: '10%', targets: [0] }, { width: '30%', targets: [1, 2, 3] } ],
//         "initComplete": function() {}
//     });
//     tabla.draw()
// }

function add_filters() {
    a_filter = []
    a_filter.push({
        column_number: 1,
        style_class: 'selectpicker show-tick',
        filter_reset_button_text: false,
        filter_default_label: "Todos"
    });

    return a_filter;
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
            { title: "Puesto", data: "nombre" },
            { title: "Turno Diurno", data: "dia",
                render: function(data, type, row) {
                    a = ''
                     a += '<p><input id="cantidadPersonal"  value="Cantidad '+ row.cantidad_personal_dia +'" type="text" minlength="4" maxlength="30" size="30" class="form-control" readonly>'
                            '</p>'
                    for (var i = 0; i < Object.keys(row.personal_dia).length; i++) {


                        a += '<p><input id="nombreInputDia'+row.personal_dia[i].id+'"  value="'+ row.personal_dia[i].fullname +'" type="text" minlength="4" maxlength="30" size="30" class="form-control" readonly>'
                            '</p>'

                        if(row.personal_dia[i].fkreemplazo){

                            $('#nombreInputDia' + row.personal_dia[i].id).addClass('color_blanco');
                            $('#nombreInputDia' + row.personal_dia[i].id).addClass('black-own');

                        }else{

                            $('#nombreInputDia' + row.personal_dia[i].id).addClass(row.personal_dia[i].color_asistencia);

                            if (row.personal_dia[i].color_asistencia == null){

                                $('#nombreInputDia' + row.personal_dia[i].id).addClass('black-own');

                            }else{

                                $('#nombreInputDia' + row.personal_dia[i].id).addClass('white-own');

                            }

                        }

                    }
                    return a
                }
            },
            { title: "Asistencia", data: "dia",
                render: function(data, type, row) {
                    a = ''
                    option_asistencias = ''

                     a += '<p><input id="cantidadPersonal2"  value="" type="text" minlength="4" maxlength="30" size="30" class="form-control borde_trasparente" readonly>'
                    '</p>'

                    for (var i = 0; i < Object.keys(row.tipo_asistencia).length; i++) {
                        option_asistencias += '<option value="'+row.tipo_asistencia[i].id+'">'+row.tipo_asistencia[i].codigo+ " : "+row.tipo_asistencia[i].nombre+'</option>'
                    }
                    for (var i = 0; i < Object.keys(row.personal_dia).length; i++) {
                        a += '<p><select id="turnodia'+row.personal_dia[i].id+'" data-puesto="'+row.id+'"  data-personal="'+row.personal_dia[i].fkpersona+'" data-turno="1" class="form-control detalle select_ select_dia" >' +option_asistencias + '</select>\
                            </p>'

                        $('#turnodia' +row.personal_dia[i].id).val(row.personal_dia[i].fkasistencia)
                        $('#turnodia' +row.personal_dia[i].id).selectpicker('refresh')

                        $('#turnodia' + row.personal_dia[i].id).addClass(row.personal_dia[i].color_asistencia);
                        $('#turnodia' + row.personal_dia[i].id).addClass('white-own');
                    }
                    return a
                }
            },
            { title: "Observacion", data: "dia",
                render: function(data, type, row) {
                    a = ''
                     a += '<p><input id="cantidadPersonal3"  value="" type="text" minlength="4" maxlength="30" size="30" class="form-control borde_trasparente" readonly>'
                    '</p>'

                    option_clientes = ''

                    for (var i = 0; i < Object.keys(row.clientes).length; i++) {
                        option_clientes += '<option value="'+row.clientes[i].id+'">'+row.clientes[i].codigo+ " : "+row.clientes[i].nombre+'</option>'
                    }
                    for (var i = 0; i < Object.keys(row.personal_dia).length; i++) {
                        a += '<p><select id="turnodiacliente'+row.personal_dia[i].id+'" data-puesto="'+row.id+'" data-personal="'+row.personal_dia[i].fkpersona+'" data-turno="1" class="form-control detalle select_ select_dia_clientes" >' +option_clientes + '</select>\
                            </p>'
                        $('#turnodiacliente' +row.personal_dia[i].id).val(row.personal_dia[i].fkreemplazo)
                        $('#turnodiacliente' +row.personal_dia[i].id).selectpicker('refresh')
                    }

                    return a
                }


            },
            { title: "Turno Nocturno", data: "noche",
                render: function(data, type, row) {
                    a = ''
                     a += '<p><input id="cantidadPersonalNocturno"  value="Cantidad '+ row.cantidad_personal_noche +'" type="text" minlength="4" maxlength="30" size="30" class="form-control" readonly>'
                    '</p>'

                    for (var i = 0; i < Object.keys(row.personal_noche).length; i++) {

                        a += '<p><input id="nombreInputNoche'+row.personal_noche[i].id+'"  value="'+row.personal_noche[i].fullname +'" type="text" minlength="4" maxlength="30" size="30" class="form-control " readonly>'
                            '</p>'


                        if(row.personal_noche[i].fkreemplazo){

                            $('#nombreInputNoche' + row.personal_dia[i].id).addClass('color_blanco');
                            $('#nombreInputNoche' + row.personal_dia[i].id).addClass('black-own');

                        }else{

                            $('#nombreInputNoche' + row.personal_noche[i].id).addClass(row.personal_noche[i].color_asistencia);

                            if (row.personal_noche[i].color_asistencia == null){

                                $('#nombreInputNoche' + row.personal_noche[i].id).addClass('black-own');
                            }else{
                                $('#nombreInputNoche' + row.personal_noche[i].id).addClass('white-own');
                            }

                        }

                    }

                    return a
                }

            },
            { title: "Asistencia", data: "noche",
                render: function(data, type, row) {
                    a = ''
                     a += '<p><input id="cantidadPersonalNocturno2"  value="" type="text" minlength="4" maxlength="30" size="30" class="form-control borde_trasparente" readonly>'
                    '</p>'
                    option_asistenciasNoche = ''

                    for (var i = 0; i < Object.keys(row.tipo_asistencia).length; i++) {

                        option_asistenciasNoche += '<option value="'+row.tipo_asistencia[i].id+'">'+row.tipo_asistencia[i].codigo+ " : "+row.tipo_asistencia[i].nombre+'</option>'

                    }

                    for (var i = 0; i < Object.keys(row.personal_noche).length; i++) {

                        a += '<p><select id="turnonoche'+row.personal_noche[i].id+'"  data-puesto="'+row.id+'"  data-personal="'+row.personal_noche[i].fkpersona+'" data-turno="2" class="form-control detalle select_ select_noche" >' +option_asistenciasNoche + '</select>\
                            </p>'

                        $('#turnonoche' +row.personal_noche[i].id).val(row.personal_noche[i].fkasistencia)
                        $('#turnonoche' +row.personal_noche[i].id).selectpicker('refresh')

                        $('#turnonoche' + row.personal_noche[i].id).addClass(row.personal_noche[i].color_asistencia);
                        $('#turnonoche' + row.personal_noche[i].id).addClass('white-own');
                    }

                    return a
                }

            },
            { title: "Observacion", data: "noche",
                render: function(data, type, row) {
                    a = ''
                     a += '<p><input id="cantidadPersonalNocturno3"  value="" type="text" minlength="4" maxlength="30" size="30" class="form-control borde_trasparente" readonly>'
                    '</p>'

                    option_clientes = ''

                    for (var i = 0; i < Object.keys(row.clientes).length; i++) {
                        option_clientes += '<option value="'+row.clientes[i].id+'">'+row.clientes[i].codigo+ " : "+row.clientes[i].nombre+'</option>'
                    }
                    for (var i = 0; i < Object.keys(row.personal_noche).length; i++) {
                        a += '<p><select id="turnonochecliente'+row.personal_noche[i].id+'" data-puesto="'+row.id+'" data-personal="'+row.personal_noche[i].fkpersona+'" data-turno="2" class="form-control detalle select_ select_dia_clientes" >' +option_clientes + '</select>\
                            </p>'
                        $('#turnonochecliente' +row.personal_noche[i].id).val(row.personal_noche[i].fkreemplazo)
                        $('#turnonochecliente' +row.personal_noche[i].id).selectpicker('refresh')
                    }

                    return a

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

        ],
        "order": [ [0, 'asc'] ],
        "pageLength": 50,
        columnDefs: [ { width: '5%', targets: [0] }, { width: '10%', targets: [1] }, { width: '20%', targets: [2] }, { width: '10%', targets: [3] }, { width: '15%', targets: [4] }, { width: '20%', targets: [5] }, { width: '10%', targets: [6] }, { width: '15%', targets: [7] } ],
        "initComplete": function() {
            // setTimeout(function() {
            //     let a_active =  [2, 3, 4, 6, 7];
            //     select_search(a_active, 'yadcf-filter--data_table-')
            // }, 1000);
            
        }
    });

    // yadcf.init(tabla, add_filters(), {
    //     cumulative_filtering: true
    // });


    tabla.draw()

    $('.select_').selectpicker({
        size: 10,
        liveSearch: true,
        liveSearchPlaceholder: 'Buscar',
        title: ' '
    })

        $('.select_dia').change(function () {

            if ($(this).val() != ""){

                objeto = JSON.stringify({
                    'fktipoausencia': $(this).val(),
                    'fkturno': $(this).attr('data-turno'),
                    'fkpersonal': $(this).attr('data-personal'),
                    'fkcliente': $(this).attr('data-puesto'),
                    'fechar': $('#fecha').val()

                })

                ajax_call('asistencia_insert', {
                    _xsrf: getCookie("_xsrf"),
                    object: objeto
                }, null, function(response) {
                    self = JSON.parse(response);

                    show_toast('success', self.message);
                    reload_table()


                })
             }
    });

        $('.select_noche').change(function () {
            
            if ($(this).val() != ""){

                objeto = JSON.stringify({
                    'fktipoausencia': $(this).val(),
                    'fkturno': $(this).attr('data-turno'),
                    'fkpersonal': $(this).attr('data-personal'),
                    'fkcliente': $(this).attr('data-puesto'),
                    'fechar': $('#fecha').val()

                })

                ajax_call('asistencia_insert', {
                    _xsrf: getCookie("_xsrf"),
                    object: objeto
                }, null, function(response) {
                    self = JSON.parse(response);

                    show_toast('success', self.message);
                    reload_table()

                })
             }
    });


        $('.select_dia_clientes').change(function () {

            if ($(this).val() != ""){

                objeto = JSON.stringify({
                    'fkreemplazo': $(this).val(),
                    'fktipoausencia': 1,
                    'fkturno': $(this).attr('data-turno'),
                    'fkpersonal': $(this).attr('data-personal'),
                    'fkcliente': $(this).attr('data-puesto'),
                    'fechar': $('#fecha').val()

                })

                ajax_call('asistencia_insert', {
                    _xsrf: getCookie("_xsrf"),
                    object: objeto
                }, null, function(response) {
                    self = JSON.parse(response);

                    show_toast('success', self.message);
                    reload_table()

                })
             }


    });

        $('.select_noche_clientes').change(function () {

            if ($(this).val() != ""){

                objeto = JSON.stringify({
                    'fkreemplazo': $(this).val(),
                    'fktipoausencia': 1,
                    'fkturno': $(this).attr('data-turno'),
                    'fkpersonal': $(this).attr('data-personal'),
                    'fkcliente': $(this).attr('data-puesto'),
                    'fechar': $('#fecha').val()

                })

                ajax_call('asistencia_insert', {
                    _xsrf: getCookie("_xsrf"),
                    object: objeto
                }, null, function(response) {
                    self = JSON.parse(response);

                    show_toast('success', self.message);
                    reload_table()
                })
             }
    });


}


function clean_data() {
    $(class_item).val('')
    $('#personal_dia_div').empty()
    $('#personal_noche_div').empty()

}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'cliente_list',
        dataType: 'json',
        data: {_xsrf: getCookie("_xsrf")},
        async: false,
        success: function (response) {
            load_table(response.data)
            document.getElementById("fecha").value=hoy
        },
        error: function (jqXHR, status, err) {
            show_message(jqXHR.responseText, 'danger', 'remove');
        }
    });
}

function reload_table_fecha(fecha) {
    objeto = JSON.stringify({
        'fecha': fecha
    })
    ajax_call('cliente_list_fecha', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function (response) {


        load_table(response.data)
    })
}


$('#new_personal_dia').click(function() {
    append_input_personal_dia('')
});

$('#new_personal_noche').click(function() {
    append_input_personal_noche('')
});

$('#fecha').change(function() {
    reload_table_fecha($('#fecha').val())


})


$('#fkpersonal').change(function () {

    if (parseInt($('#fkpersonal').val()) != 0){
            append_input_personal(parseInt(JSON.parse($('#fkpersonal').val())))
            $('#idpersonal' + parseInt(JSON.parse($('#fkpersonal').val()))).val(parseInt(JSON.parse($('#fkpersonal').val())))
            $('#nombrepersonal' + parseInt(JSON.parse($('#fkpersonal').val()))).val($("#fkpersonal option:selected").text())

            $(fkpersonal).val('')
            $(fkpersonal).selectpicker('render')
    }else{
        $('#personal_div').empty()
    }



});

function obtener_personales() {
        objeto = []

        objeto_inputs = $('.personal_dia')
        objeto_inputs_noche = $('.personal_noche')


        for(i=0;i<objeto_inputs.length;i+=3){
            h0 = objeto_inputs[i].value
            h1 = objeto_inputs[i+2].value

            objeto.push((function add_hours(h0,h1) {

                if (h0 ==''){
                    return {
                    'fkpersonal': h1,
                    'fkturno': 1

                    }

                }else{
                    return {
                    'id':h0,
                    'fkpersonal': h1,
                    'fkturno': 1
                    }
                }

            })(
                    h0,
                    h1))


        }

        for(i=0;i<objeto_inputs_noche.length;i+=3){
            h0 = objeto_inputs_noche[i].value
            h1 = objeto_inputs_noche[i+2].value

            objeto.push((function add_hours(h0,h1) {

                if (h0 ==''){
                    return {
                    'fkpersonal': h1,
                    'fkturno': 2

                    }

                }else{
                    return {
                    'id':h0,
                    'fkpersonal': h1,
                    'fkturno': 2
                    }
                }

            })(
                    h0,
                    h1))


        }


        return objeto
    }


function append_input_personal(id_in) {

        $('#personal_div').append(
        '<div class="row">\
            <div class="col-sm-1" hidden>\
                <div class="input-group">\
                <input  id="idpersonal'+id_in+'" class="form-control personal_reporte txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-4">\
                <div class="form-line">\
                    <input id="nombrepersonal'+id_in+'" data-id="'+id_in+'" class="form-control txta-own"readonly>\
                </div>\
            </div>\
            <div class="col-sm-1">\
                <button type="button" class="btn bg-red waves-effect white-own clear_personal" title="Eliminar">\
                    <i class="material-icons">clear</i>\
                </button>\
            </div>\
        </div>\
        </br>'
    )

        $('.clear_personal').last().click(function () {
        $(this).parent().parent().remove()
    })


}

function obtener_personal() {
        objeto = []
        objeto_inputs = $('.personal_reporte')

        for(i=0;i<objeto_inputs.length;i+=1){
            h0 = objeto_inputs[i].value

            objeto.push(parseInt(h0))


        }

        return objeto
    }


$('#new').click(function() {

    clean_data()
    verif_inputs('')
    validationInputSelects("modal")
    $('.item-form').parent().removeClass('focused')

    $('#update').hide()
    $('#insert').show()
});


$('#generar_reporte').click(function () {
    $('#exportar_excel').show()


    obj = JSON.stringify({
        'fecha-inicio-reporte': $('#fecha-inicio-reporte').val(),
        'fecha-fin-reporte': $('#fecha-fin-reporte').val(),
        'personal': obtener_personal(),
    })

    ruta = "/asistencia_reporte_excel";
    $.ajax({
        method: "POST",
        url: ruta,
        data:{_xsrf: getCookie("_xsrf"), object: obj},
        async: false
    }).done(function(response){
        response = JSON.parse(response)

        if (response.success) {
            $('#link_excel').attr('href', response.response.url).html(response.response.nombre)
        }
    })
    // $('#modal-rep-xls').modal('show')
})


$('#reporte').click(function() {
    


    $('#exportar_excel').hide()
    $('#personal_div').empty()

    $('#fecha-inicio-reporte').val($('#fecha').val())
    $('#fecha-fin-reporte').val($('#fecha').val())

    

});

$('#insert').on('click', function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {
        objeto = JSON.stringify({
            'nombre': $('#nombre').val(),
            'codigo': $('#codigo').val(),
            'personales': obtener_personales()
        })

        ajax_call('cliente_insert', {
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

    ajax_call_get('cliente_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#nombre').val(self.nombre)
        $('#codigo').val(self.codigo)


        for (i in self.personales) {

            if(self.personales[i]['fkturno'] == 1){
                append_input_personal_dia(self.personales[i]['id'])
                $('#id_dia'+ self.personales[i]['id']).val(self.personales[i]['id'])
                $('#fkpersonaldia'+ self.personales[i]['id']).val(self.personales[i]['fkpersonal'])
                $('#fkpersonaldia'+ self.personales[i]['id']).selectpicker('refresh')
            }else{
                append_input_personal_noche(self.personales[i]['id'])
                $('#id_noche'+self.personales[i]['id']).val(self.personales[i]['id'])
                $('#fkpersonalnoche'+self.personales[i]['id']).val(self.personales[i]['fkpersonal'])
                $('#fkpersonalnoche'+self.personales[i]['id']).selectpicker('refresh')
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
            'codigo': $('#codigo').val(),
            'personales': obtener_personales()
        })

        ajax_call('cliente_update', {
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
        cb_title = "¿Está seguro de que desea dar de baja la cliente?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la cliente?"
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

            ajax_call('cliente_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente la cliente?",
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

            ajax_call('cliente_delete', {
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
