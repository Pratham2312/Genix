document.addEventListener('DOMContentLoaded', () => {
    const roleButtons = document.querySelectorAll('.roles button');
    const roleInput = document.getElementById('role');

    roleButtons.forEach(button => {
        button.addEventListener('click', () => {
            roleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            roleInput.value = button.textContent.toLowerCase();
        });
    });
});
