//Validação do input de criar lista
document.getElementById("criar-lista-form").addEventListener("submit", function (event) {
  const novaListaInput = document.querySelector('input[name="nova_lista"]');
  const messageValidation = document.querySelector(".message-validation");

  if (novaListaInput.value.trim() === "") {
    messageValidation.textContent = "O campo não pode estar vazio";
    event.preventDefault();

    document.getElementById("minhas-listas").classList.add("show");
  } else {
    messageValidation.textContent = "";
  }
});

//Manter dropdown de listas aberto
const inputCriarLista = document.querySelector(".input-add-list");
document.addEventListener("DOMContentLoaded", function () {
const urlParams = new URLSearchParams(window.location.search);
const dropdownParam = urlParams.get("dropdown");

if (dropdownParam === "open") {
  document.getElementById("minhas-listas").classList.add("show");
  inputCriarLista.focus();
}

document
  .querySelector(".btn-save-list")
  .addEventListener("click", function () {
    document.getElementById("minhas-listas").classList.remove("show");
  });
});

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

//função exibir container de adicionar resenha
document.addEventListener("DOMContentLoaded", function () {
var formularioResenha = document.getElementById("formularioResenha");
var resenhasContainer = document.getElementById("resenhasContainer");
var toggleFormularioResenha = document.getElementById("toggleFormularioResenha");
var resenhas = resenhasContainer.querySelectorAll(".resenha");

formularioResenha.style.display = "none";
for (var i = 0; i < resenhas.length; i++) {
  resenhas[i].style.display = "none";
}

toggleFormularioResenha.addEventListener("click", function () {
  console.log("Botão clicado");
  if (formularioResenha.style.display === "none" || formularioResenha.style.display === "") {
    formularioResenha.style.display = "block";
  } else {
    formularioResenha.style.display = "none";
  }
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

//Recuperar checkboxes de listas selecionadas para salvar livro
var listaSelecionada = {};
document.getElementById("btnSalvar").addEventListener("click", function (e) {
var checkboxes = document.querySelectorAll(".form-check-input");
var selectedLists = [];

checkboxes.forEach(function (checkbox) {
  if (checkbox.checked) {
    var lista_id = checkbox.value;
    var lista_nome = document
      .querySelector("label[for=check" + lista_id + "]")
      .innerText.trim();
    selectedLists.push({ id: lista_id, nome: lista_nome });
  }
});

if (selectedLists.length > 0) {
  var listaIds = selectedLists
    .map(function (item) {
      return item.id;
    })
    .join(",");

  var listaNomes = selectedLists
    .map(function (item) {
      return item.nome;
    })
    .join(",");

  document.getElementById("lista_id").value = listaIds;
  document.getElementById("lista_nome").value = listaNomes;

  document.getElementById("formulario").submit();
}
});

