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
            DROP TABLE IF EXISTS invoices;

            CREATE TABLE invoices (
                id           INTEGER      NOT NULL PRIMARY KEY AUTOINCREMENT,
                invoice_id   VARCHAR(255) NOT NULL,
                created      VARCHAR(255) DEFAULT CURRENT_TIMESTAMP
            );

            INSERT INTO invoices (invoice_id) VALUES ('f0daa85f-b9de-4b78-beff-2f86e242d6ac');
        `);
    }
    async listInvoices() {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM invoices order by id desc');
                resolve(await stmt.all());
            } catch(e) {
                reject(e);
            }
        });
    }
    async getInvoice(id) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('SELECT * FROM invoices WHERE invoice_id = ?');
                resolve(await stmt.get(id));
            } catch(e) {
                reject(e);
            }
        });
    }

    async addInvoice(id) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('INSERT INTO invoices (invoice_id) VALUES( ? )');
                resolve(await stmt.run(id));
            } catch(e) {
                reject(e);
            }
        });
    }
    async deleteInvoice(id) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare('DELETE FROM invoices WHERE invoice_id = ?');
                resolve(await stmt.run(id));
            } catch(e) {
                reject(e);
            }
        });
    }
}

module.exports = Database;