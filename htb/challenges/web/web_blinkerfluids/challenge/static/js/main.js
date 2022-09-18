$(document).ready(function() {
	listInvoice();
	$('#create-btn').on('click', showForm);
	$('#save-btn').on('click', addInvoice);
	window.easyMDE = new EasyMDE({element: $('#markdown_content')[0], renderingConfig: {singleLineBreaks: false}});
});

const showForm = () => {
	$('#invoices_view').hide();
	$('#markdown_view').slideDown();
}

const populateTable = (data) => {
	tRow = `<tr>
				<td>${data.invoice_id}</td>
				<td>${data.created}</td>
				<td><a href="/static/invoices/${data.invoice_id}.pdf" target="_blank">PDF</a></td>
				<td><a href="#" onclick="removeInvoice('${data.invoice_id}')">Delete</a></td>
			</tr>`;
	$('#invoice-list').append(tRow);
}

const listInvoice = async () => {
	await fetch('/api/invoice/list', {
		method: 'GET'
	})
	.then((response) => response.json()
		.then((data) => {
			if (response.status == 200) {
				for (let row of data) {
					populateTable(row);
				}
				return;
			}
		}))
	.catch((error) => {
		console.log(error);
	});
};

const removeInvoice = async (invoice_id) => {
	await fetch('/api/invoice/delete', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({invoice_id}),
	})
	.then((response) => {
		location.reload();
	})
	.catch((error) => {
		console.log(error);
	});
}

const addInvoice = async () => {

	$('#save-btn').prop('disabled', true);

	let card = $('#resp-msg');
	card.hide();

	let loading = $('#loading_view');
	loading.show();
	$('.pdf_frame').hide();

	let markdown_content = window.easyMDE.value();

	if ($.trim(markdown_content) === '') {
		$('#save-btn').prop('disabled', false);
		card.text('Please add some content first!');
		card.attr('class', 'alert alert-danger');
		card.show();
		loading.hide();
		return;
	}

	await fetch('/api/invoice/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({markdown_content}),
		})
		.then((response) => response.json()
			.then((data) => {
				if (response.status == 200) {
					window.setTimeout(function() {
						loading.hide();
						location.reload();
						}, 2500);
						return;
				} else {
					loading.hide();
					card.text(data.message);
					card.attr('class', 'alert alert-danger');
					card.show();
				}
			}))
		.catch((error) => {
			loading.hide();
			card.text(error);
			card.attr('class', 'alert alert-danger');
			card.show();
		});
}


