document.addEventListener("input", function (e) {
  if (e.target.tagName.toLowerCase() === "textarea") {
      e.target.style.height = "auto"; // Redefine a altura para automática
      e.target.style.height = (e.target.scrollHeight) + "px"; // Define a altura com base no conteúdo
  }
});

//visibilidade do container de comentarios
const btnComentarios = document.querySelectorAll(".btn-comentarios");
const containerComentarios = document.querySelectorAll(".container-comentarios");
const iconComment = document.querySelectorAll("#icon-comment");

btnComentarios.forEach(function (btn, index) {
  btn.addEventListener("click", function () {
      if (containerComentarios[index].style.display === "none" || containerComentarios[index].style.display === "") {
          containerComentarios[index].style.display = "block";
          iconComment[index].className = 'bx bxs-comment';
      } else {
          containerComentarios[index].style.display = "none";
          iconComment[index].className = 'bx bx-comment';
      }
  });
});

let formEditComentario = null; // Armazena o formulário em edição
// Função para mostrar ou ocultar o campo de edição de comentário
function toggleComentarioEdicao(comentarioId) {
  const formEdit = document.querySelector(`#form-edit-${comentarioId}`);
  const textareaEditComentario = document.querySelector(`#texto_edit_comentario_${comentarioId}`);

  if (formEditComentario === formEdit) {
      // Se o mesmo formulário estiver em edição, oculte-o
      formEdit.style.display = "none";
      formEditComentario = null;
  } else {
      if (formEditComentario) {
          // Se houver um formulário em edição diferente, oculte-o primeiro
          formEditComentario.style.display = "none";
      }

      // Exiba o formulário atual
      formEdit.style.display = "block";
      textareaEditComentario.focus();
      formEditComentario = formEdit;
  }
}

// Adicione um evento de clique aos botões "Editar"
const btnEditarComentarios = document.querySelectorAll(".btn-editar-comentario");
btnEditarComentarios.forEach((btn) => {
    btn.addEventListener("click", () => {
        const comentarioId = btn.getAttribute("data-comentario-id");
        toggleComentarioEdicao(comentarioId);
    });
});


//Visibilidade container adicionar resenha
const buttonAddResenha = document.getElementById("toggleFormularioResenha");
const formularioResenha = document.getElementById("formularioResenha");

buttonAddResenha.addEventListener("click", function() {
    if (formularioResenha.style.display === "none") {
      formularioResenha.style.display = "block";
    } else {
      formularioResenha.style.display = "none";
    }
});

//Visibilidade container editar resenha
const btnEditar = document.querySelectorAll(".btn-editar");

btnEditar.forEach(function (botaoEditar) {
    botaoEditar.addEventListener("click", function () {
      const resenhaId = botaoEditar.getAttribute("data-resenha-id");
      const containerEditarResenha = document.getElementById(`editarResenha_${resenhaId}`);
      const tituloResenha = containerEditarResenha.querySelector("#titulo_resenha");

        if (containerEditarResenha) {
            // Alternar a exibição do contêiner editarResenha
            if (containerEditarResenha.style.display === "none" || !containerEditarResenha.style.display) {
                containerEditarResenha.style.display = "block";
                tituloResenha.focus();
            } else {
                containerEditarResenha.style.display = "none";
            }
        }
    });
});

var starContainers = document.querySelectorAll('.star-resenha');

starContainers.forEach(function (container) {
    var ratingValue = container.getAttribute('data-rating');
    var stars = container.querySelectorAll('i');

    stars.forEach(function (star, index) {
        if (index < ratingValue) {
            star.style.color = '#EDAC06';
        } else {
            star.style.color = 'gray'; 
        }
    });
});

//ADICIONAR RESENHA - Selecionar estrelas para avaliação do livro
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

const openModalResenha = document.querySelectorAll(".btn-excluir-resenha");
const closeModalResenha = document.querySelector("#close-modal-resenha");
const cancelarModalResenha = document.querySelector("#cancelar-modal-resenha");
const modalResenha = document.querySelector("#modal-resenha");
const fadeResenha = document.querySelector("#fade-resenha");
let resenhaIDToDelete;

