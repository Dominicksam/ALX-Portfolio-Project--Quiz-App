console.log ("Hello World from main.js");

const modalBtns = [...document.getElementsByClassName('modal-button')];
const modalBody = document.getElementById('modal-body-confirm');
const startBtn = document.getElementById('start-button')
const url = window.location.href

modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const pk = modalBtn.getAttribute('data-pk');
    const name = modalBtn.getAttribute('data-quiz');
    const numQuestions = modalBtn.getAttribute('data-questions');
    const difficulty = modalBtn.getAttribute('data-difficulty');
    const scoreToPass = modalBtn.getAttribute('data-score');
    const time = modalBtn.getAttribute('data-time');

    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to start "<b>${name}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>Difficulty: <b>${difficulty}</b></li>
                <li>Number of questions: <b>${numQuestions}</b></li>
                <li>Score to pass: <b>${scoreToPass}%</b></li>
                <li>Time: <b>${time} min</b></li>
            </ul>
        `;

    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk
    })
}));