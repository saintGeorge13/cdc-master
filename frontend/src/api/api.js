import Network from "../plugins/network";

const baseUrl = "http://118.31.41.159:5000/";

import axios from "axios";
// import echart from "../plugins/echart";
axios.defaults.withCredentials = true;


export default {
    getdata,
    getLine,
    getBar,
    register,
    login,
    postData,
    download,
    postFile
}

async function getdata(queries) {
    const res = await Network.request({
        url: baseUrl + "hotspotmap_json/",
        method: "get",
        queries
    });
    return res;
}
async function getLine(queries) {
    return Network.request({
        url: baseUrl + "linechart_json/",
        method: "get",
        queries
    })
}

async function getBar(queries) {
    return Network.request({
        url: baseUrl + "barchart_json/",
        method: "get",
        queries
    })
}

async function register(data) {
    return Network.request({
        url: baseUrl + "register/",
        method: "post",
        data: data
    })
}

async function login(data) {
    return Network.request({
        url: baseUrl + "login/",
        method: "post",
        data:data
    })
}

async function postData(data) {
    return Network.request({
        url: baseUrl + "data_update/",
        method: "post",
        config: {
            headers: {
                'Content-Type': 'application/json'
            }
        },
        data: data
    })
}

async function download(data) {
    axios({
        url: baseUrl + "download_data/",
        method: 'POST',
        data: data,
        responseType: 'blob', //指定返回数据格式
    }).then(res => {
        // 将二进制数据流转成URL对象
        const url = window.URL.createObjectURL(
            new Blob([res.data], {
                type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8',
            }),
        );
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'download.csv'); // 需要指定文件格式。
        document.body.appendChild(link);
        link.click(); //点击事件
    });
}

function postFile(data) {
    const formData = new FormData();
    formData.append("file", data);
    let request = new XMLHttpRequest();
    request.open("POST", baseUrl + "upload_data/");
    request.send(formData);
}