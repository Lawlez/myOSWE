$(document).ready(() => {
    $('#submit-btn').on('click', submit);
});

const elf_info = (elf_id) => {
    inst = $('[data-remodal-id=modal]').remodal();
    inst.open();
    $('#elfavatar').attr('src',`/static/images/elf${elf_id}.png`);
    $('#elfname').text((elf_id == 1) ? 'Lhoris Farrie' : 'Ievis Chaeqirelle');
}

const submit = async () => {
    $('#submit-btn').prop('disabled', true);

	// prepare alert
	let card = $('#resp-msg');
	card.attr('class', 'alert alert-info');
	card.hide();

	// validate
	let query = $('#query').val();
	if ($.trim(query) === '') {
		$('#submit-btn').prop('disabled', false);
		card.text('Please input your query first!');
		card.attr('class', 'alert alert-danger');
		card.show();
		return;
	}

	await fetch('/api/submit', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({query: query}),
		})
		.then((response) => response.json()
			.then((resp) => {
				card.attr('class', 'alert alert-danger');
				if (response.status == 200) {
					card.attr('class', 'alert alert-success');
				}
				card.text(resp.message);
				card.show();
			}))
		.catch((error) => {
			card.text(error);
			card.attr('class', 'alert alert-danger');
			card.show();
		});

        $('#submit-btn').prop('disabled', false);
}