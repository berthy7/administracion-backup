var class_item = '.item-form';
var id_table = '#data_table';
accion = "nuevo"

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

function load_table(data_tb) {
    var tabla = $(id_table).DataTable({
        destroy: true,
        data: data_tb,
        deferRender:    true,
        scrollCollapse: true,
        scroller:       true,
        columns: [
            { title: "ID", data: "id" },
            { title: "Fecha Ingreso", data: "fechar" },
            { title: "Cargo", data: "cargo" },
            { title: "Nombre", data: "fullname" },
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
                    if (row.delete) {
                        a += '\
                            <button data-json="' + data + '"  type="button" class="btn btn-danger waves-effect" title="Reporte" onclick="reporte_item(this)">\
                                <i class="material-icons">picture_as_pdf</i>\
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
        "order": [ [3, 'asc'] ],
        columnDefs: [ { width: '10%', targets: [0] }, { width: '30%', targets: [1, 2, 3] } ],
        "initComplete": function() {}
    });
    tabla.draw()
}

function clean_data() {
    $('#familiar_div').empty()
    $('#laboral_div').empty()
    $('#estudio_div').empty()
    $('#complemento_div').empty()
    $(class_item).val('')
}

function reload_table() {
    $.ajax({
        method: "POST",
        url: 'personal_list',
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

$('#fkcargo').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})


$('#fknacionalidad').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkregimiento').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})


$('#fkexpedido').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkcategoriavehiculo').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkcategoriamotocicleta').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fkcivil').selectpicker({
    size: 10,
    liveSearch: true,
    liveSearchPlaceholder: 'Buscar',
    title: 'Seleccione'
})

$('#fechanacimiento').change(function() {
        objeto = JSON.stringify({
            'fechanacimiento': $('#fechanacimiento').val()
        })
        ajax_call('personal_edad', {
            object: objeto,
            _xsrf: getCookie("_xsrf")
        }, null, function (response) {

            response = JSON.parse(response);


            $('#edad').val(response.response)


            if (parseInt(response.response) < 18){
                show_msg_lg('error', 'No se cumple con la edad minima 18 años', 'center')
            }


        })



})

$('#serviciomilitar').change(function() {


    if($('#serviciomilitar').val()== "Si"){
        $('#div_servicio_militar').show()

    }else{
        $('#div_servicio_militar').hide()

    }

})

$('#serviciomilitar').change(function() {

    if($('#serviciomilitar').val() == "Si"){

        // $('#div_residente').hide()
        // $('#div_invitacion').show()
        // $('#div_datos_visita').show()
        $('#fkregimiento').prop("required", true);
        
    }else{
        $('#nrolibreta').val('')

        $(fkregimiento).val('')
        $(fkregimiento).selectpicker('render')
        
       $('#fkregimiento').removeAttr("required");
        eraseError('fkregimiento')



    }

})

