$(document).ready(() => {
	loadElfInfo();
	$('#cancel-edit-btn').on('click', hideEdit);
	$('#update-edit-btn').on('click', editelf);
});

const loadElfInfo = async () => {

	await fetch('/api/elf/list', {
			method: 'GET',
			credentials: 'include'
		})
		.then((response) => response.json())
		.then(async (elfList) => {
			for (let elfInfo of elfList) {
				populateTable(elfInfo);			
			}
		})
		$('#loading_view').hide();
		$('#elfinfo_view').show();
		$('#elf-listing').show();
		$('#empty-table-msg').hide();
}

const populateTable = (elfInfo) => {
	rowData = `<tr id="${htmlEncode(elfInfo.id)}_row">`;
	rowData += `<td>${htmlEncode(elfInfo.elf_name)}</td>`;
	rowData += `<td>${htmlEncode(elfInfo.type)}</td>`;
	rowData += `<td>
                        <button type="button" class="btn btn-primary btn-sm btn-icon-text" onclick="showEdit('${htmlEncode(elfInfo.id)}')" id="${elfInfo.id}_vBtn">
                            <i class="mdi mdi-file-document-edit-outline btn-icon"></i>
                        </button>
                </td>
        </tr>`;

	$('#elf-listing > tbody:last-child').append(rowData);

}


const showEdit = (rowId) => {
	dataRow = $(`#${rowId}_row`);
	dataCols = ['elf_name', 'type'];
	dataRow.find('td').each((id, td) => {
		$(`#editForm input[name=${dataCols[id]}]`).val(htmlDecode($(td).text()));
	})
	$('#editForm input[name=editelf_id]').val(rowId);
	$('#elfinfo_view').hide();
	$('#editelf_view').slideDown("slow");
}

const hideEdit = () => {
	$('#elfinfo_view').slideDown();
	$('#editelf_view').hide();
}

const getFormData = ($form) => {
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};
	$.map(unindexed_array, (n, i) => {
		indexed_array[n['name']] = n['value'];
	});
	return indexed_array;
}

const editelf = async () => {
	const card = $('#edit-resp-msg');
	card.attr("class", "alert alert-info");
	card.text('Please wait...');
	card.show();
	$form = $('#editForm');
	const formData = getFormData($form);
	await fetch('/api/elf/edit', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(formData)
		})
		.then(response => response.json()
			.then(resp => {
				card.attr("class", "alert alert-danger");
				if (response.status == 200) {
					card.attr("class", "alert alert-success");
					setTimeout(() => {
						location.reload()
					}, 1000);
				}
				if (resp.hasOwnProperty('message')) {
					card.text(resp.message);
					card.show();
				}
			}))
		.catch((error) => {
			console.log(error);
		});
}


// can I haz security?
const htmlEncode = (str) => {
	return String(str).replace(/[^\w. ]/gi, function(c) {
		return '&#' + c.charCodeAt(0) + ';';
	});
}
const htmlDecode = (str) => {
	var doc = new DOMParser().parseFromString(str, "text/html");
	return doc.documentElement.textContent;
}