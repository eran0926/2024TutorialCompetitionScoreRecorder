msg = [[2401, 5, 50, 10], [2402, 8 , 50, 10], [2403, 8, 45, 5], [2404, 8, 50, 20]]

// socket = io.coneect("/leaderboard");

// socket.on("connect", () => {
//     console.log("Connected to server");
// })

// socket.on("all_commited", function (msg) {
//     msg.sort(sortFuntion);
//     table = document.getElementById("leaderboard");
//     table.innerHTML = "";
//     msg.forEach((element, index) => {
//         table.innerHTML += "<tr><td>" + toString(index+1) + "</td><td>" + element[0] + "</td><td>" + element[1] + "</td><td>" + element[2] + "</td></tr>";
//     });
    
// })


msg.sort(sortFuntion);
table = document.getElementById("leaderboard");
table.innerHTML = "";
msg.forEach(function(element, index)  {
    tr = document.createElement("tr");
    td = document.createElement("td");
    td.setAttribute("scope", "row");
    td.appendChild(document.createTextNode(index+1));
    tr.appendChild(td);
    element.forEach(function (value) {
        td = document.createElement("td");
        td.appendChild(document.createTextNode(value));
        tr.appendChild(td);
    })
    table.appendChild(tr);
    // console.log(element);
    // console.log(index);
    // table.innerHTML += "<tr><td>" + (index+1).toString() + "</td><td>" + element[0] + "</td><td>" + element[1] + "</td><td>" + element[2] + "</td></tr>";
});

function sortFuntion(a, b) {
    for (let i = 1; i < a.length ; i++){
        if (a[i] == b[i]){
            continue;
        } else {
            return(a[0]<b[0] ? -1 : 1);
            break;
        }
    }
}