// SUPPORT =====================================================================
function sleep(s) {
    return new Promise(resolve => setTimeout(resolve, s*1000));
}

function isEditActive(dayEntry) {
    return dayEntry.classList.contains('isEditActive');
}

function isDetailsActive(dayEntry) {
    return dayEntry.classList.contains('isDetailsActive');
}
// =============================================================================


function toggleDetails(entry) {
    entry = entry.closest('.day-entry')

    if (isEditActive(entry)) { // If in edit mode, just handle the edit form...
        const editForm = entry.querySelector('.edit-form');
        editForm.classList.toggle('show');
    } else { // If not, just handle the details...
        const details = entry.querySelector('.day-details');   
        details.classList.toggle('show');
        entry.classList.toggle('isDetailsActive'); // And tell that details are active
    }

    const arrow = entry.querySelector('.arrow');
    arrow.classList.toggle('rotate');
}

async function toggleEditForm(icon) {
    // Order of action changes
    const entry = icon.closest('.day-entry');
    const editForm = entry.querySelector('.edit-form');
    const details = entry.querySelector('.day-details');   

    if (!isEditActive(entry)) {  // It was not in edit mode
        if (isDetailsActive(entry)) { // If details were shown
            details.classList.remove('show'); // Then remove them
            await sleep(0.3); // And wait for the animation to end
        }
        editForm.classList.add('show'); // Then add the edit form
        entry.classList.add('isEditActive'); // Finally, put in edit mode

    } else { // It was in edit mode
        editForm.classList.remove('show');
        if (isDetailsActive(entry)) {
            await sleep(0.3);
            details.classList.add('show');
        }
        entry.classList.remove('isEditActive') // No more edit mode
    }
}

function goBack() {
    window.history.back();
}

function goForward() {
    window.history.forward();
}