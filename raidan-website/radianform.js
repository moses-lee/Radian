let b64;

document.getElementById("lungPic").onchange = function() {
    let file = this.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function() {
        b64 = reader.result;
    }
}

document.getElementById("uploadData").onclick = function() {
    console.log("Submitting request...")
    b64 = b64.split(',')
    console.log(b64[1].length)
    let Http = new XMLHttpRequest();
    console.log(b64[1])
    let url = 'http://127.0.0.1:5000/diagnose?image='+b64[1];
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        rsp = Http.responseText;
        rsp = JSON.parse(rsp);
        let res = rsp.has_covid == "True" ? "high" : "low";
        console.log(rsp.has_covid);
        alert(document.getElementById("patient_name").value+" has a " + res + " likelihood of developing COVID-19.");
    }
};