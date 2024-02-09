class Curve{

    constructor(index, reactionTime){
        this.index = index;
        this.reactionTime = reactionTime;
        this.penaltyTime = 0;

        this.component = document.createElement('tr');
        this.reactionTimeField = this.createReactionTimeField();
        this.addCell(this.reactionTimeField, "reactionTime");
        this.addCell(this.createIndexField(), "index");
        this.setIfIsPenalty()
    }

    addPenaltyWithTime(time){
        this.penaltyTime += time;
        this.reactionTimeField.innerHTML = (this.reactionTime).toFixed(1).toLocaleString("de-DE") + " ms" + " (<font style='color: rgba(255, 0, 0, 0.7)'> +" + Math.round((this.penaltyTime)).toLocaleString("de-DE") + " ms </font>)";
    }

    setIfIsPenalty(){
        this.component.classList.add('normal');
    }

    addCell(compoent, className){
        let cell = document.createElement('th');
        cell.classList.add(className);
        cell.appendChild(compoent);
        this.component.appendChild(cell);
    }

    createIndexField(){
        let indexField = document.createElement('span');
        indexField.textContent = this.index==0?"Ende":this.index;
        return indexField;
    }

    createReactionTimeField(){
        let reactionTimeField = document.createElement('span');
        reactionTimeField.textContent = (this.reactionTime).toFixed(1).toLocaleString("de-DE") + " ms";
        return reactionTimeField;
    }

}
