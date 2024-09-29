function trocarTextoLabel() {
    const label = document.getElementById('label-foto');
    const input = document.getElementById('fotos');
    
    // Se um arquivo for selecionado, muda o texto do label
    if (input.files.length > 0) {
        label.innerHTML = "Imagem carregada";
    }
    else {
        // Se nenhum arquivo estiver selecionado, volta para o texto padrão
        label.innerHTML = "Adicione uma imagem";
    }
};

document.getElementById('function_validate_form').addEventListener('submit', function(event) {
    // Usando window.confirm para validação
    if (!window.confirm("Você tem certeza que deseja ENVIAR os dados?")) {
        // Se o usuário clicar em "Cancelar", prevenimos o envio do formulário
        event.preventDefault();
    }
});

document.getElementById('function_validate_form_delete').addEventListener('submit', function(event) {
    // Usando window.confirm para validação
    if (!window.confirm("Você tem certeza que deseja EXCLUIR os dados?")) {
        // Se o usuário clicar em "Cancelar", prevenimos o envio do formulário
        event.preventDefault();
    }
});

function toggle(source) {
    checkboxes = document.getElementsByName('input-checkbox');
    for(i = 0, n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
};