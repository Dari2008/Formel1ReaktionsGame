var scores = [];

document.addEventListener("DOMContentLoaded", ()=>{
    var scoresTable = document.getElementById("scoresBody");
    scoresTable.innerHTML = "";

    $.ajax({
        url: "./scores.json",
        type: "GET",
        responseType: "json",
        success: function(response){
            scores = [];
            response.forEach((score) => {
                scores.push(new Score(score.name, score.score, score.smallest, score.time));
            });
            scores.sort((a, b) => {
                return a.getScore() - b.getScore();
            });

            scoresTable.innerHTML = "";
            scores.forEach((score) => {
                scoresTable.appendChild(score.getComponent());
            });

            scores[0].getComponent().classList.add("best");
            if(scores.length > 1){
                scores[1].getComponent().classList.add("second");
            }
            if(scores.length > 2){
                scores[2].getComponent().classList.add("third");
            }
        }
    });

});