var crypto = require("crypto");
const axios = require("axios").default;

const loadData = async () => {
  try {
    const response = await axios.get("https://github.com/axios/axios");
    console.log(response.data);
    const PAGE = response.data;
    var x = "<h3>";
    var y = "</h3>";
    const string = PAGE.substring(
      PAGE.indexOf(x) + x.length,
      PAGE.lastIndexOf(y)
    );
    const md5 = (data) => crypto.createHash("md5").update(data).digest("hex");

    console.log(md5(string));
  } catch (error) {
    console.error(error);
  }
};

loadData();
