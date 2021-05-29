var class_item = '.item-form';
var id_table = '#data_table';
var elem_password = document.getElementById('clavesecreta')

$(document).ready( function () {

});
validationKeyup("modal")

$(function () {

});



$('#cont-eye').on('click', function () {
    if ($(this).html() === 'visibility') {
        $(elem_password).attr('type', 'text')
        $(this).html('visibility_off')
    } else {
        $(elem_password).attr('type', 'password')
        $(this).html('visibility')
    }
});



$('#actualizarClave').click(function () {

    objeto = JSON.stringify({
        'clavesecreta': $('#clavesecreta').val(),
    })
    ajax_call('ajuste_update', {
        object: objeto,
        _xsrf: getCookie("_xsrf")
    }, null, function () {
        show_msg_lg('success', self.message, 'center')

    })

})
