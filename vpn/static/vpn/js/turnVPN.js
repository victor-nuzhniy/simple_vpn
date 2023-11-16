const enableVPN = document.getElementById("enableVPN");
const disableVPN = document.getElementById("disableVPN");

console.log(window.location.href, window.location.host, window.location.pathname, 3333333333)
if (Boolean(enableVPN) && !window.location.pathname.startsWith("/localhost")){
    enableVPN.setAttribute("href", "http://127.0.0.1:8001/localhost" + window.location.pathname)
};
if (Boolean(disableVPN) && window.location.pathname.startsWith("/localhost")){
    disableVPN.setAttribute("href", "http://127.0.0.1:8000" + window.location.pathname.slice(10))
}