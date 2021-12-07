const jwt = require('jsonwebtoken');
const NodeRSA = require('node-rsa');

const keyPair = new NodeRSA({b: 512}).generateKeyPair();
const publicKey = keyPair.exportKey('public')
const privateKey = keyPair.exportKey('private')

module.exports = {
	async sign(data) {
		data = Object.assign(data, {pk:publicKey});
		return (await jwt.sign(data, privateKey, { algorithm:'RS256' }))
	},
	async verify(token) {
		return (await jwt.verify(token, publicKey, { algorithms: ['RS256', 'HS256'] }));
	}
}