(window.webpackJsonp=window.webpackJsonp||[]).push([[0],[,,,function(e){e.exports=[{name:"klicunou",rating:1648,sets:35,prev_rating:1648},{name:"lucky_looser",rating:1552,sets:89,prev_rating:1373},{name:"Drapegnik",rating:1426,sets:29,prev_rating:1396},{name:"uladbohdan",rating:1362,sets:6,prev_rating:1362},{name:"VladDeykun",rating:1358,sets:10,prev_rating:1400},{name:"BG_grab",rating:1281,sets:66,prev_rating:1281},{name:"iraborsch",rating:1174,sets:25,prev_rating:1341}]},function(e,a,n){e.exports=n(11)},,,,,,function(e,a,n){},function(e,a,n){"use strict";n.r(a);var t=n(0),r=n.n(t),s=n(2),c=n.n(s),l=(n(10),n(3)),i={up:"\u25b2",down:"\u25bc"},o=function(e){var a=e.value;if(!a)return r.a.createElement("span",null);var n=a>0?"up":"down",t=i[n];return r.a.createElement("span",{className:"delta-value__".concat(n)},t,Math.abs(a))},m=function(e){var a=e.name,n=e.rating,t=e.sets,s=n-e.prev_rating;return r.a.createElement("div",{className:"list__person"},r.a.createElement("img",{className:"person__image",src:"".concat("/squash","/avatars/").concat(a,".jpg"),alt:a}),r.a.createElement("p",{className:"person__name"},a),r.a.createElement("div",{className:"person__rating"},r.a.createElement("span",{className:"person__rating-value"},n),r.a.createElement("div",{className:"person__rating-stats"},r.a.createElement(o,{value:s})," ",r.a.createElement("span",{className:"person__sets"},"(",t,")"))))},u=function(){return r.a.createElement("div",{className:"header"},r.a.createElement("img",{className:"header__icon",src:"".concat("/squash","/cup.png"),alt:"logo"}),r.a.createElement("h1",{className:"header__title"},"Squash",r.a.createElement("span",null,"Leaderboard")))},p=function(){return r.a.createElement("div",{className:"app"},r.a.createElement(u,null),r.a.createElement("div",{className:"list"},l.map(function(e){return r.a.createElement(m,Object.assign({key:e.name},e))})))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(r.a.createElement(p,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}],[[4,1,2]]]);
//# sourceMappingURL=main.226f116f.chunk.js.map