//Editar lista abilitando o input
document.querySelectorAll(".btn-editar").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const listaId = btn.getAttribute("data-lista-id");
      const input = document.getElementById("editarLista" + listaId);
  
      if (input) {
        // Verifica se o placeholder original já foi salvo
        if (!input.originalPlaceholder) {
          input.originalPlaceholder = input.placeholder;
        }
  
        if (input.hasAttribute("disabled")) {
          input.removeAttribute("disabled");
          input.placeholder = "Novo nome para a lista";
          input.focus();
        } else {
          input.setAttribute("disabled", "disabled");
          input.placeholder = input.originalPlaceholder;
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
  
  
  