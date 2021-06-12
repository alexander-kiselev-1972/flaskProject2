let caravans = document.querySelectorAll('form.caravan-price');

for (let i = 0; i < caravans.length; i++) {
    caravans[i].addEventListener('click', function (event) {
        let caravan_price = caravans[i].parentNode.querySelector('span.p-price');
        let base_price = parseInt(caravan_price.innerText);
        let price_input = caravans[i].querySelector("input[name='price']");

        if (event.target.tagName.toLowerCase() === 'input') {

            if (event.target.type === 'checkbox') {
                if (event.target.checked === true) {
                    event.target.value = 'on';
                    base_price += parseInt(event.target.dataset.price);
                } else {
                    event.target.value = 'off';
                    base_price -= parseInt(event.target.dataset.price);
                }
                caravan_price.innerText = base_price;
            }

            if (event.target.type === 'radio') {
                event.target.addEventListener('change', function () {
                    if (event.target.checked === true) {

                        if (event.target.value === 'with-chassis') {
                            if ((caravans[i].querySelector("input[name='parking_brake']").checked === true) && (caravans[i].querySelector("input[name='spare_tire']").checked === true)) {
                                base_price += parseInt(event.target.dataset.price) + parseInt(caravans[i].querySelector("input[name='parking_brake']").dataset.price) + parseInt(caravans[i].querySelector("input[name='spare_tire']").dataset.price);
                            } else if (caravans[i].querySelector("input[name='parking_brake']").checked === true) {
                                base_price += parseInt(event.target.dataset.price) + parseInt(caravans[i].querySelector("input[name='parking_brake']").dataset.price);
                            } else if (caravans[i].querySelector("input[name='spare_tire']").checked === true) {
                                base_price += parseInt(event.target.dataset.price) + parseInt(caravans[i].querySelector("input[name='spare_tire']").dataset.price);
                            } else {
                                base_price += parseInt(event.target.dataset.price);
                            }
                            caravans[i].querySelector("input[name='parking_brake']").removeAttribute('disabled');
                            caravans[i].querySelector("input[name='spare_tire']").removeAttribute('disabled');
                        }

                        if (event.target.value === 'no-chassis') {
                            if ((caravans[i].querySelector("input[name='parking_brake']").checked === true) && (caravans[i].querySelector("input[name='spare_tire']").checked === true)) {
                                base_price = base_price - parseInt(caravans[i].querySelector("input[name='parking_brake']").dataset.price) - parseInt(caravans[i].querySelector("input[name='spare_tire']").dataset.price) - parseInt(caravans[i].querySelector("input[value='with-chassis']").dataset.price);
                            } else if (caravans[i].querySelector("input[name='parking_brake']").checked === true) {
                                base_price = base_price - parseInt(caravans[i].querySelector("input[name='parking_brake']").dataset.price) - parseInt(caravans[i].querySelector("input[value='with-chassis']").dataset.price);
                            } else if (caravans[i].querySelector("input[name='spare_tire']").checked === true) {
                                base_price = base_price - parseInt(caravans[i].querySelector("input[name='spare_tire']").dataset.price) - parseInt(caravans[i].querySelector("input[value='with-chassis']").dataset.price);
                            } else {
                                base_price -= parseInt(caravans[i].querySelector("input[value='with-chassis']").dataset.price);
                            }
                            caravans[i].querySelector("input[name='parking_brake']").setAttribute('disabled', 'true');
                            caravans[i].querySelector("input[name='spare_tire']").setAttribute('disabled', 'true');
                        }

                    }
                    caravan_price.innerText = base_price;
                    price_input.value = base_price;
                });
            }

        }
        price_input.value = base_price;

        if (event.target.tagName.toLowerCase() === 'button') {

            let colors = document.querySelectorAll('.color-block');

            for (let i = 0; i < colors.length; i++) {
                colors[i].addEventListener('click', function (event) {
                    if (event.target.tagName.toLowerCase() === 'input') {
                        if (event.target.type === 'radio') {
                            event.target.addEventListener('change', function () {
                                for (let j = 0; j < colors.length; j++) {
                                    colors[j].querySelector('.color-img').classList.remove('selected');
                                }

                                if (event.target.checked === true) {
                                    event.target.parentNode.querySelector('.color-img').classList.add('selected');
                                    //get data name from modal
                                    let color_name = event.target.getAttribute('data-name');
                                    //confirm button
                                    let confirm = document.querySelector('#chooseColor .modal-footer button');
                                    let id_modal = confirm.getAttribute('data-id');

                                    let inputColor = caravans[id_modal].querySelector("input[name='color']");
                                    let buttonColor = caravans[id_modal].querySelector('button.btn-choose-color');

                                    confirm.addEventListener('click', function () {
                                        inputColor.value = event.target.value;
                                        buttonColor.innerText = 'Color: ' + color_name;
                                    });
                                }

                            });
                        }
                    }
                });
            }

        }

    });
}

$(document).ready(function () {
    let input_checked_options = document.querySelector("input[name='checked_options']");
    if (input_checked_options) {
        let checked_options = input_checked_options.value;
        if (checked_options[0] === '&') {
            checked_options = checked_options.substring(1);
        }
        let arr_options = (checked_options).split('&');
        for (let i = 0; i < arr_options.length; i++) {

            if (arr_options[i].includes('color=')) {
                let value_color = arr_options[i].substr(6);
                let inputColor = document.querySelector("input[name='color']");
                inputColor.value = value_color;
                let radio_color = document.querySelector("#chooseColor input[value='" + value_color +"']");
                let color_text = radio_color.getAttribute('data-name');
                let buttonColor = document.querySelector('button.btn-choose-color');
                buttonColor.innerText = 'Color: ' + color_text;
            }

            if (arr_options[i] === 'with-chassis') {
                document.querySelector("input[value='" + arr_options[i] + "']").setAttribute('checked', 'checked');
                document.querySelector("input[name='parking_brake']").removeAttribute('disabled');
                document.querySelector("input[name='spare_tire']").removeAttribute('disabled');
            } else if (arr_options[i] === 'no-chassis') {
                document.querySelector("input[value='" + arr_options[i] + "']").setAttribute('checked', 'checked');
                document.querySelector("input[name='parking_brake']").setAttribute('disabled', 'true');
                document.querySelector("input[name='spare_tire']").setAttribute('disabled', 'true');
            }

            let checked_input = document.querySelector("input[name='" + arr_options[i] + "']");
            if (checked_input) {
                checked_input.setAttribute('checked', 'checked');
                checked_input.addEventListener('change', function () {
                    if (checked_input.hasAttribute('checked')) {
                        checked_input.removeAttribute('checked');
                    } else {
                        checked_input.setAttribute('checked', 'checked');
                    }
                });
            }
        }
    }

    $(document).on('click', '.btn-choose-color', function () {
        //get modal id
        let id_modal = $(this).attr('data-id_modal');
        let color_check = $(this).closest('ul').find("[name='color']").val();

        $('.color-img').removeClass('selected');
        $('.color-radio').prop('checked', false);

        //if !empty color we check on modal
        if(color_check) {
            $(".color-block :input[value=" + color_check + "]").closest('.color-block').find(".color-img").addClass('selected');
        }
        //set id in button
        $('.confirm-color-button').attr('data-id', id_modal);
    });
});