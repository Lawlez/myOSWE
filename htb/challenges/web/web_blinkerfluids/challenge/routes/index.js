const express        = require('express');
const router         = express.Router();
const MDHelper       = require('../helpers/MDHelper.js');

let db;

const response = data => ({ message: data });

router.get('/', async (req, res) => {
    return res.render('index.html');
});

router.get('/api/invoice/list', async (req, res) => {
	return db.listInvoices()
		.then(invoices => {
			res.json(invoices);
		})
		.catch(e => {
			res.status(500).send(response('Something went wrong!'));
		})
});

router.post('/api/invoice/add', async (req, res) => {
    const { markdown_content } = req.body;

    if (markdown_content) {
        return MDHelper.makePDF(markdown_content)
            .then(id => {
                db.addInvoice(id)
					.then(() => {
						res.send(response('Invoice saved successfully!'));
					})
					.catch(e => {
						res.send(response('Something went wrong!'));
					})
            })
            .catch(e => {
                console.log(e);
                return res.status(500).send(response('Something went wrong!'));
            })
    }
    return res.status(401).send(response('Missing required parameters!'));
});

router.post('/api/invoice/delete', async (req, res) => {
	const { invoice_id } = req.body;

	if (invoice_id) {
		return db.deleteInvoice(invoice_id)
		.then(() => {
			res.send(response('Invoice removed successfully!'))
		})
		.catch(e => {
			res.status(500).send(response('Something went wrong!'));
		})
	}

	return res.status(401).send(response('Missing required parameters!'));
});

module.exports = database => {
    db = database;
    return router;
};
