document.addEventListener("DOMContentLoaded", () => {
  /* This is a function that disables the new post button until the user types something in the text
  area. */
  if (document.querySelector("#newPostBtn")) {
    
    document.querySelector("#newPostBtn").disabled = true;
    
    document.querySelector("#newPost").addEventListener("keyup", () => {
      /* This is checking if the value of the textarea is not empty. */
      if (document.querySelector("#newPost").value.trim() !== "") {
        document.querySelector("#newPostBtn").disabled = false;
      } else {
        document.querySelector("#newPostBtn").disabled = true;
      }
    });
  }
});

function prefill(id) {
  /* This is a function that is called when the user clicks the edit button. It is prefilling the
  textarea with the content of the post. It is also hiding the content div and the edit button and
  showing the edit form. It is also adding an event listener to the textarea that enables the edit
  button when the user types something in the textarea. */
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
  /* This is hiding the edit form and showing the content div and the edit button. */
  document.querySelector(`#editpostform-${id}`).hidden = true;
  document.querySelector(`#contentdiv-${id}`).hidden = false;
  document.querySelector(`#editpostbutton-${id}`).hidden = false;
}

function edit(id) {
  /* This is sending a POST request to the server with the new content of the post. It is also
  updating the content of the post on the page. */
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

function toggleLikes(id) {
  /* This is a function that is called when the user clicks the like button. It is checking if the user
  has already liked the post. If the user has already liked the post, it is unliking the post and
  updating the number of likes. If the user has not already liked the post, it is liking the post and
  updating the number of likes. */
  if (document.querySelector(`#unlike-${id}`)) {
    document.querySelector(`#togglelikediv-${id}`).innerHTML = `<button id='like-${id}' name='like' class='btn btn-outline-light btn-sm' type='submit'><i class='heart fa fa-heart-o' style='font-size: 20px; color: red;'></i></button>`;
    fetch(`/likes/${id}`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((num) => {
        document.querySelector(`#likenum-${id}`).innerHTML = num;
      });

  } else {
    document.querySelector(`#togglelikediv-${id}`).innerHTML = `<button id='unlike-${id}' name='unlike' class='btn btn-outline-light btn-sm' type='submit'><i class='heart fa fa-heart' style='font-size: 20px; color: red;'></i></button>`;
    fetch(`/likes/${id}`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((num) => {
        document.querySelector(`#likenum-${id}`).innerHTML = num;
      });
  }
}