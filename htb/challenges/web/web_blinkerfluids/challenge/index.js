const express      = require('express');
const app          = express();
const path         = require('path');
const nunjucks     = require('nunjucks');
const routes       = require('./routes/index.js');
const Database     = require('./database');

const db = new Database('invoice.db');

app.use(express.json());
app.disable('etag');

nunjucks.configure('views', {
	autoescape: true,
	express: app
});

app.set('views', './views');
app.use('/static', express.static(path.resolve('static')));

app.use(routes(db));

app.all('*', (req, res) => {
	return res.status(404).send({
		message: '404 page not found'
	});
});

(async () => {
	await db.connect();
	await db.migrate();
	app.listen(1337, '0.0.0.0', () => console.log('Listening on port 1337'));
})();