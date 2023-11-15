const slugField = document.getElementById("id_slug")
const name = document.getElementById("id_name")
name.addEventListener("input", (event) => {
    const {name, value } = event.target;
    slugField.setAttribute("value", slug(value));
});