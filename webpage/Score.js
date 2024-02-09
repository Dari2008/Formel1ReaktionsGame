class Score{
    constructor(name, score, min, time){
        this.score = score;
        this.min = min;
        this.time = time;
        this.name = name;

        this.component = document.createElement('tr');

        this.addCell(this.createNameField(), "name");
        this.addCell(this.createScoreField(), "score");
        this.addCell(this.createMinField(), "min");
        this.addCell(this.createDateField(), "date");

    }

    getComponent(){
        return this.component;
    }

    createNameField(){
        let nameField = document.createElement('span');
        nameField.textContent = this.name;
        return nameField;
    }

    createScoreField(){
        let scoreField = document.createElement('span');
        scoreField.textContent = this.score;
        return scoreField;
    }

    createMinField(){
        let minField = document.createElement('span');
        minField.textContent = this.min;
        return minField;
    }

    createDateField(){
        let dateField = document.createElement('span');
        dateField.textContent = this.time;
        return dateField;
    }

    addCell(compoent, className){
        let cell = document.createElement('th');
        cell.classList.add(className);
        cell.appendChild(compoent);
        this.component.appendChild(cell);
    }

    getScore(){
        return this.score;
    }

    getMin(){
        return this.min;
    }
}