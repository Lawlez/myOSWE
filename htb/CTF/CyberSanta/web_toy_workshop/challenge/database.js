const sqlite = require('sqlite-async');

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
			DROP TABLE IF EXISTS queries;

			CREATE TABLE IF NOT EXISTS queries (
				id         INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
				query    VARCHAR(500) NOT NULL,
				created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
			);
		`);
	}

	async addQuery(query) {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('INSERT INTO queries (query) VALUES (?)');
				resolve(await stmt.run(query));
			} catch(e) {
				reject(e);
			}
		});
	}

	async getQueries() {
		return new Promise(async (resolve, reject) => {
			try {
				let stmt = await this.db.prepare('SELECT * FROM queries');
				resolve(await stmt.all());
			} catch(e) {
				reject(e);
			}
		});
	}

}

module.exports = Database;