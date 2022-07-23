import axios from 'axios'
import { getToken } from '@/utils/auth'
import store from "@/store"
import { MessageBox, Message } from 'element-ui'

// axios instance
const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API,
    timeout: 5000
})

// 请求
service.interceptors.request.use(

    config => {
        if (store.getters.token) {
            const token = getToken()
            var username = token
            var password = ''
            var credentials = btoa(username + ':' + password);
            var basicAuth = 'Basic ' + credentials;
            config.headers['Authorization']  = basicAuth
        }
        return config

    },
    error => {
        console.log(error)
        return Promise.reject(error)

    }
)

// 响应
service.interceptors.response.use(
    response => {
        const res = response.data
        console.log("==========" + res.code)
        console.log("==========" + res.data)
        console.log("==========" + res.msg)


        if (res.code !== 0) {
            Message({
                message: res.msg || "error",
                type: "error",
                duration: 5 * 1000
            })
            return Promise.reject(new Error(res.msg || "error"))
        } else {
            return res
        }

    },
    error => {
        console.log('err' + error) // for debug
        Message({
            message: error.message,
            type: 'error',
            duration: 5 * 1000
        })
        return Promise.reject(error)
    }

)


export default service