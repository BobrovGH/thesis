//подсказки к словам
$(document).ready(function () {
    // Click event handler for <w> elements
    $('w.word').click(function () {
        var word = $(this).text();
        var $this = $(this);

        // Close any open popovers
        $('.popover').popover('hide');

        // Make AJAX request to get word analysis
        $.ajax({
            url: '/get_word_analysis/',
            type: 'GET',
            data: {
                'word': word
            },
            success: function (data) {
                var analysisResult = data.analysis_result;

                // Initialize popover with new content
                var content = '';
                for (var i = 2; i < analysisResult.length; i++) {
                    content += analysisResult[i] + '<br>';
                }
                $this.popover({
                    html: true,
                    title: 'Слово: ' + analysisResult[0] + '<br> начальная форма: ' + analysisResult[1],
                    content: content,
                    trigger: 'manual' // Prevent automatic opening
                });

                // Show popover
                $this.popover('show');
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
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