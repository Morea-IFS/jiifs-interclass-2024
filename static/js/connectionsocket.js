
const socket = new WebSocket('ws://' + window.location.host + '/ws/placar/');

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.getElementById('points-a').textContent = data.points_a;
    document.getElementById('points-b').textContent = data.points_b;
    console.log("CCHEGOUUUUUUUUUUUUUUUUUU");
};

socket.onclose = function(e) {
    console.error('WebSocket fechado com código: ' + e.code);
};


