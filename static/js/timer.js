
const socket = new WebSocket('ws://' + window.location.host + '/ws/placar/');

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const pointsA = document.getElementById('points-a');
    const pointsB = document.getElementById('points-b');
    const teamA = document.getElementById('team-a');
    const teamB = document.getElementById('team-b');
    const photoA = document.getElementById('photo-team-a')
    const photoB = document.getElementById('photo-team-b')
    const photoAB = document.getElementById('photo-team-a-b')
    const photoBB = document.getElementById('photo-team-b-b')
    
    if (pointsA) pointsA.textContent = data.points_a;
    if (pointsB) pointsB.textContent = data.points_b;
    if (teamA) teamA.textContent = data.team_a;
    if (teamB) teamB.textContent = data.team_b;
    if (photoA) photoA.src = data.photoA;
    if (photoB) photoB.src = data.photoB;
    if (photoAB) photoAB.src = data.photoA;
    if (photoBB) photoBB.src = data.photoB;

    console.log("Atualização recebida", data);
    
};


socket.onclose = function(e) {
    console.error('WebSocket fechado com código: ' + e.code);
};