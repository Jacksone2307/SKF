console.log("WOWEE");

function headerFunction(){
    document.getElementById("mainHeading").innerHTML = "Wooba";
}

function clock(){
    const d = new Date;
    document.getElementById("clock").innerHTML = `${d.toLocaleTimeString()}`;
}



setInterval(clock, 1000);