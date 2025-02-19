let submit = document.getElementById("submitbutton");

submit.addEventListener("click", (e) => {
    let inc = true;

    // Full name validation
    const errfn = document.getElementById("fn");
    const fname = document.getElementById("Full-name");
    const fnregex = /^[A-Za-z][a-z]+(\s[a-zA-Z][a-z]+)+$/;

    if (fname.value === "") {
        inc = false;
        errfn.innerHTML = "This field is required";
    } else if (!fnregex.test(fname.value)) {
        inc = false;
        errfn.innerHTML = "Invalid full name";
    } else {
        errfn.innerHTML = "";
    }

    // Email validation
    const errm = document.getElementById("em");
    const email = document.getElementById("mail");
    const mregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}$/;

    if (email.value === "") {
        inc = false;
        errm.innerHTML = "This field is required";
    } else if (!mregex.test(email.value)) {
        inc = false;
        errm.innerHTML = "Invalid email";
    } else {
        errm.innerHTML = "";
    }

    // Phone number validation
    const errnumber = document.getElementById("phn");
    const pnumber = document.getElementById("phone");
    const nregex = /^(?:\+213\s?|0)[5-7](?:[\s.-]?[0-9]{2}){4}$/;

    if (pnumber.value === "") {
        inc = false;
        errnumber.innerHTML = "This field is required";
    } else if (!nregex.test(pnumber.value)) {
        inc = false;
        errnumber.innerHTML = "Invalid phone number";
    } else {
        errnumber.innerHTML = "";
    }

    // If validation fails, prevent form submission
    if (!inc) {
        e.preventDefault();
        return;
    }

    // Show loading spinner & disable button
    submit.innerHTML = `<div class="spinner-border spinner-border-sm" role="status"></div> Loading...`;
    submit.disabled = true;
    const originalContent = submit.innerHTML;
    // Prepare data
    const data = {
        name: fname.value,
        email: email.value,
        number: pnumber.value,
    };

    const resultElement = document.getElementById("result");

    fetch("/book-ticket", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Success:", result);
        resultElement.textContent = "Ticket booked! Please check your e-mail inbox.";
        resultElement.style.display = "block";

        setTimeout(() => {
            resultElement.style.display = "none";
        }, 3000);
    })
    .catch(error => {
        console.error("Error:", error);
        resultElement.textContent = "Failed to book a ticket! Please try again later.";
        resultElement.style.display = "block";

        setTimeout(() => {
            resultElement.style.display = "none";
        }, 3000);
    })
    .finally(() => {
        // Restore button after request is complete
        submit.innerHTML = originalContent; 
          
        submit.disabled = false;
    });
});



  //countdown
let cd= new Date("Feb 25, 2025 23:59:59").getTime();
console.log(cd); 

let cout= setInterval(()=>{
    let dateNew= new Date().getTime();

    let dateDF= cd-dateNew ;

    let days=Math.floor(dateDF /(86400000)) ; 

    let hours= Math.floor((dateDF % 86400000)/(1000*60*60));
    let minuts= Math.floor((dateDF %(1000*60*60))/60000);
    let seconds = Math.floor((dateDF % (1000*60))/1000);


     document.querySelector("#days").innerHTML =days <10 ? `0${days}`: days;
     document.querySelector("#hours").innerHTML =hours <10 ? `0${hours}`: hours;
     document.querySelector("#minutes").innerHTML =minuts <10 ? `0${minuts}`: minuts;
     document.querySelector("#seconds").innerHTML =seconds <10 ? `0${seconds}`: seconds;

if(dateDF<0){
    clearInterval(cd); 
}

},);