document.getElementById("tab-personal").click();

    $('#tab-personal').click(function () {
        $('#body-personal').css("display", "block")
        $('#body-administrativos').css("display", "none")
        $('#body-estudios').css("display", "none")
        $('#body-documentos').css("display", "none")

        if (accion == "nuevo"){
            $('#siguiente1').show()
            $('#siguiente2').hide()
            $('#siguiente3').hide()
        }else{
            $('#siguiente1').hide()
            $('#siguiente2').hide()
            $('#siguiente3').hide()
        }
    })
    $('#tab-administrativos').click(function () {
        $('#body-personal').css("display", "none")
        $('#body-administrativos').css("display", "block")
        $('#body-estudios').css("display", "none")
        $('#body-documentos').css("display", "none")

        $('#div_buscar_administrativos').hide()
        $('#div_cancelar_administrativos').hide()
        $('#div_agregar_administrativos').show()

        if (accion == "nuevo"){
            $('#siguiente1').hide()
            $('#siguiente2').show()
            $('#siguiente3').hide()
        }else{
            $('#siguiente1').hide()
            $('#siguiente2').hide()
            $('#siguiente3').hide()
        }
    })
    $('#tab-estudios').click(function () {
        $('#body-personal').css("display", "none")
        $('#body-administrativos').css("display", "none")
        $('#body-estudios').css("display", "block")
        $('#body-documentos').css("display", "none")

        $('#div_buscar_estudios').hide()
        $('#div_cancelar_estudios').hide()
        $('#div_agregar_estudios').show()

        if (accion == "nuevo"){
            $('#siguiente1').hide()
            $('#siguiente2').hide()
            $('#siguiente3').show()
        }else{
            $('#siguiente1').hide()
            $('#siguiente2').hide()
            $('#siguiente3').hide()
        }

    })
    $('#tab-documentos').click(function () {
        $('#body-personal').css("display", "none")
        $('#body-administrativos').css("display", "none")
        $('#body-estudios').css("display", "none")
        $('#body-documentos').css("display", "block")



        if (accion == "nuevo"){
            $('#insert').show()
            $('#siguiente1').hide()
            $('#siguiente2').hide()
            $('#siguiente3').hide()
        }else{
            $('#update').show()
            $('#siguiente1').hide()
            $('#siguiente2').hide()
            $('#siguiente3').hide()
        }

    })

    $('#switch').change(function() {
       sw = $(this).prop('checked')

   })


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


$('#siguiente1').click(function () {
    document.getElementById("tab-administrativos").click();
    $('#body-personal').css("display", "none")
    $('#body-administrativos').css("display", "block")
    $('#body-estudios').css("display", "none")
    $('#body-documentos').css("display", "none")

    $('#siguiente1').hide()
    $('#siguiente2').show()
    $('#siguiente3').hide()


})

$('#siguiente2').click(function () {
    document.getElementById("tab-estudios").click();
    $('#body-personal').css("display", "none")
    $('#body-administrativos').css("display", "none")
    $('#body-estudios').css("display", "block")
    $('#body-documentos').css("display", "none")

    $('#siguiente1').hide()
    $('#siguiente2').hide()
    $('#siguiente3').show()


})

$('#siguiente3').click(function () {
    document.getElementById("tab-documentos").click();
    $('#body-personal').css("display", "none")
    $('#body-administrativos').css("display", "none")
    $('#body-estudios').css("display", "none")
    $('#body-documentos').css("display", "block")

    $('#siguiente1').hide()
    $('#siguiente2').hide()
    $('#siguiente3').hide()
    $('#insert').show()

})

function get_administrativos() {
    objeto = []
        h0 = $('#id_adminitrativo').val(),
        h1 = $('#serviciomilitar').val(),
        h2 = $('#nrolibreta').val(),
        h3 = $('#fkregimiento').val()

    objeto.push((function add_(h0, h1, h2,h3) {

        if (h0 ==''){
            return {
                'serviciomilitar': h1,
                'nrolibreta': h2,
                'fkregimiento': h3

            }

        }else{
            return {
            'id':h0,
            'serviciomilitar': h1,
            'nrolibreta': h2,
            'fkregimiento': h3
            }
        }

                })(
            h0,
            h1,
            h2,h3))

    return objeto
}

$('#new_familiar').click(function () {
    append_input_familiar('')
})

function get_familiares() {
    objeto = []
    objeto_inputs = $('.familiar')
    cant_ = 0

    for (i = 0; i < objeto_inputs.length; i += 5) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 4].value

        objeto.push((function add_(h0, h1, h2,h3) {

            if (h0 ==''){
                return {
                    'nombre': h1,
                    'celular': h2,
                    'fkparentesco': h3

                }

            }else{
                return {
                'id':h0,
                    'nombre': h1,
                    'celular': h2,
                    'fkparentesco': h3
                }
            }


        })(
            h0,
            h1,
            h2,
            h3))
    }



    return objeto
}

$('#new_estudio').click(function () {
    append_input_estudio('')
})

