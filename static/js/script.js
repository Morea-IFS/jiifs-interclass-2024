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

document
    .getElementById("function_validate_form")
    .addEventListener("submit", function (event) {
        // Usando window.confirm para validação
        if (!window.confirm("Você tem certeza que deseja ENVIAR os dados?")) {
            // Se o usuário clicar em "Cancelar", prevenimos o envio do formulário
            event.preventDefault();
        }
    });

document
    .getElementById("function_validate_form_delete")
    .addEventListener("submit", function (event) {
        // Usando window.confirm para validação
        if (!window.confirm("Você tem certeza que deseja EXCLUIR os dados?")) {
            // Se o usuário clicar em "Cancelar", prevenimos o envio do formulário
            event.preventDefault();
        }
    });

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

//alert for match add
function exibirAlerta(mensagem) {
    if (mensagem) {
        window.alert(mensagem);
    }
}
function enviar1Formularios() {
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