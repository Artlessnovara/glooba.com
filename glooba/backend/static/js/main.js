document.addEventListener('DOMContentLoaded', function() {
    // ... (other listeners)

    // --- Post Interactions ---
    document.addEventListener('click', function(event) {
        const postContainer = event.target.closest('.post-container');
        if (!postContainer) return;

        const postId = postContainer.dataset.postId;
        let url = '';
        let targetSpan = null;
        let targetText = '';

        if (event.target.matches('.like-btn')) {
            url = `/like_post/${postId}`;
            targetSpan = postContainer.querySelector('.likes-count');
            targetText = 'Likes';
        } else if (event.target.matches('.glow-btn')) {
            url = `/glow_post/${postId}`;
            targetSpan = postContainer.querySelector('.glows-count');
            targetText = 'Glows';
        } else if (event.target.matches('.share-btn')) {
            url = `/share_post/${postId}`;
            targetSpan = postContainer.querySelector('.shares-count');
            targetText = 'Shares';
        } else if (event.target.matches('.comment-btn')) {
            const commentSection = postContainer.querySelector('.comment-section');
            if (commentSection) {
                commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
            }
        }

        if (url) {
            fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                if (targetSpan && data.count !== undefined) {
                    targetSpan.textContent = `${data.count} ${targetText}`;
                }
                if (data.active !== undefined) {
                    event.target.classList.toggle('active', data.active);
                }
            });
        }
    });

    document.addEventListener('submit', function(event) {
        if (event.target.matches('.comment-form')) {
            event.preventDefault();
            const form = event.target;
            const postContainer = form.closest('.post-container');
            const postId = postContainer.dataset.postId;
            const commentInput = form.querySelector('.comment-input');
            const commentText = commentInput.value;

            if (commentText) {
                fetch(`/comment_on_post/${postId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ comment: commentText })
                })
                .then(response => response.json())
                .then(data => {
                    commentInput.value = '';
                    form.parentElement.style.display = 'none';
                    const commentCounter = postContainer.querySelector('.comments-count');
                    commentCounter.textContent = `${data.count} Comments`;
                });
            }
        }
    });

    // --- Live Username Availability Check ---
    const usernameInput = document.getElementById('username');
    const availabilityCheck = document.querySelector('.availability-check');
    if (usernameInput && availabilityCheck) {
        usernameInput.addEventListener('keyup', function() {
            const username = this.value;
            if (username.length > 2) {
                fetch('/check_username', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: username })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        availabilityCheck.textContent = `@${username} is available!`;
                        availabilityCheck.style.color = '#00E0FF';
                    } else {
                        availabilityCheck.textContent = `@${username} is taken.`;
                        availabilityCheck.style.color = '#ff4d4d';
                    }
                });
            } else {
                availabilityCheck.textContent = '';
            }
        });
    }

    // --- Password Strength Indicator ---
    const passwordStrengthInput = document.querySelector('#signup .password-group input');
    const strengthIndicator = document.querySelector('.password-strength');
    if (passwordStrengthInput && strengthIndicator) {
        passwordStrengthInput.addEventListener('keyup', function() {
            const password = this.value;
            let strength = 0;
            if (password.length >= 8) strength++;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
            if (password.match(/[0-9]/)) strength++;
            if (password.match(/[^a-zA-Z0-9]/)) strength++;

            strengthIndicator.style.width = `${strength * 25}%`;
            if (strength <= 1) {
                strengthIndicator.style.backgroundColor = '#ff4d4d'; // Weak
            } else if (strength <= 3) {
                strengthIndicator.style.backgroundColor = '#FFA500'; // Medium
            } else {
                strengthIndicator.style.backgroundColor = '#00E0FF'; // Strong
            }
        });
    }
});