function get_estudio() {
    objeto = []
    objeto_inputs = $('.estudio')
    cant_ = 0

    for (i = 0; i < objeto_inputs.length; i += 5) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 3].value
        h3 = objeto_inputs[i + 4].value

        objeto.push((function add_(h0, h1, h2,h3) {

            if (h0 ==''){
                return {
                    'institucion': h1,
                    'fkgrado': h2,
                     'egreso': h3

                }

            }else{
                return {
                'id':h0,
                'institucion': h1,
                'fkgrado': h2,
                 'egreso': h3
                }
            }


        })(
            h0,
            h1,
            h2,
            h3))
    }



    return objeto
}

$('#new_laboral').click(function () {
    append_input_laboral('')
})

function get_laboral() {
    objeto = []
    objeto_inputs = $('.laboral')
    cant_ = 0

    for (i = 0; i < objeto_inputs.length; i += 8) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 2].value
        h3 = objeto_inputs[i + 4].value
        h4 = objeto_inputs[i + 5].value
        h5 = objeto_inputs[i + 6].value
        h6 = objeto_inputs[i + 7].value

        objeto.push((function add_(h0, h1, h2,h3,h4,h5,h6) {

            if (h0 ==''){
                return {
                    'institucion': h1,
                    'duracion': h2,
                    'fkretiro': h3,
                    'cargo': h4,
                    'telefono': h5,
                    'referencia': h6


                }

            }else{
                return {
                'id':h0,
                    'institucion': h1,
                    'duracion': h2,
                    'fkretiro': h3,
                    'cargo': h4,
                    'telefono': h5,
                    'referencia': h6
                }
            }


        })(
            h0,
            h1,
            h2,h3,h4,h5,h6))
    }

    return objeto
}

$('#new_complemento').click(function () {
    append_input_complemento('')
})

function get_complemento() {
    objeto = []
    objeto_inputs = $('.complemento')
    cant_ = 0

    for (i = 0; i < objeto_inputs.length; i += 4) {
        h0 = objeto_inputs[i].value
        h1 = objeto_inputs[i + 1].value
        h2 = objeto_inputs[i + 3].value

        objeto.push((function add_(h0, h1, h2) {

            if (h0 ==''){
                return {
                    'estudio': h1,
                    'fkgrado': h2

                }

            }else{
                return {
                'id':h0,
                'estudio': h1,
                'fkgrado': h2
                }
            }


        })(
            h0,
            h1,
            h2))
    }


    return objeto
}


function limpiar_formulario(){
    $('#apellidop').val('')
    $('#apellidom').val('')
    $('#nombre').val('')
    $('#ci').val('')
    $('#edad').val('')

    $('#fkexpedido').val('')
    $('#fkexpedido').selectpicker('refresh')

    $('#fknacionalidad').val('')
    $('#fknacionalidad').selectpicker('refresh')

    $('#fechanacimiento').val('')

    $('#licenciavehiculo').val('')
    $('#fkcategoriavehiculo').val('')
    $('#fkcategoriavehiculo').selectpicker('refresh')

    $('#licenciamotocicleta').val('')
    $('#fkcategoriamotocicleta').val('')
    $('#fkcategoriamotocicleta').selectpicker('refresh')

    $('#domicilio').val('')
    $('#telefono').val('')
    $('#fkcivil').val('')
    $('#fkcivil').selectpicker('refresh')

    $('#id_adminitrativo').val('')
    $('#serviciomilitar').val('Si')
    $('#serviciomilitar').selectpicker('refresh')
    $('#nrolibreta').val('')
    $('#expedido').val('')


    $('#familiar_div').empty()
    $('#laboral_div').empty()
    $('#estudio_div').empty()
    $('#complemento_div').empty()



    $('#foto').fileinput('clear');
    $('.fotos').fileinput('clear');
    document.getElementById("imagen_show_img").src = "/resources/images/no_photo.png";


}

