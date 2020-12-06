
const crypto = require("crypto");
const http = require("http");
const axios = require("axios").default;
const httpAgent = new http.Agent({ keepAlive: true });

const loadData = async () => {
  try {
    const response = await axios.get("http://144.126.206.242:32609",{httpAgent});
    console.log(response.data);
    const PAGE = response.data;
    var x = "<h3 align='center'>";
    var y = "</h3>";
    const string = PAGE.substring(
      PAGE.indexOf(x) + x.length,
      PAGE.lastIndexOf(y)
    )
console.log('string',string)
    const md5 = (data) => crypto.createHash("md5").update(string).digest("hex");
 const hash = md5(string)
console.log('MD%',hash);

const response2 = await axios({
			method: 'post', 
			url: "http://144.126.206.242:32609",
			headers:{'Content-Type':'application/x-www-form-urlencoded',
				'Cookie':'PHPSESSID=ilimcjsspls1p1qpnhlbdbf6o6'}, 
			body:`hash=${hash}`, 
			httpAgent});

console.log(response2.data)
 } catch (error) {
    console.error(error);
  }
};

loadData();
