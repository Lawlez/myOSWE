const crypto = require("crypto");
const http = require("http");
const axios = require("axios").default;
const httpAgent = new http.Agent({ keepAlive: true });

const loadData = async () => {
  try {
    const response = await axios.get("http://144.126.206.242:32609", {
      httpAgent,
    });

    const PAGE = response.data;
    const x = "<h3 align='center'>";
    const y = "</h3>";
    const string = PAGE.substring(
      PAGE.indexOf(x) + x.length,
      PAGE.lastIndexOf(y)
    );

    console.log("recieved string: ", string);
    const md5 = (data) => crypto.createHash("md5").update(data).digest("hex");
    const hash = md5(string);
    console.log("new MD: ", hash);

    const response2 = await axios({
      method: "post",
      url: "http://127.0.0.1:32609",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Cookie: "PHPSESSID=ilimcjsspls1p1qpnhlbdbf6o6",
      },
      data: `hash=${hash}`,
      //go through burp proxy
      proxy: {
        host: "127.0.0.1",
        port: 8080,
      },
      httpAgent,
    });

    console.log(response2.data);
  } catch (error) {
    console.error(error);
  }
};

loadData();
