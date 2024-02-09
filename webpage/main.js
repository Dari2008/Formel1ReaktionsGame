var update = ()=>{};
var elements = [];


document.addEventListener('DOMContentLoaded', function(){

    var data = {};
    var timeTaken = 0.0;
    var reactionTimeAvg = 0;
    var totalPenaltyTime = 0.0;
    var penaltyCount = 0;
    var penaltyTimePerPenalty = 0;

    init();
    update();

    function init(){
        document.querySelector("#timeTaken .left").textContent = "Gesamtzeit";
        document.querySelector("#timeTaken .center").textContent = "?";

        document.querySelector("#avgReactionTime .left").textContent = "Reaktionszeit";
        document.querySelector("#avgReactionTime .center").textContent = "?";     

        document.querySelector("#penaltyTime .center").textContent = "?";
        document.querySelector("#penaltyTime .right").textContent = " Strafzeit";

        document.querySelector("#penaltyCount .center").textContent = "?";
        document.querySelector("#penaltyCount .right").textContent = " Strafzeiten";

        document.querySelector("#timeTaken .left").classList.add("name");
        document.querySelector("#avgReactionTime .left").classList.add("name");
        document.querySelector("#penaltyTime .right").classList.add("name");
        document.querySelector("#penaltyCount .right").classList.add("name");
    }

    update = function(){

        $.ajax({
            url: "./raceData.json",
            type: "GET",
            dataType: "json",
            success: function(tmpData){
                data = tmpData;
                if(data["times"] != undefined){
                    elements = data["times"].map((e)=>{
                        return new Curve(e.curve, e.time);
                    });
                    elements.push(new Curve(0, 0));
                }

                timeTaken = -1;
                reactionTimeAvg = -1;
                totalPenaltyTime = -1;
                penaltyCount = -1;
                penaltyTimePerPenalty = -1;
    
                if(data["timeTaken"] != undefined)timeTaken = data["timeTaken"];
                if(data["reactionTimeAvg"] != undefined)reactionTimeAvg = data["reactionTimeAvg"];
                if(data["penaltyTime"] != undefined)totalPenaltyTime = data["penaltyTime"];
                if(data["penaltyCount"] != undefined)penaltyCount = data["penaltyCount"];
                if(data["penaltyTimePerPenalty"] != undefined)penaltyTimePerPenalty = data["penaltyTimePerPenalty"];
                
                if(data["penaltys"] != undefined){
                    data["penaltys"].forEach((el)=>{
                        elements.forEach((e)=>{
                            console.log((e.index==0?elements.length:e.index) + ":" + el.curve)
                            if((e.index==0?elements.length:e.index) == el.curve){
                                e.addPenaltyWithTime(penaltyTimePerPenalty)
                            }
                        });
                    });
                }

                var table = document.getElementById("timeTableBody");
                table.innerHTML = "";
                elements.forEach((e)=>{
                    table.appendChild(e.component);
                });

                document.querySelector("#timeTaken .left").textContent = "Gesamtzeit";
                document.querySelector("#timeTaken .center").textContent = (timeTaken).toFixed(1).toLocaleString("de-DE") + " ms";

                document.querySelector("#avgReactionTime .left").textContent = "Reaktionszeit";
                document.querySelector("#avgReactionTime .center").textContent = reactionTimeAvg.toFixed(1).toLocaleString("de-DE") + " ms";

                document.querySelector("#penaltyTime .center").textContent = totalPenaltyTime.toLocaleString("de-DE") + " ms";
                document.querySelector("#penaltyTime .right").textContent = " Strafzeit";

                document.querySelector("#penaltyCount .center").textContent = penaltyCount.toLocaleString("de-DE");
                document.querySelector("#penaltyCount .right").textContent = " Strafzeiten";

                document.querySelector("#timeTaken .left").classList.add("name");
                document.querySelector("#avgReactionTime .left").classList.add("name");
                document.querySelector("#penaltyTime .right").classList.add("name");
                document.querySelector("#penaltyCount .right").classList.add("name");
            }
        });

    }

});

function generateNewName(){
    $.ajax({
        url: "./names.json",
        type: "GET",
        dataType: "json",
        success: function(data){
            var name = data[Math.floor(Math.random()*data.length)];
            document.getElementById("name").placeholder = name;
        }
    });
}

function startNewGame(){
    var name = document.getElementById("name").value;
    if(name == ""){
        name = document.getElementById("name").placeholder;
    }
    var url = "./startGame"
    $.ajax({
        url: url,
        type: "POST",
        data: name,
        dataType: "json",
        success: function(data){
        }
    });
}

function updateScoreData(place, score, minimal){
    document.getElementById("place").textContent = place + ". Place";
    document.getElementById("score").textContent = "Score: " + score + " Millisekunden";
    document.getElementById("minimal").textContent = "Minimale Reationszeit: " + minimal + " Millisekunden";

    if(place == 1){
        document.getElementById("placeBanner").classList.add("first");
    }else if(place == 2){
        document.getElementById("placeBanner").classList.add("second");
    }else if(place == 3){
        document.getElementById("placeBanner").classList.add("third");
    }

    document.getElementById("placeBanner").classList.add("show");
    setTimeout(function(){
        document.getElementById("placeBanner").classList.remove("show");
    }, 5000);
}

if(location.origin.includes("5000")){
    setInterval(function(){
        $.ajax({
            url: "./isNewData.json",
            type: "GET",
            dataType: "json",
            success: function(data){
                if(data["update"] == true){
                    update();
                    document.getElementById("newGameDialog").close();
                    if(data["place"] != undefined && data["score"] != undefined && data["minimal"] != undefined){
                        updateScoreData(data["place"], data["score"], data["minimal"]);
                    }
                }
            }
        });
    }, 2000);
}