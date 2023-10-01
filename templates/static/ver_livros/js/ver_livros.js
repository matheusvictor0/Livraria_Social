function expandirDescricao(elemento) {
    var descricaoLivro = elemento.parentElement;
    descricaoLivro.style.maxHeight = 'none'; // Remove o limite de altura
    elemento.style.display = 'none'; // Oculta o botão "Ler mais"
    descricaoLivro.querySelector('.ocultar').style.display = 'block'; // Exibe o botão "Ocultar"
}

function ocultarDescricao(elemento) {
    var descricaoLivro = elemento.parentElement;
    descricaoLivro.style.maxHeight = '150px'; // Recoloca o limite de altura
    descricaoLivro.querySelector('.ler-mais').style.display = 'block'; // Exibe o botão "Ler mais"
    elemento.style.display = 'none'; // Oculta o botão "Ocultar"
}

//função da caixa de adicionar resenha
$(document).ready(function () {
    var $formularioResenha = $('#formularioResenha');
    var $resenhasContainer = $('#resenhasContainer');

    // Inicialmente, oculte o formulário de resenha e as resenhas adicionais
    $formularioResenha.hide();
    $resenhasContainer.children('.resenha').hide();

    $('#toggleFormularioResenha').on('click', function () {
        console.log('Botão clicado');
        $formularioResenha.toggle();
    });

});