$('#importar_Excel').click(function () {
    $(".xlsfl").each(function () {
        $(this).fileinput('refresh',{
            allowedFileExtensions: ['xlsx', 'txt'],
            maxFileSize: 2000,
            maxFilesNum: 1,
            showUpload: false,
            layoutTemplates: {
                main1: '{preview}\n' +
                    '<div class="kv-upload-progress hide"></div>\n' +
                    '<div class="input-group {class}">\n' +
                    '   {caption}\n' +
                    '   <div class="input-group-btn">\n' +
                    '       {remove}\n' +
                    '       {cancel}\n' +
                    '       {browse}\n' +
                    '   </div>\n' +
                    '</div>',
                main2: '{preview}\n<div class="kv-upload-progress hide"></div>\n{remove}\n{cancel}\n{browse}\n',
                preview: '<div class="file-preview {class}">\n' +
                    '    {close}\n' +
                    '    <div class="{dropClass}">\n' +
                    '    <div class="file-preview-thumbnails">\n' +
                    '    </div>\n' +
                    '    <div class="clearfix"></div>' +
                    '    <div class="file-preview-status text-center text-success"></div>\n' +
                    '    <div class="kv-fileinput-error"></div>\n' +
                    '    </div>\n' +
                    '</div>',
                icon: '<span class="glyphicon glyphicon-file kv-caption-icon"></span>',
                caption: '<div tabindex="-1" class="form-control file-caption {class}">\n' +
                    '   <div class="file-caption-name"></div>\n' +
                    '</div>',
                btnDefault: '<button type="{type}" tabindex="500" title="{title}" class="{css}"{status}>{icon}{label}</button>',
                btnLink: '<a href="{href}" tabindex="500" title="{title}" class="{css}"{status}>{icon}{label}</a>',
                btnBrowse: '<div tabindex="500" class="{css}"{status}>{icon}{label}</div>',
                progress: '<div class="progress">\n' +
                    '    <div class="progress-bar progress-bar-success progress-bar-striped text-center" role="progressbar" aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100" style="width:{percent}%;">\n' +
                    '        {percent}%\n' +
                    '     </div>\n' +
                    '</div>',
                footer: '<div class="file-thumbnail-footer">\n' +
                    '    <div class="file-caption-name" style="width:{width}">{caption}</div>\n' +
                    '    {progress} {actions}\n' +
                    '</div>',
                actions: '<div class="file-actions">\n' +
                    '    <div class="file-footer-buttons">\n' +
                    '        {delete} {other}' +
                    '    </div>\n' +
                    '    {drag}\n' +
                    '    <div class="file-upload-indicator" title="{indicatorTitle}">{indicator}</div>\n' +
                    '    <div class="clearfix"></div>\n' +
                    '</div>',
                actionDelete: '<button type="button" class="kv-file-remove {removeClass}" title="{removeTitle}"{dataUrl}{dataKey}>{removeIcon}</button>\n',
                actionDrag: '<span class="file-drag-handle {dragClass}" title="{dragTitle}">{dragIcon}</span>'
            }
        })
    });
    verif_inputs('')

    $('#id_div').hide()
    $('#insert-importar').show()
    $('#form-importar').modal('show')
})

$('#new').click(function() {
    clean_data()
    verif_inputs('')
    validationInputSelects("modal")
    $('.item-form').parent().removeClass('focused')

    $('#fechanacimiento').val('')
    $('#fkexpedido').val('')
    $('#fkexpedido').selectpicker('refresh')

    $('#fkcargo').val('')
    $('#fkcargo').selectpicker('refresh')
    
    $('.nfoto').hide()
    $('#div_foto').hide()
    $('#id_div').hide()
    $('#insert').hide()
    $('#update').hide()
    $('#div_nuevo_estudios').hide()
    $('#form').modal('show')
    $('#siguiente1').show()
    $('#siguiente2').hide()
    $('#siguiente3').hide()
    $('#siguiente4').hide()
    $('#div_username').hide()
    document.getElementById("tab-personal").click();

});

