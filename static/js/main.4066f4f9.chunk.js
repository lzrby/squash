(this["webpackJsonpleaderboard-ui"]=this["webpackJsonpleaderboard-ui"]||[]).push([[0],[,,,function(e){e.exports=JSON.parse('[{"name":"opagrek","rating":1649,"sets":20,"sets_won":18,"prev_rating":1649},{"name":"lucky_looser","rating":1638,"sets":213,"sets_won":164,"prev_rating":1584},{"name":"vanyann","rating":1573,"sets":48,"sets_won":34,"prev_rating":1573},{"name":"klicunou","rating":1484,"sets":117,"sets_won":70,"prev_rating":1484},{"name":"drapegnik","rating":1464,"sets":37,"sets_won":23,"prev_rating":1464},{"name":"bg_grab","rating":1432,"sets":124,"sets_won":49,"prev_rating":1437},{"name":"vladdeykun","rating":1365,"sets":22,"sets_won":8,"prev_rating":1365},{"name":"lisouski","rating":1311,"sets":33,"sets_won":9,"prev_rating":1311},{"name":"unikalas","rating":1285,"sets":54,"sets_won":15,"prev_rating":1285},{"name":"rubanau","rating":1281,"sets":48,"sets_won":17,"prev_rating":1281},{"name":"uladbohdan","rating":1238,"sets":61,"sets_won":13,"prev_rating":1287},{"name":"iraborsch","rating":1080,"sets":79,"sets_won":8,"prev_rating":1080}]')},function(e,a,n){e.exports=n(10)},,,,,function(e,a,n){},function(e,a,n){"use strict";n.r(a);var t=n(0),r=n.n(t),s=n(2),l=n.n(s),i=(n(9),n(3)),o={up:"\u25b2",down:"\u25bc"},c=function(e){var a=e.value;if(!a)return r.a.createElement("span",null);var n=a>0?"up":"down",t=o[n];return r.a.createElement("span",{className:"delta-value__".concat(n)},Math.abs(a),t)},m=function(e){var a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:0,n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:120,t=e/100*(n-a),r=a+t;return"hsl(".concat(r,", 80%, 50%)")},_=function(e){var a=e.name,n=e.rating,t=e.sets,s=e.sets_won,l=n-e.prev_rating,i=Math.floor(s/t*100);return r.a.createElement("div",{className:"list__person"},r.a.createElement("img",{className:"person__image",src:"".concat("/squash","/avatars/").concat(a,".jpg"),alt:a}),r.a.createElement("div",{className:"person__row"},r.a.createElement("div",{className:"person__row__name"},a),r.a.createElement("div",{className:"person__row__sets"},r.a.createElement("span",{title:"sets played"},r.a.createElement("span",{role:"img","aria-labelledby":"games"},"\ud83c\udfcf"),": ",t),","," ",r.a.createElement("span",{title:"win rate"},r.a.createElement("span",{role:"img","aria-labelledby":"win rate"},"\ud83e\udd47"),": ",r.a.createElement("span",{style:{color:m(i)}},i,"%")))),r.a.createElement("div",{className:"person__rating"},r.a.createElement("span",{className:"person__rating-value"},n),r.a.createElement("div",{className:"person__rating-delta"},r.a.createElement(c,{value:l}))))},g=function(){return r.a.createElement("div",{className:"header"},r.a.createElement("img",{className:"header__icon",src:"".concat("/squash","/cup.png"),alt:"logo"}),r.a.createElement("h1",{className:"header__title"},"SQUASH",r.a.createElement("span",null,"LEADERBOARD")))},p=function(){return r.a.createElement("div",{className:"app"},r.a.createElement(g,null),r.a.createElement("div",{className:"list"},i.map((function(e){return r.a.createElement(_,Object.assign({key:e.name},e))}))))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));l.a.render(r.a.createElement(p,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}],[[4,1,2]]]);
//# sourceMappingURL=main.4066f4f9.chunk.js.map