// Add CSP meta tag that will block cross-origin AJAX
//var cspMetaTag = document.createElement('meta');
//cspMetaTag.setAttribute('http-equiv', 'Content-Security-Policy');
//cspMetaTag.setAttribute('content', "connect-src 'self' http://localhost:5000/check_user/ ");
//document.querySelector('head').appendChild(cspMetaTag);

document.querySelectorAll('[href^="/user/"]').forEach(async element => {
    const username = element.href.split('/user/')[1].slice(0,-1);

    const response = await fetch(`http://localhost:5000/check_user/${username}`);
    const data = await response.json();
    
    console.log("Hmmmm...");
    
    if(data.is_bot) {
	console.log(`Found a bot! ${username}`);
        element.style.backgroundColor = '#ffebee';
        element.insertAdjacentHTML('afterend', 
            `<span class="bot-tag" style="color:red">⚠️ ${data.score} Bot Score</span>`);
    }
});
