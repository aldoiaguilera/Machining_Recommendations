// Load inserts based on manufacturer
async function get_all_inserts(manufacturer_id) {
    var results = await fetch('http://18.118.161.190/get_inserts/' + manufacturer_id)
        .then( response => response.json() )
    position = document.getElementById("insrt");
    position.innerHTML = '';
    for (var i = 0; i < results.length; i++) {
        position.innerHTML += `
        <option value="${results[i].id}">${results[i].insrt}</option>
        `;
    }
    get_all_materials(results[0].id)
}

// Load default values into find form when page is loaded
get_all_inserts(document.getElementById("manufacturer").value)

// Load materials based on insert
async function get_all_materials(insrt_id){
    var results = await fetch('http://18.118.161.190/get_materials/' + insrt_id)
        .then( response => response.json() )
    position = document.getElementById("material");
    position.innerHTML = '';
    for (var i = 0; i < results.length; i++) {
        position.innerHTML += `
        <option value="${results[i].id}">${results[i].material}</option>
        `;
    }
}

// Load page result
function find() {
    material = document.getElementById("material").value;
    window.location.href = "http://18.118.161.190/find/" + material;
}
