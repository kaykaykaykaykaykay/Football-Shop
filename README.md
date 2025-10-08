**Deployed link:**  
[https://khayru-rafa-football-shop.pbp.cs.ui.ac.id](https://khayru-rafa-football-shop.pbp.cs.ui.ac.id)

Assignment 6
What is the difference between synchronous request and asynchronous request?
A synchronous request means the browser waits for the server to finish responding before continuing. The whole page is refreshed or replaced with new content.
An asynchronous request (AJAX) happens in the background. The browser can keep running other scripts, and only part of the page is updated when the response arrives. This makes the interaction smoother and faster since it doesn’t reload the whole page.

How does AJAX work in Django (request–response flow)?
When a user performs an action on the page, JavaScript sends an AJAX request to a Django view. Django processes the request, performs the needed database or logic operation, and sends a JSON response back. The JavaScript code then updates specific parts of the HTML dynamically using that data, without reloading the entire page. This cycle of background request and targeted update is what makes AJAX powerful.

What are the advantages of using AJAX compared to regular rendering in Django?
AJAX makes websites feel faster and more responsive because only the necessary data is sent and received, not the entire webpage. It reduces server load, improves user experience, and allows dynamic features such as live updates, instant searches, and interactive forms. It also enables smoother transitions since users don’t lose their place or have to reload the page every time they interact with it.

How do you ensure security when using AJAX for Login and Register features in Django?
Security in AJAX must be handled carefully. Every AJAX request should include a valid CSRF token so Django can verify that the request comes from a trusted source. Input data must always be validated on the server side, not just in JavaScript. The communication should use HTTPS to protect credentials, and responses should never expose sensitive information. Even though AJAX is used, authentication and session management should still rely on Django’s secure built-in authentication system.

How does AJAX affect user experience (UX) on websites?
AJAX greatly enhances user experience by making web pages feel more interactive and immediate. Users can see results instantly, interact with content without losing progress, and experience smoother navigation. It makes the website feel more like a real application. However, if implemented carelessly, AJAX can confuse users by breaking the back button, making pages less accessible, or complicating search engine indexing. When done correctly, AJAX creates a faster, more engaging, and seamless experience.
