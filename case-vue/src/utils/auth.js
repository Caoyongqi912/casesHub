import Cookies from "js-cookie"

const TOKENKEY = "CASEHUB-KEY"

/**
 * get TOKEN
 */
export function getToken(){
    
    return Cookies.get(TOKENKEY)
}
/**
 * set TOKEN
 * @param {str} token 
 */
export function setToken(token){
    return Cookies.set(TOKENKEY,token)
}

/**
 * remove TOKEN
 */
export function removeToken(){
    return Cookies.remove(TOKENKEY)
}