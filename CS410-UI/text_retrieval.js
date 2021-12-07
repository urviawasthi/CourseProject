function set_variable(element) {
    localStorage.setItem('lecture_number', element.innerHTML);
    alert(localStorage.getItem('lecture_number'));
}