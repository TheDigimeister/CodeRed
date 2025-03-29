document.querySelectorAll('[href^="/user/"]').forEach(async element => {
    const username = element.href.split('/user/')[1];
    const response = await fetch(`http://localhost:5000/check_user/${username}`);
    const data = await response.json();
    
    if(data.is_bot) {
        element.style.backgroundColor = '#ffebee';
        element.insertAdjacentHTML('afterend', 
            `<span class="bot-tag" style="color:red">⚠️ ${data.score} Bot Score</span>`);
    }
});
