//função de expandir descrição do livro
function expandirDescricao(elemento) {
  var descricaoLivro = elemento.parentElement;
  descricaoLivro.style.maxHeight = "none";
  elemento.style.display = "none";
  descricaoLivro.querySelector(".ocultar").style.display = "block";
  atualizarBotoes();
}
//função de ocultar descrição do livro
function ocultarDescricao(elemento) {
  var descricaoLivro = elemento.parentElement;
  descricaoLivro.style.maxHeight = "150px";
  descricaoLivro.querySelector(".ler-mais").style.display = "block";
  elemento.style.display = "none";
  atualizarBotoes();
}

//função da caixa de adicionar resenha
$(document).ready(function () {
  var $formularioResenha = $("#formularioResenha");
  var $resenhasContainer = $("#resenhasContainer");

  $formularioResenha.hide();
  $resenhasContainer.children(".resenha").hide();

  $("#toggleFormularioResenha").on("click", function () {
    console.log("Botão clicado");
    $formularioResenha.toggle();
  });
});

//Selecionar estrelas para avaliação do livro
const stars = document.querySelectorAll(".star");
const inputAvaliacao = document.getElementById("avaliacao_resenha");

stars.forEach((star) => {
  star.addEventListener("click", () => {
    const rating = star.getAttribute("data-rating");
    const currentRating = parseInt(inputAvaliacao.value, 10);

    if (rating === currentRating.toString()) {
      inputAvaliacao.value = "0";
    } else {
      inputAvaliacao.value = rating;
    }

    stars.forEach((s) => {
      const sRating = parseInt(s.getAttribute("data-rating"), 10);
      if (sRating <= parseInt(inputAvaliacao.value, 10)) {
        s.classList.add("filled");
      } else {
        s.classList.remove("filled");
      }
    });
  });
});
