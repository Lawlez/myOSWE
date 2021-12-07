const fs             = require('fs');
const path           = require('path');
const express        = require('express');
const router         = express.Router();
const AuthMiddleware = require('../middleware/AuthMiddleware');
const JWTHelper      = require('../helpers/JWTHelper');
const CardHelper     = require('../helpers/CardHelper');

let db;

const response = data => ({ message: data });

router.get('/', (req, res) => {
	return db.listNames()
		.then(elfList => {
			return CardHelper.generateCard(elfList)
				.then(cardHTML => {
					return res.send(cardHTML);
				})
				.catch(() => res.status(500).send(response('Something went wrong!')));
		});
});

router.get('/login', (req, res) => {
	return res.render('login.html');
});

router.get('/register', (req, res) => {
	return res.render('register.html');
});

router.get('/dashboard', AuthMiddleware, async (req, res) => {
	return db.getUser(req.data.username)
		.then(user => {
			if(user.username == 'admin') return res.render('admin.html');
			res.render('dashboard.html', { user });
		})
		.catch(() => res.status(500).send(response('Something went wrong!')));
});

router.post('/api/login', async (req, res) => {
	const { username, password } = req.body;

	if (username && password) {
		return db.loginUser(username, password)
			.then(user => {
				JWTHelper.sign({ username: user.username })
					.then(token => {
						res.cookie('session', token, { maxAge: 43200000 });
						res.send(response('User authenticated successfully!'));
					})
			})
			.catch(() => res.status(403).send(response('Invalid username or password!')));
	}
	return res.status(500).send(response('Missing parameters!'));
});

router.post('/api/register', async (req, res) => {
	const { username, password } = req.body;

	if (username && password) {
		return db.getUser(username)
			.then(user => {
				if (user) return res.status(401).send(response('This username is already registered!'));
				return db.registerUser(username, password)
					.then(()  => res.send(response('Account registered successfully!')))
			})
			.catch(() => res.status(500).send(response('Something went wrong!')));
	}
	return res.status(401).send(response('Please fill out all the required fields!'));
});

router.get('/api/elf/list', AuthMiddleware, (req, res) => {
	return db.getUser(req.data.username)
		.then(user => {
			if(user.username != 'admin') return res.status(403).send(response('Access denied'));
			return db.listNames()
				.then(elfList => {
					return res.json(elfList);
				});
		})
		.catch(() => res.status(500).send(response('Something went wrong!')));
});

router.post('/api/elf/edit', AuthMiddleware, async (req, res) => {
	return db.getUser(req.data.username)
		.then(user => {
			if(user.username != 'admin') return res.status(403).send(response('Access denied'));
			const {elf_name, type, editelf_id} = req.body;
			if (elf_name, type, editelf_id) {
				if (type != 'nice' && type != 'naughty') return res.status(403).send(response('The type has to be either "nice" or "naughty"!'));
				return db.editName(elf_name, type, editelf_id)
					.then(() => res.send(response('Elf details updated successfully!')))
					.catch(() => res.status(500).send(response('Something went wrong, please try again!')));
			}
			res.status(403).send(response('Missing required parameters, make sure to fill out all the fields!'));
		})
		.catch(() => res.status(500).send(response('Something went wrong!')));
});


router.get('/logout', (req, res) => {
	res.clearCookie('session');
	return res.redirect('/');
});

module.exports = database => { 
	db = database;
	return router;
};