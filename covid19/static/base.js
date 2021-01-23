$.ajaxSetup({
    url: 'http://127.0.0.1:8000/settings/',
    headers: { 'X-CSRFToken':  $("#token").val() },
    type: 'post',
    dataType: 'text',
    async: false
});

$("#top").change(function () {
    if ($(this).val() > $("#end").val()) {
        $("#top").val($("#end").val())
    };
    $.ajax({
        data: { date_top: $(this).val() }
    });
});

$("#end").change(function () {
    if ($(this).val() < $("#top").val()) {
        $("#end").val($("#top").val())
    };
    $.ajax({
        data: { date_end: $(this).val() }
    });
});

$("#continent").change(function () {
    $("#country").prop('selectedIndex', 0);
    $.ajax({
        data: { continent: $(this).val() }
    });
});

$("#country").change(function () {
    $("#continent").prop('selectedIndex', 0);
    $.ajax({
        data: { country: $(this).val() }
    });
});
