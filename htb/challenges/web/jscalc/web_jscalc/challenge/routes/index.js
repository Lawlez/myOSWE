const path       = require('path');
const express    = require('express');
const router     = express.Router();
const Calculator = require('../helpers/calculatorHelper');

const response = data => ({ message: data });

router.get('/', (req, res) => {
	return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/calculate', (req, res) => {
	let { formula } = req.body;

	if (formula) {
		result = Calculator.calculate(formula);
		return res.send(response(result));
	}

	return res.send(response('Missing parameters'));
})

module.exports = router;

// ocd