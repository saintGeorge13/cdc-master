import axios from "axios";
axios.defaults.withCredentials = true;

export default {
    request
};

/**
 * @param {Object} obj 请求对象
 * @param {string} obj.url 请求路径
 * @param {string} obj.method 请求方法 
 * @param {Object} obj.queries 查询参数对象
 * @param {Object} [obj.data] 请求体
 * @param {String} obj.responseType 设置响应的数据类型。合法值：text、arraybuffer
 */
async function request(obj) {

    let result = await axios({
        method: obj.method,
        timeout: 40000,
        url: obj.url + queryObjectToString(obj.queries),
        data: obj.data,
        crossDomain: true
    });
    let data = result.data;
    return data;
}

/**
 * @param {JSON} queryObj 查询字段
 * @return {String} 格式化后的 query 字符串
 */
function queryObjectToString(queryObj) {
    let queryString = '';
    for (const key in queryObj) {
        if (queryObj[key] !== undefined && queryObj[key] !== null) queryString += `&${key}=${queryObj[key]}`;
    }
    if (queryString.length > 0) queryString = `?${queryString.slice(1)}`;
    return queryString;
}