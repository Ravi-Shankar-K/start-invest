function progress(){
    let circle = document.querySelector('.circle');
    let circleValue = document.querySelector('.value');
    let amountRequired = document.getElementById('target-amt');
    let den = parseInt(amountRequired.textContent);
    let amountCollected = document.getElementById('amt-collected');
    let num = parseInt(amountCollected.textContent);
    let startvalue = 0;
    let endValue = Math.floor((num/den)*100);
    let progress = setInterval(()=>{
        startvalue += 1;
        circle.style.background = `conic-gradient(rgb(0, 0, 255) ${startvalue*3.6}deg,rgb(215, 241, 244)  0deg)`;
        circleValue.textContent = `${startvalue}%`
        if(startvalue == endValue){
            clearInterval(progress);
        }
    },1)
}