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
    // Retrieve the text ID from the data attribute
    var textId = button.parentElement.parentElement.dataset.textId;
    button.addEventListener('click', function () {
        // Redirect to the reader page with the text ID
        window.location.href = "{% url 'reader_view' text_id=textId %}";
    });
    button.parentElement.parentElement.addEventListener('mouseenter', function () {
        button.style.display = 'block';
    });
    button.parentElement.parentElement.addEventListener('mouseleave', function () {
        button.style.display = 'none';
    });
});