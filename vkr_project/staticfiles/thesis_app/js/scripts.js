document.addEventListener("DOMContentLoaded", function () {
    // Динамическое заполнение модала
    function updateModal(word, data) {
        const wordHeader = document.getElementById('wordHeader');
        const posElement = document.getElementById('pos');
        const isFormOfElement = document.getElementById('isFormOf');
        const translationElement = document.getElementById('translation');
        const word1Element = document.getElementById('word1');
        const word2Element = document.getElementById('word2');
        const attributesTable = document.getElementById('attributesTable');
        const closeButton = document.getElementById('closeButton');
        const synonymsElement = document.getElementById('synonyms');
        const fromElement = document.getElementById('from');

        // Очистка ранее отображаемого модала
        word1Element.textContent = '';
        word2Element.textContent = '';
        attributesTable.innerHTML = '';
        synonymsElement.innerHTML = '';
        fromElement.innerHTML = '';

        // Проверка и извлечение данных из data
        const words = Object.keys(data);
        if (words.length < 2) {
            console.error('Ожидалось 2 слова:', data);
            return;
        }
        const word1 = words[0];
        const word2 = words[1];
        const word1Data = data[word1];
        const word2Data = data[word2];

        // Обновление заголовка модала
        wordHeader.textContent = word1;

        // Обновление части речи и перевода
        posElement.textContent = (word1Data.isFormOf ? word1Data.isFormOf.join(', ') : word1) + ', ' +
            (word1Data.POS || 'N/A');
        translationElement.innerHTML = word1Data.isTranslationOf ? word1Data.isTranslationOf.join(', ') : 'N/A';

        word1Element.textContent = word1;
        word2Element.textContent = word2;

        // Отображение синонимов (при наличии)
        if (word1Data.isSynonym || word2Data.isSynonym) {
            const synonyms = (word1Data.isSynonym || []).concat(word2Data.isSynonym || []);
            synonymsElement.innerHTML = '<b>Синонимы:</b> ' + synonyms.join(', ');
        }

        // Отображение этимологии (при наличии)
        if (word1Data.isFrom || word2Data.isFrom) {
            const from = (word1Data.isFrom || []).concat(word2Data.isFrom || []);
            fromElement.innerHTML = '<b>Происходят от:</b> ' + from.join(', ');
        }

        // Проверка наличия свойств у слова
        const attributes = new Set([...Object.keys(word1Data), ...Object.keys(word2Data)]);
        attributes.delete('isTranslationOf');
        attributes.delete('POS');
        attributes.delete('isFormOf');
        attributes.delete('isInTable');
        attributes.delete('isSynonym');
        attributes.delete('isFrom');

        // Заполнение таблицы атрибутов
        attributes.forEach(attribute => {
            const row = document.createElement('tr');
            const attributeCell = document.createElement('td');
            attributeCell.innerHTML = attribute;
            row.appendChild(attributeCell);

            const word1ValueCell = document.createElement('td');
            word1ValueCell.textContent = word1Data[attribute] ? word1Data[attribute].join(', ') : 'N/A';
            row.appendChild(word1ValueCell);

            const word2ValueCell = document.createElement('td');
            word2ValueCell.textContent = word2Data[attribute] ? word2Data[attribute].join(', ') : 'N/A';
            row.appendChild(word2ValueCell);

            attributesTable.appendChild(row);
        });
    }

    // Обработка клика для открытия модала с данными слова по его ID
    document.querySelectorAll('.word, .open-modal').forEach(wordElement => {
        wordElement.addEventListener('click', function () {
            const word = this.getAttribute('data-word');
            const wordId = this.getAttribute('data-index');
            document.getElementById('wordIdInput').value = wordId;
            fetch(`/get_word_data/${wordId}/`)
                .then(response => response.json())
                .then(data => {
                    console.log('Получен данные для слова:', word, data);
                    updateModal(word, data);
                })
                .catch(error => console.error('НЕ получены данные для слова:', error));
        });
    });

    // Функция для показа уведомлений при взаимодействии с кнопками
    function showAlert(message, type) {
        const alertPlaceholder = document.getElementById('alertPlaceholder');
        const alertMessage = document.getElementById('alertMessage');

        alertMessage.innerText = message;
        alertPlaceholder.classList.add('show');
        alertPlaceholder.classList.add(`alert-${type}`);

        setTimeout(() => {
            alertPlaceholder.classList.remove('show');
            alertPlaceholder.classList.remove(`alert-${type}`);
        }, 3500);
    }

    // Интеграция кнопки addToDictionary и соответствующего view
    // Добавлени слова в словарь юзера
    const addToDictionaryButton = document.getElementById('addToDictionary');
    addToDictionaryButton.addEventListener('click', function () {
        const wordId = document.getElementById('wordIdInput').value;
        fetch(`/add_to_dictionary/${wordId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Функция для получения CSRF токена
            },
            credentials: 'same-origin' // Включение cookies в запрос
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Сетевая ошибка');
                }
                return response.json();
            })
            .then(data => {
                console.log('Слово было:', data);
                if (data.success) {
                    showAlert('Добавлено в словарь', 'success');
                } else {
                    showAlert(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Ошибка при добавлении в словарь:', error);
                showAlert('Уже в словаре', 'danger');
            });
    });

    // Получение CSRF-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Поповер с морфологической характеристикой слова
document.getElementById('search-button').addEventListener('click', function () {
    let word = document.getElementById('word-input').value;

    if (word) {
        fetch(`/get_word_analysis/?word=${encodeURIComponent(word)}`)
            .then(response => response.json())
            .then(data => {
                // Закрыть ранее открытых поповеров
                $('.popover').popover('dispose');

                // Создание содержимого  поповера
                let content = '';
                data.forEach(item => {
                    content += `<b>${item.token}</b><br>`;
                    content += `${item.lemma}, ${item.morphological_description['<b>Часть речи</b>']}<br>`;
                    for (let key in item.morphological_description) {
                        if (key !== '<b>Часть речи</b>' && key !== 'Полярность' && key !== '<b>Форма глагола</b>' && key !== '<b>Залог</b>') {
                            content += `${key}: ${item.morphological_description[key]}<br>`;
                        }
                    }
                    content += '<hr>';
                });

                // Присваивание модалу данных из content
                $('#popover-container').attr('data-bs-content', content);

                // Создание поповера
                var popover = new bootstrap.Popover(document.getElementById('popover-container'), {
                    placement: 'bottom',
                    content: content,
                    html: true
                });
                popover.show();

                // Позиционирование поповера под центром поля ввода
                var inputField = document.getElementById('word-input');
                var inputFieldRect = inputField.getBoundingClientRect();
                var popoverContainer = document.getElementById('popover-container');
                var popoverWidth = $('.popover').outerWidth();

                popoverContainer.style.position = 'absolute';
                popoverContainer.style.top = (inputFieldRect.bottom + window.scrollY) + 'px';
                popoverContainer.style.left = (inputFieldRect.left + window.scrollX + (inputFieldRect.width / 2) - (popoverWidth / 2)) + 'px';

                // Обработка клика вне поповера для его закрытия
                document.addEventListener('click', function (event) {
                    if (!popoverContainer.contains(event.target) && !inputField.contains(event.target)) {
                        popover.hide();
                    }
                }, { once: true });
            })
            .catch(error => console.error('Ошибка:', error));
    }
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

//яндекс форма
document.getElementById('reportErrorButton').addEventListener('click', function () {
    document.getElementById('yandexFormContainer').style.display = 'block';
});