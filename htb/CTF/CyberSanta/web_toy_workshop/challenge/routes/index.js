const express        = require('express');
const router         = express.Router();
const bot            = require('../bot');

let db;

const response = data => ({ message: data });

router.get('/', (req, res) => {
	return res.render('index');
});

router.post('/api/submit', async (req, res) => {

		const { query } = req.body;
		if(query){
			return db.addQuery(query)
				.then(() => {
					bot.readQueries(db);
					res.send(response('Your message is delivered successfully!'));
				});
		}
		return res.status(403).send(response('Please write your query first!'));
});

router.get('/queries', async (req, res, next) => {
	if(req.ip != '127.0.0.1') return res.redirect('/');

	return db.getQueries()
		.then(queries => {
			res.render('queries', { queries });
		})
		.catch(() => res.status(500).send(response('Something went wrong!')));
});

module.exports = database => { 
	db = database;
	return router;
};