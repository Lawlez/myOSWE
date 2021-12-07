const JWTHelper = require('../helpers/JWTHelper');

module.exports = async (req, res, next) => {

	if (req.cookies.session === undefined) {
		if (!req.is('application/json')) return res.redirect('/');
		return res.status(401).json({ status: 'unauthorized', message: 'Authentication expired, please login again!' });
	}
	return JWTHelper.verify(req.cookies.session)
		.then(username => {
			req.data = username;
			next();
		})
		.catch((e) => {
			console.log(e);
			res.redirect('/logout');
		});
   
}