const toggleModalResenha = () => {
    modalResenha.classList.toggle("hide");
    fadeResenha.classList.toggle("hide");
};

openModalResenha.forEach((btn) => {
    btn.addEventListener("click", (e) => {
        resenhaIDToDelete = e.currentTarget.getAttribute("data-lista-id");
        toggleModalResenha();
    });
});

[closeModalResenha, fadeResenha, cancelarModalResenha].forEach((el) => {
    el.addEventListener("click", () => toggleModalResenha());
});

const confirmarModalResenha = document.querySelector("#confirmar-modal-resenha");
confirmarModalResenha.addEventListener("click", () => {
    const form = document.querySelector("#modal-resenha form");
    form.action = `/livro/excluir_resenha/${resenhaIDToDelete}/`;
});

const openModalComentario = document.querySelectorAll(".btn-excluir-comentario");
const closeModalComentario = document.querySelector("#close-modal-comentario");
const cancelarModalComentario = document.querySelector("#cancelar-modal-comentario");
const modalComentario = document.querySelector("#modal-comentario");
const fadeComentario = document.querySelector("#fade-comentario");
let comentarioIDToDelete;

const toggleModalComentario = () => {
  modalComentario.classList.toggle("hide");
  fadeComentario.classList.toggle("hide");
};

openModalComentario.forEach((btn) => {
  btn.addEventListener("click", (e) => {
      comentarioIDToDelete = e.currentTarget.getAttribute("data-lista-id");
      toggleModalComentario();
  });
});

[closeModalComentario, fadeComentario, cancelarModalComentario].forEach((el) => {
  el.addEventListener("click", () => toggleModalComentario());
});

const confirmarModalComentario = document.querySelector("#confirmar-modal-comentario");
confirmarModalComentario.addEventListener("click", () => {
    const form = document.querySelector("#modal-comentario form");
    form.action = `/livro/excluir_comentario/${comentarioIDToDelete}/`;
});


//EDITAR LIVRO- Selecionar estrelas para avaliação do livro
const resenhas = document.querySelectorAll(".rounded-rectangle-resenhas");
resenhas.forEach((resenha) => {
  const stars = resenha.querySelectorAll(".star");
  const inputAvaliacao = resenha.querySelector("#edit_avaliacao_resenha");

  stars.forEach((star) => {
    star.addEventListener("click", () => {
      console.log("Clique na estrela");
      const rating = star.getAttribute("data-rating");
      const currentRating = parseInt(inputAvaliacao.value, 10);

      console.log("Rating: ", rating);
      console.log("Current Rating: ", currentRating);

      if (rating === currentRating.toString()) {
        inputAvaliacao.value = "0";
      } else {
        inputAvaliacao.value = rating;
        console.log("Rating: ", rating);
        console.log("Current Rating: ", currentRating);
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
});

const urlParams = new URLSearchParams(window.location.search);
const resenhaCurtida = urlParams.get("like");
const resenhaComentada = urlParams.get("comment");
const resenhaID = urlParams.get("resenha");

if (resenhaCurtida || resenhaComentada) {
    if (resenhaCurtida) {
        const resenhaCurtidaElement = document.getElementById("resenha-" + resenhaCurtida);
        if (resenhaCurtidaElement) {
            // Role até a resenha curtida
            resenhaCurtidaElement.scrollIntoView({ behavior: "smooth" });
        }
    }

    if (resenhaComentada) {
        const resenhaComentadaElement = document.getElementById("comentario-" + resenhaComentada);
        if (resenhaComentadaElement) {
            // Tornar o contêiner de comentários visível
            const containerComentarios = document.getElementById("container-comentario-" + resenhaID);
            containerComentarios.style.display = "block";

            // Role até o comentário
            resenhaComentadaElement.scrollIntoView({ behavior: "smooth" });
        }
    }
}

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

document.querySelector(".btn-save-list").addEventListener("click", function () {
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


