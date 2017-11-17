$(function () {
    $('.footable').footable();
    addRowToggle: false
});

$(function () {
    $('table').footable();
    $('table').trigger('footable_clear_filter');
    $('.toggle').click(function () {
        $('.toggle').toggle();
        $('table').trigger($(this).data('trigger')).trigger('footable_redraw');
    });
});

$("#checkAll").click(function () {
    $(".check").prop('checked', $(this).prop('checked'));
});