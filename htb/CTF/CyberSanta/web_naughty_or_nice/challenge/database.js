const sqlite = require('sqlite-async');
const crypto = require('crypto');
const adminPass = crypto.randomBytes(69).toString('hex');

class Database {
	constructor(db_file) {
		this.db_file = db_file;
		this.db = undefined;
	}
	
	async connect() {
		this.db = await sqlite.open(this.db_file);
	}

	async migrate() {
		return this.db.exec(`
			DROP TABLE IF EXISTS users;

			CREATE TABLE IF NOT EXISTS users (
				id		 INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				username   VARCHAR(255) NOT NULL UNIQUE,
				password   VARCHAR(255) NOT NULL
			);
			
			INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '${adminPass}');

			DROP TABLE IF EXISTS nice_or_naughty;

			CREATE TABLE IF NOT EXISTS nice_or_naughty (
				id		 INTEGER	  NOT NULL PRIMARY KEY AUTOINCREMENT,
				elf_name  VARCHAR(255) NOT NULL,
				type	VARCHAR(255) NOT NULL
			);
			
			INSERT OR IGNORE INTO nice_or_naughty (elf_name, type) VALUES ('Alabaster Snowball', 'naughty');
			INSERT OR IGNORE INTO nice_or_naughty (elf_name, type) VALUES ('Bushy Evergreen', 'naughty');
			INSERT OR IGNORE INTO nice_or_naughty (elf_name, type) VALUES ('Pepper Minstix', 'naughty');
			INSERT OR IGNORE INTO nice_or_naughty (elf_name, type) VALUES ('Shinny Upatree', 'naughty');
			INSERT OR IGNORE INTO nice_or_naughty (elf_name, type) VALUES ('Sugarplum Mary', 'naughty');
			INSERT OR IGNORE INTO nice_or_naughty (elf_name, type) VALUES ('Wunorse Openslae', 'naughty');
		`);
	}

	async registerUser(user, pass) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('INSERT INTO users (username, password) VALUES ( ?, ?)');
				resolve((await stmt.run(user, pass)));
			} catch(e) {
				reject(e);
			}
		});
	}

	async loginUser(user, pass) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT username FROM users WHERE username = ? and password = ?');
				resolve(await stmt.get(user, pass));
			} catch(e) {
				reject(e);
			}
		});
	}

	async getUser(user) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT * FROM users WHERE username = ?');
				resolve(await stmt.get(user));
			} catch(e) {
				reject(e);
			}
		});
	}

	async listNames() {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT * FROM nice_or_naughty');
				resolve(await stmt.all());
			} catch(e) {
				reject(e);
			}
		});
	}


	async editName(elf_name, type, editelf_id) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('UPDATE nice_or_naughty SET elf_name = ?, type = ? WHERE id = ?');
				resolve(await stmt.run(elf_name, type, editelf_id));
			} catch(e) {
				reject(e);
			}
		});
	}

}

module.exports = Database;