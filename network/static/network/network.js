// let post = document.querySelector("#editpost");
// // function prefillBody(post) {
// //   return post.content;
// // }

// function editPost(post) {
//   fetch(`/edit_post/${post.id}`, {
//     method: "POST",
//     body: JSON.stringify({
//       content: document.querySelector("#editpost").value,
//     }),
//   });

//   return false;
//   // loadMailbox("sent");
// }
document.addEventListener("DOMContentLoaded", function () {
  var myVar = document.getElementById("myVar").value;
  console.log(myVar);
})
