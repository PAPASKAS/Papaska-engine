function fetchForm (id, eventType, _then, headers= {}) {
    document.getElementById(id).addEventListener(eventType,(event) => {
        event.preventDefault();

        headers['Content-Type'] = 'application/json;charset=utf-8';
        headers['X-CSRFToken'] = event.target.csrfmiddlewaretoken.value;

        // without whitespace from sides and to lowerCase
        for (const input of event.target) {
            if (input.name !== 'csrfmiddlewaretoken') {
                input.value = input.value.trim().toLowerCase();
            }
        }

        axios({
            method: event.target.method,
            url: event.target.action,
            data: new FormData(event.target),
            headers,
        })
            .then((res) => res.data)
            .then((res) => {
                _then(res);
            })
            .catch((err) => {
                // For dev debug
                console.log(err);

                alert(err.message + '\n' + 'Код ошибки: ' + err.response?.status + '\n' + 'Пожалуйста сообщите администратору о данной ошибке');
            });
    });
}

fetchForm('searchForm', 'submit',(res) => {
    const dns = document.querySelector('#dns .row');
    const mVideo = document.querySelector('#mVideo .row');
    const svyaznoy = document.querySelector('#svyaznoy .row');
    const bq = document.querySelector('#bq .row');

    // clear old elements
    dns.innerHTML = '';
    mVideo.innerHTML = '';
    svyaznoy.innerHTML = '';
    bq.innerHTML = '';

    // add new elements
    res.forEach((telephone) => {
        const card = get_card(telephone);
        document.querySelector('#' + telephone['shop'] + ' .row').append(card);
    })
});

fetchForm('updateDB', 'submit',(res) => {
    console.log(res);
});

function get_card(telephone) {
    const div = document.createElement('div');
    let before_discount;

    telephone['before_discount'] === null ? before_discount = '' : before_discount = `Цена без скидки: <strong>${telephone['before_discount']}</strong>`

    div.className = "card text-bg-dark col-12 col-lg-4";
    div.innerHTML = `
        <div class="card-header h4"><strong>${telephone['name']}</strong></div>
        <div class="card-body">
            <p class="card-text">
                Текущая цена: <strong>${telephone['current_price']}</strong>
                <br />
                ${before_discount}
            </p>
        </div>
    `;
//    <div class="card-footer">
//        <p class="card-text">Тип телефона: <strong>${telephone['type']}</strong></p>
//    </div>
    return div;
}