$('#insert').on('click', function() {
    if (parseInt($('#edad').val()) >= 18) {
        notvalid = validationInputSelectsWithReturn("modal");
        if (!notvalid) {
    
            var data = new FormData($('#form_submit')[0]);
    
            objeto = JSON.stringify({
                'apellidop': $('#apellidop').val(),
                'apellidom': $('#apellidom').val(),
                'nombre': $('#nombre').val(),
                'ci': $('#dni').val(),
                'fkexpedido': $('#fkexpedido').val(),
                'fknacionalidad': $('#fknacionalidad').val(),
                'fechanacimiento': $('#fechanacimiento').val(),
                'expendido': $('#expendido').val(),
                'licenciavehiculo': $('#licenciavehiculo').val(),
                'fkcategoriavehiculo': $('#fkcategoriavehiculo').val(),
                'licenciamotocicleta': $('#licenciamotocicleta').val(),
                'fkcategoriamotocicleta': $('#fkcategoriamotocicleta').val(),
                'domicilio': $('#domicilio').val(),
                'telefono': $('#telefono').val(),
                'fkcivil': $('#fkcivil').val(),
                'fkcargo': $('#fkcargo').val(),
    
                'administrativos' : get_administrativos(),
                'familiares' : get_familiares(),
                'experiencias' : get_laboral(),
                'estudios' : get_estudio(),
                'complementos' : get_complemento()
            })
            ruta = "personal_insert";
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
    }
    else show_msg_lg('error', 'No se cumple con la edad minima 18 años');
});

function edit_item(e) {
    clean_data()
    obj = JSON.stringify({
        'id': parseInt(JSON.parse($(e).attr('data-json')))
    })

    ajax_call_get('personal_update',{
        _xsrf: getCookie("_xsrf"),
        object: obj
    },function(response){
        var self = response.response;

        $('#id').val(self.id)
        $('#nombre').val(self.nombre)
        $('#apellidop').val(self.apellidop)
        $('#apellidom').val(self.apellidom)
        $('#sexo').val(self.sexo)
        $('#sexo').selectpicker('refresh')
        $('#dni').val(self.ci)
        $('#edad').val(self.edad)
        $('#correo').val(self.correo)
        $('#fkexpedido').val(self.fkexpedido)
        $('#fkexpedido').selectpicker('refresh')
        $('#fechanacimiento').val(self.fechanacimiento)
        $('#telefono').val(self.telefono)
        $('#fknacionalidad').val(self.fknacionalidad)
        $('#fknacionalidad').selectpicker('refresh')
        $('#licenciavehiculo').val(self.licenciavehiculo)
        $('#fkcategoriavehiculo').val(self.fkcategoriavehiculo)
        $('#fkcategoriavehiculo').selectpicker('refresh')
        $('#fkcargo').val(self.fkcargo)
        $('#fkcargo').selectpicker('refresh')

        $('#licenciamotocicleta').val(self.licenciamotocicleta)
        $('#fkcategoriamotocicleta').val(self.fkcategoriamotocicleta)
        $('#fkcategoriamotocicleta').selectpicker('refresh')

        $('#domicilio').val(self.domicilio)
        $('#fkcivil').val(self.fkcivil)
        $('#fkcivil').selectpicker('refresh')

        $('.fotos').fileinput('clear');
        

        $('#administrativos_div').empty()
        $('#estudio_div').empty()
        $('#complemento_div').empty()

        for (adm in self.administrativos) {

            $('#serviciomilitar').val(self.administrativos[adm]['serviciomilitar'])
            $('#nrolibreta').val(self.administrativos[adm]['nrolibreta'])
            $('#fkregimiento').val(self.administrativos[adm]['fkregimiento'])
            $('#fkregimiento').selectpicker('refresh')

        }


        for (fami in self.familiares) {

            append_input_familiar(self.familiares[fami]['id'])
            $('#id_familiar' + self.familiares[fami]['id']).val(self.familiares[fami]['id'])
            $('#nombre' + self.familiares[fami]['id']).val(self.familiares[fami]['nombre'])
            $('#celular' + self.familiares[fami]['id']).val(self.familiares[fami]['celular'])
            $('#fkparentesco' + self.familiares[fami]['id']).val(self.familiares[fami]['fkparentesco'])
            $('#fkparentesco' + self.familiares[fami]['id']).selectpicker('refresh')

        }

        for (expe in self.experiencias) {
            console.log(self.experiencias[expe]['institucion'])
            append_input_laboral(self.experiencias[expe]['id'])
            $('#id_laboral' + self.experiencias[expe]['id']).val(self.experiencias[expe]['id'])
            $('#institucion' + self.experiencias[expe]['id']).val(self.experiencias[expe]['institucion'])
            $('#duracion' + self.experiencias[expe]['id']).val(self.experiencias[expe]['duracion'])
            $('#fkretiro' + self.experiencias[expe]['id']).val(self.experiencias[expe]['fkretiro'])
            $('#fkretiro' + self.experiencias[expe]['id']).selectpicker('refresh')
            $('#cargo' + self.experiencias[expe]['id']).val(self.experiencias[expe]['cargo'])
            $('#telefono' + self.experiencias[expe]['id']).val(self.experiencias[expe]['telefono'])
            $('#referencia' + self.experiencias[expe]['id']).val(self.experiencias[expe]['referencia'])


        }

        for (estu in self.estudios) {

            append_input_estudio(self.estudios[estu]['id'])
            $('#id_estudio' + self.estudios[estu]['id']).val(self.estudios[estu]['id'])
            $('#instituciones' + self.estudios[estu]['id']).val(self.estudios[estu]['institucion'])
            $('#fkgrado_estudio' + self.estudios[estu]['id']).val(self.estudios[estu]['fkgrado'])
            $('#fkgrado_estudio' + self.estudios[estu]['id']).selectpicker('refresh')
            $('#egreso' + self.estudios[estu]['id']).val(self.estudios[estu]['egreso'])


        }

        for (comple in self.complementos) {

            append_input_complemento(self.complementos[comple]['id'])
            $('#id_complemento' + self.complementos[comple]['id']).val(self.complementos[comple]['id'])
            $('#estudio' + self.complementos[comple]['id']).val(self.complementos[comple]['estudio'])
            $('#fkgrado_complemento' + self.complementos[comple]['id']).val(self.complementos[comple]['fkgrado'])
            $('#fkgrado_complemento' + self.complementos[comple]['id']).selectpicker('refresh')

        }

        $('#id_documentos').val(self.documentos[0].id)

        if (self.documentos[0].ci != "None" && self.documentos[0].ci != "") {
            document.getElementById("imagen_show_img-ci").src = self.documentos[0].ci;
        } else {
            document.getElementById("imagen_show_img-ci").src = "/resources/images/sinImagen.jpg";
        }

        if (self.documentos[0].libretamilitar != "None" && self.documentos[0].libretamilitar != "") {
            document.getElementById("imagen_show_img-libretamilitar").src = self.documentos[0].libretamilitar;
        } else {
            document.getElementById("imagen_show_img-libretamilitar").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].titulobachiller != "None" && self.documentos[0].titulobachiller != "") {
            document.getElementById("imagen_show_img-titulobachiller").src = self.documentos[0].titulobachiller;
        } else {
            document.getElementById("imagen_show_img-titulobachiller").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].titulotecnico != "None" && self.documentos[0].titulotecnico != "") {
            document.getElementById("imagen_show_img-titulotecnico").src = self.documentos[0].titulotecnico;
        } else {
            document.getElementById("imagen_show_img-titulotecnico").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].titulolicenciatura != "None" && self.documentos[0].titulolicenciatura != "") {
            document.getElementById("imagen_show_img-titulolicenciatura").src = self.documentos[0].titulolicenciatura;
        } else {
            document.getElementById("imagen_show_img-titulolicenciatura").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].flcn != "None" && self.documentos[0].flcn != "") {
            document.getElementById("imagen_show_img-flcn").src = self.documentos[0].flcn;
        } else {
            document.getElementById("imagen_show_img-flcn").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].flcc != "None" && self.documentos[0].flcc != "") {
            document.getElementById("imagen_show_img-flcc").src = self.documentos[0].flcc;
        } else {
            document.getElementById("imagen_show_img-flcc").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].flcv != "None" && self.documentos[0].flcv != "") {
            document.getElementById("imagen_show_img-flcv").src = self.documentos[0].flcv;
        } else {
            document.getElementById("imagen_show_img-flcv").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].luzagua != "None" && self.documentos[0].luzagua != "") {
            document.getElementById("imagen_show_img-luzagua").src = self.documentos[0].luzagua;
        } else {
            document.getElementById("imagen_show_img-luzagua").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].certificadonacimiento != "None" && self.documentos[0].certificadonacimiento != "") {
            document.getElementById("imagen_show_img-certificadonacimiento").src = self.documentos[0].certificadonacimiento;
        } else {
            document.getElementById("imagen_show_img-certificadonacimiento").src = "/resources/images/sinImagen.jpg";
        }

                if (self.documentos[0].otros != "None" && self.documentos[0].otros != "") {
            document.getElementById("imagen_show_img-otros").src = self.documentos[0].otros;
        } else {
            document.getElementById("imagen_show_img-otros").src = "/resources/images/sinImagen.jpg";
        }

        clean_form()
        verif_inputs('')
        validationInputSelects("form")
        $('.item-form').parent().addClass('focused')
        $('#div_nuevo_estudios').hide()
        $('#div_foto').show()
        $('.nfoto').show()

        $('#insert').hide()
        $('#update').show()
        $('#modal').modal('show')

        document.getElementById("tab-personal").click();
        $('#siguiente1').hide()
        $('#siguiente2').hide()
        $('#siguiente3').hide()
        $('#siguiente4').hide()

    })
}


