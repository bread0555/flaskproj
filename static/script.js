if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then(() => console.log('Service Worker Registered'));
}

const inactivityTime = 300000; // 5 * 60 * 1000
const redirectUrl = "/";
let inactivityTimer;
function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
        window.location.href = redirectUrl;
    }, inactivityTime);
}
document.addEventListener("mousemove", resetInactivityTimer);
document.addEventListener("keydown", resetInactivityTimer);
document.addEventListener("scroll", resetInactivityTimer);
document.addEventListener("click", resetInactivityTimer);
resetInactivityTimer();

function validateField(f){
  if(f.value.length == 0){
      alert("Please enter data in the "+f.name+" field");
  }
}