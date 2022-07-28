document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#newPostBtn").disabled = true;
  
  document.querySelector("#newPost").addEventListener("keyup", () => {
    if (document.querySelector("#newPost").value.trim() !== "") {
      document.querySelector("#newPostBtn").disabled = false;
    } else {
      document.querySelector("#newPostBtn").disabled = true;
    }
  });
});

function prefill(id) {
  const textarea = document.getElementById(`editpost-${id}`);
  const content = document.getElementById(`post-${id}`);
  textarea.innerHTML = content.textContent;
  document.querySelector(`#contentdiv-${id}`).hidden = true;
  document.querySelector(`#editpostbutton-${id}`).hidden = true;
  document.querySelector(`#editpostform-${id}`).hidden = false;

  document.querySelector(`#editpost-${id}`).addEventListener("keyup", () => {
    if (document.querySelector(`#editpost-${id}`).value.trim() !== "") {
      document.querySelector(`#editbtn-${id}`).disabled = false;
    } else {
      document.querySelector(`#editbtn-${id}`).disabled = true;
    }
  });
}

function hide(id) {
  document.querySelector(`#editpostform-${id}`).hidden = true;
  document.querySelector(`#contentdiv-${id}`).hidden = false;
  document.querySelector(`#editpostbutton-${id}`).hidden = false;
}

function edit(id) {

  fetch(`/edit_post/${id}`, {
    method: "POST",
    body: JSON.stringify({
      content: document.querySelector(`#editpost-${id}`).value.trim(),
    }),
  });

  const cntnt = document.getElementById(`post-${id}`);
  const val = document.querySelector(`#editpost-${id}`).value.trim();
  cntnt.innerHTML = val;
}