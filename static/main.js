// validation of form
let fname=document.getElementById("Full-name"); 
let email=document.getElementById("mail");
let pnumber=document.getElementById("phone"); 
let form=document.getElementById("form");
 


form.addEventListener("submit",(e)=>{
    
    inc=true; 
       //full name 
    const errfn=document.getElementById("fn");
    const fnregex=/^[A-Za-z][a-z]+(\s[a-zA-Z][a-z]+)+$/;
    
    if(fname.value===""){
        inc=false; 
        errfn.innerHTML="this field is required";
   
    } else if(! fnregex.test(fname.value)){
        inc=false; 
       errfn.innerHTML="Invalid full name";
    } else{ errfn.innerHTML=""; }

          //email
     const errm=document.getElementById("em");  
      const mregex=/^[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}$/; 
    if(email.value===""){
        inc=false; 
        errm.innerHTML="this field is required";
   
    } else if(! mregex.test(email.value)){
        inc=false; 
       errm.innerHTML="Invalid email";
    } else{ errm.innerHTML=""; }

          //phone number
    const errnumber=document.getElementById("phn");
    const nregex=/^(?:\+213\s?|0)[5-7](?:[\s.-]?[0-9]{2}){4}$/;

    if(pnumber.value===""){
        inc=false; 
        errnumber.innerHTML="this field is required";
   
    } else if(! nregex.test(pnumber.value)){
        inc=false; 
       errnumber.innerHTML="Invalid phone number";
    } else{ errnumber.innerHTML=""; } 

    if(inc==false){
        e.preventDefault(); 
      }
     
     
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

     console.log(days); 
     console.log(hours); 
     console.log(minuts); 
     console.log(seconds); 
     console.log("###############################"); 

     document.querySelector("#days").innerHTML =days <10 ? `0${days}`: days;
     document.querySelector("#hours").innerHTML =hours <10 ? `0${hours}`: hours;
     document.querySelector("#minutes").innerHTML =minuts <10 ? `0${minuts}`: minuts;
     document.querySelector("#seconds").innerHTML =seconds <10 ? `0${seconds}`: seconds;

if(dateDF<0){ss
    clearInterval(cd); 
}

},);


