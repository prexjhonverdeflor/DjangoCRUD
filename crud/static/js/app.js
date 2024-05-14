
var message_timeout = document.getElementById("message-timer");
setTimeout(function()
{
    message_timeout.style.display = "none";
}
,5000);



//on scroll effect

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
            // Unobserve to prevent re-triggering
            observer.unobserve(entry.target);
        }
    });
});

const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));
