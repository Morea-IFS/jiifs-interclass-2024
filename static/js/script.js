function trocarTextoLabel() {
    const label = document.getElementById('label-foto');
    const input = document.getElementById('foto-jogador');
    
    // Se um arquivo for selecionado, muda o texto do label
    if (input.files.length > 0) {
        label.innerHTML = "Imagem carregada";
    }
    else {
        // Se nenhum arquivo estiver selecionado, volta para o texto padrão
        label.innerHTML = "Adicione uma imagem";
    }
}