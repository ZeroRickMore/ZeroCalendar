
function updateUrl() {
    const month = document.getElementById('month-select').value;
    const year = document.getElementById('year-select').value;
    const url = `/view_month/${year}-${month.padStart(2, '0')}`;
    window.history.pushState({}, '', url);
}

function goToMonth() {
    const month = document.getElementById('month-select').value;
    const year = document.getElementById('year-select').value;
    window.location.href = `/view_month/${year}-${month.padStart(2, '0')}`;
}


