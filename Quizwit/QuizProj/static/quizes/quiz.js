console.log("Hello World from quiz.js");

const url = window.location.href;
const quizBox = document.getElementById('quiz-box');
let data

// Fetch data from the API
$.ajax({
    type: 'GET',
    url: `${url}data`, // Ensure URL is correctly formatted
    success: function(response) {
        console.log(response)
        data = response.data;
        data.array.forEach(element => {
            for (const [question, answers] of Object.entries(element)) {
                console.log(question)
                console.log(answers)
            }
        }); 
    },
    error: function(error) {
        console.error("Error occurred:", error);
    }
});

/* $.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response) { 
        console.log(response);
        data = response.data;
        data.array.forEach(element => {
            for (const [question, answers] of Object.entries(element)) {
                console.log(question);
                console.log(answers);
            }
        });
    },
    error: function(error) { 
        console.error("Error occurred:", error);
    }
});
*/


