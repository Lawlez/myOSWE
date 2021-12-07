const express       = require('express');
const app           = express();
const path          = require('path');
const routes        = require('./routes');
const Database      = require('./database');

const db = new Database('toy_workshop.db');

app.use(express.json());

app.set("view engine", "hbs");
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