$('#update').on('click', function() {
    notvalid = validationInputSelectsWithReturn("modal");

    if (!notvalid) {

        var data = new FormData($('#form_submit')[0]);

        objeto = JSON.stringify({
            'id': $('#id').val(),
            'apellidop': $('#apellidop').val(),
            'apellidom': $('#apellidom').val(),
            'nombre': $('#nombre').val(),
            'ci': $('#dni').val(),
            'fkexpedido': $('#fkexpedido').val(),
            'fknacionalidad': $('#fknacionalidad').val(),
            'fechanacimiento': $('#fechanacimiento').val(),
            'expendido': $('#expendido').val(),
            'licenciavehiculo': $('#licenciavehiculo').val(),
            'fkcategoriavehiculo': $('#fkcategoriavehiculo').val(),
            'licenciamotocicleta': $('#licenciamotocicleta').val(),
            'fkcategoriamotocicleta': $('#fkcategoriamotocicleta').val(),
            'domicilio': $('#domicilio').val(),
            'telefono': $('#telefono').val(),
            'fkcivil': $('#fkcivil').val(),
            'fkcargo': $('#fkcargo').val(),
            'id_documentos': $('#id_documentos').val(),

            'administrativos' : get_administrativos(),
            'familiares' : get_familiares(),
            'experiencias' : get_laboral(),
            'estudios' : get_estudio(),
            'complementos' : get_complemento()
        })
        ruta = "personal_update";
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
        cb_title = "¿Está seguro de que desea dar de baja la personal?"
        cb_text = ""
        cb_type = "warning"
    } else {
        cb_title ="¿Está seguro de que desea dar de alta la personal?"
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

            ajax_call('personal_state', {
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
        title: "¿Está seguro de que desea eliminar permanentemente la personal?",
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

            ajax_call('personal_delete', {
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


function reporte_item(elemento){
    obj = JSON.stringify({
        'idPersonal': parseInt(JSON.parse($(elemento).attr('data-json'))),
        '_xsrf': getCookie("_xsrf")
    })

    $.ajax({
        method: "POST",
        url: '/personal_report',
        data: {object: obj, _xsrf: getCookie("_xsrf")}
    }).done(function(response){
        dictionary = JSON.parse(response)
        dictionary = dictionary.response
        servidor = ((location.href.split('/'))[0])+'//'+(location.href.split('/'))[2];
        url = servidor + dictionary;

        window.open(url)
    })
}
