function trocarTextoLabel() {
    const label = document.getElementById("label-foto");
    const input = document.getElementById("fotos");

    // Se um arquivo for selecionado, muda o texto do label
    if (input.files.length > 0) {
        label.innerHTML = "Imagem carregada";
    } else {
        // Se nenhum arquivo estiver selecionado, volta para o texto padrão
        label.innerHTML = "Adicione uma imagem";
    }
}

function toggle_checkbox(source) {
    checkboxes = document.getElementsByName("input-checkbox");
    for (i = 0, n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
}

function search_table() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search-input");
    filter = input.value.toUpperCase();
    table = document.getElementById("search-table");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) {
        // Começa em 1 para pular o cabeçalho
        tr[i].style.display = "none"; // Oculta a linha por padrão
        td = tr[i].getElementsByTagName("td");
        for (var j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = ""; // Mostra a linha se houver correspondência
                    break;
                }
            }
        }
    }
}

// Function for mobile hamburger menu.
function toggle(element) {
    element.classList.toggle("change");
}

function exibirAlerta(mensagem) {
    if (mensagem) {
        window.alert(mensagem);
    }
}
function enviar1Formularios() {
    console.log("form1")
    // Obter os dados do primeiro formulário
    const form1 = new FormData(document.getElementById('form1'));
    const form2 = document.getElementById('form2');

    // Adicionar os dados do form1 ao form2
    for (let [key, value] of form1.entries()) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value;
        form2.appendChild(input);
    }

    // Submeter o segundo formulário com os dados combinados
    form2.submit();
}
function enviar2Formularios() {
    console.log("form2")
    // Obter os dados do primeiro formulário
    const form3 = new FormData(document.getElementById('form3'));
    const form4 = document.getElementById('form4');

    // Adicionar os dados do form1 ao form2
    for (let [key, value] of form3.entries()) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value;
        form4.appendChild(input);
    }

    // Submeter o segundo formulário com os dados combinados
    form4.submit();
}
function enviar3Formularios() {
    console.log("form3")
    // Obter os dados do primeiro formulário
    const form1 = new FormData(document.getElementById('form1'));
    const form5 = document.getElementById('form5');

    // Adicionar os dados do form1 ao form2
    for (let [key, value] of form1.entries()) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value;
        form5.appendChild(input);
    }
    console.log(form5, form1)
    // Submeter o segundo formulário com os dados combinados
    form5.submit();
}

function enviar4Formularios() {
    console.log("form2")
    // Obter os dados do primeiro formulário
    const form3 = new FormData(document.getElementById('form3'));
    const form6 = document.getElementById('form6');

    // Adicionar os dados do form1 ao form2
    for (let [key, value] of form3.entries()) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = value;
        form6.appendChild(input);
    }

    // Submeter o segundo formulário com os dados combinados
    form6.submit();
}




function mostrarCampos() {
    const tipo = document.getElementById('tipo').value;
    const camposPenalidade = document.getElementById('camposPenalidade');
    const camposAssistencia = document.getElementById('camposAssistencia');
    const camposAcrescimo = document.getElementById('camposAcrescimo');
    const camposSets = document.getElementById('camposSets');
    const camposEnd = document.getElementById('camposEnd');
    const camposWinner = document.getElementById('camposWinner');
    const camposBanner = document.getElementById('camposBanner')

    // Esconder todos os campos inicialmente
    camposPenalidade.classList.add('hidden');
    camposAssistencia.classList.add('hidden');
    camposAcrescimo.classList.add('hidden');
    camposSets.classList.add('hidden');
    camposEnd.classList.add('hidden');
    camposWinner.classList.add('hidden');
    camposBanner.classList.add('hidden');

    // Exibir os campos com base na escolha
    if (tipo === 'penalidade') {
        camposPenalidade.classList.remove('hidden');
    } else if (tipo === 'assistencia') {
        camposAssistencia.classList.remove('hidden');
    }else if (tipo === 'acrescimo') {
        camposAcrescimo.classList.remove('hidden');
    }else if (tipo === 'sets') {
        camposSets.classList.remove('hidden');
    }else if (tipo === 'end') {
        camposEnd.classList.remove('hidden');
    }else if (tipo === 'winner') {
        camposWinner.classList.remove('hidden');
    }else if (tipo === 'banner') {
        camposBanner.classList.remove('hidden');
    }
}