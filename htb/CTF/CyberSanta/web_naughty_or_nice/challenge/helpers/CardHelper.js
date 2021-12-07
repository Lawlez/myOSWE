const nunjucks   = require('nunjucks');

module.exports = {
	async generateCard(elfList) {
		return new Promise(async (resolve, reject) => {
			try {
				let NaughtyNames = NiceNames = '<br>';
				for(elfData of elfList) {
					if (elfData.type == 'naughty') {
						NaughtyNames = `${NaughtyNames}\n${elfData.elf_name}<br>`;
					}
					else if (elfData.type == 'nice') {
						NiceNames = `${NiceNames}\n${elfData.elf_name}<br>`;
					}
				}
				card = `
					{% extends "card.html" %}
					{% block card %}
					<div class="card">
						<div class="card-page cart-page-front">
							<div class="card-page cart-page-outside"></div>
							<div class="card-page cart-page-inside">
							<p><span class='nheader green'>Nice List</span>
								${NiceNames}
							</p>
							</div>
						</div>
						<div class="card-page cart-page-bottom">
							<p><span class='nheader red'>Naughty List</span>
								${NaughtyNames}
							</p>
						</div>
					</div>
					{% endblock %}
				`;
				resolve(nunjucks.renderString(card));
			} catch(e) {
				reject(e);
			}
		})
	}
};