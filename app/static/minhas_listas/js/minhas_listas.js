//Editar lista abilitando o input
document.querySelectorAll(".btn-editar").forEach(function (btn) {
  btn.addEventListener("click", function () {
    const listaId = btn.getAttribute("data-lista-id");
    const input = document.getElementById("editarLista" + listaId);
    const form = input.closest("form");

    if (input) {
      // Verifica se o placeholder original já foi salvo
      if (!input.originalPlaceholder) {
        input.originalPlaceholder = input.placeholder;
      }

      if (input.hasAttribute("disabled") && input.value.trim() === '') {
        input.removeAttribute("disabled");
        input.placeholder = "Novo nome para a lista";
        input.focus();
      } else {
        input.setAttribute("disabled", "disabled");
        input.placeholder = input.originalPlaceholder;

        const isFormValid = validarForm(form);
        if (!isFormValid) {
            // A validação falhou, evite que o formulário seja enviado
            Event.preventDefault();
        }
      }
    }
  });
});

function validarForm(form) {
const nomeListaInput = form.querySelector('.nome-lista');
const trimmedValue = nomeListaInput.value.trim();
const messageValidation = form.querySelector('.message-validation');

if (trimmedValue === '') {
    messageValidation.textContent = 'O nome da lista não pode estar em branco';
    return false; 
}

return true; 
}

//Exibir modal e excluir livro da lista
const openModalLivroButtons = document.querySelectorAll(".btn-excluir-livro");
const closeModalLivroButton = document.querySelector("#close-modal-livro");
const cancelarModalLivroButton = document.querySelector("#cancelar-modal-livro");
const confirmarModalLivroButton = document.querySelector("#confirmar-modal-livro");
const excluirLivroForm = document.querySelector("#excluir-livro-form");
const livroIsbnInput = document.querySelector("#livro-isbn-input");
const listaIdInput = document.querySelector("#lista-id-input");
const modalLivro = document.querySelector("#modal-livro");
const fadeLivro = document.querySelector("#fade-livro");

const toggleModalLivro = () => {
  modalLivro.classList.toggle("hide");
  fadeLivro.classList.toggle("hide");
};

openModalLivroButtons.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const livroIsbn = e.currentTarget.getAttribute("data-livro-isbn-livro");
    const listaId = e.currentTarget.getAttribute("data-lista-id-livro");

    // Atualiza os valores dos campos ocultos no formulário
    livroIsbnInput.value = livroIsbn;
    listaIdInput.value = listaId;
    excluirLivroForm.action = `/livro/excluir_livro_lista/${livroIsbn}/${listaId}`;

    toggleModalLivro()
  });
});

[closeModalLivroButton, fadeLivro, cancelarModalLivroButton].forEach((el) => {
  el.addEventListener("click", () => toggleModalLivro());
});

confirmarModalLivroButton.addEventListener("click", () => {
  excluirLivroForm.submit();
});


//Exibir modal e excluir lista
const openModalButtons = document.querySelectorAll(".btn-excluir");
const closeModalButton = document.querySelector("#close-modal");
const cancelarModalButton = document.querySelector("#cancelar-modal");
const modal = document.querySelector("#modal");
const fade = document.querySelector("#fade");
let listaIdToDelete; // Variável para armazenar o ID da lista a ser excluída

const toggleModal = () => {
  modal.classList.toggle("hide");
  fade.classList.toggle("hide");
};

openModalButtons.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    listaIdToDelete = e.currentTarget.getAttribute("data-lista-id");
    toggleModal();
  });
});

[closeModalButton, fade, cancelarModalButton].forEach((el) => {
  el.addEventListener("click", () => toggleModal());
});

const confirmarModalButton = document.querySelector("#confirmar-modal");
confirmarModalButton.addEventListener("click", () => {
  const form = document.querySelector("#modal form");
  form.action = `/livro/excluir_lista/${listaIdToDelete}/`;
});


