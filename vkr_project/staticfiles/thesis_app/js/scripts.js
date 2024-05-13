//подсказки к словам
$(document).ready(function () {
    var currentPopover;
    $('.word').popover({
        html: true,
        title: 'Word Info',
        content: function () {
            return $('#wordPopoverContent').html();
        }
    });
    $('.word').click(function () {
        if (currentPopover) {
            currentPopover.popover('hide');
        }
        var word = $(this).text();
        $(this).attr('data-bs-original-title', word);
        $(this).popover('show');
        currentPopover = $(this);
    });
});

//переход с домашней страницы в раздел для чтения
document.querySelectorAll('.go-somewhere').forEach(function (button) {
    // Получаем ID текста
    var textId = button.dataset.textId;
    button.addEventListener('click', function () {
        window.location.href = "/reader_view/" + textId + "/";
    });
    button.parentElement.parentElement.addEventListener('mouseenter', function () {
        button.style.display = 'block';
    });
    button.parentElement.parentElement.addEventListener('mouseleave', function () {
        button.style.display = 'none';
    });
});