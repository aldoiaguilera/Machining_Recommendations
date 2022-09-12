// Display recommendation form, remove show form button
function show_form(buttn) {
    buttn.style.display = 'none';
    elem = document.getElementById('recommendation-form');
    elem.style.display = 'flex';
}

// Remove recommendation form, display show form button
function cancel_recommendation() {
    bttn = document.getElementById('add-recommendation');
    elem = document.getElementById('recommendation-form');
    elem.style.display = 'none';
    bttn.style.display = 'block';
}