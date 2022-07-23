import { getToken, setToken } from "@/utils/auth";
import { login, getUserInfo } from "@/api/user";


const state = {
    token: getToken(),
    id: "",
    departmentID: "",
    username: "",
    avatar: "",
    phone: "",
    email: "",
    gender: "",
    isAdmin: "",
    tag: ""

}

const mutations = {
    SET_TOKEN: (state, token) => {
        state.token = token
    },
    SET_INFO: (state, info) => {
        const { username, avatar, departmentID, email, gender, id, phone, isAdmin, tag } = info
        state.username = username
        state.avatar = avatar
        state.departmentID = departmentID
        state.email = email
        state.gender = gender
        state.isAdmin = isAdmin
        state.id = id
        state.phone = phone
        state.tag = tag

    }
}

const actions = {
    //login
    login({ commit }, userInfo) {
        const { username, password } = userInfo
        return new Promise((res, rej) => {
            login({ username: username.trim(), password: password }).then(response => {
                const { data } = response
                commit('SET_TOKEN', data)
                setToken(data)
                res()

            }).catch(error => {
                rej(error)
            })
        })
    },

    //get info
    getUserInfo({ commit, state }) {
        return new Promise((res, rej) => {
            getUserInfo(state.token).then(response => {
                const { data } = response
                commit('SET_INFO', data)
                res(data)
            }).catch(error => {
                rej(error)
            })
        })
    },
    // // user logout
    // logout({ commit, state, dispatch }) {
    //     return new Promise((resolve, reject) => {
    //         logout(state.token).then(() => {
    //             commit('SET_TOKEN', '')
    //             removeToken()
    //             resetRouter()
    //             // reset visited views and cached views
    //             // to fixed https://github.com/PanJiaChen/vue-element-admin/issues/2485
    //           //  dispatch('tagsView/delAllViews', null, { root: true })
    //             resolve()
    //         }).catch(error => {
    //             reject(error)
    //         })
    //     })
    // },
    //   // remove token
    // resetToken({ commit }) {
    //     return new Promise(resolve => {
    //     commit('SET_TOKEN', '')
    //     removeToken()
    //     resolve()
    //     })
    // },
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}