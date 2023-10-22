
// Message/Notification timer

var message_timeout = document.getElementById("message-timer");

setTimeout(function()

{

    message_timeout.style.display = "none";


}, 5000);


$(function () {
    $('#start_date_picker, #end_date_picker').datetimepicker({
        format: 'YYYY-MM-DDTHH:mm:ss',
        showClear: true,
        icons: {
            time: 'fa fa-clock',
            date: 'fa fa-calendar',
            up: 'fa fa-chevron-up',
            down: 'fa fa-chevron-down',
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            clear: 'fa fa-trash',
            close: 'fa fa-times'
        }
    });
});








