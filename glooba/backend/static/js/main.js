document.addEventListener('DOMContentLoaded', function() {
    // --- Profile Picture Preview ---
    const profilePicInput = document.getElementById('profile_pic');
    const picPreview = document.getElementById('pic_preview');

    if (profilePicInput && picPreview) {
        profilePicInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    picPreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // --- Interest Tag Selection ---
    const interestsContainer = document.querySelector('.interests-container');
    if (interestsContainer) {
        interestsContainer.addEventListener('click', function(event) {
            if (event.target.classList.contains('interest-tag')) {
                event.target.classList.toggle('selected');
            }
        });
    }

    // --- Show/Hide Password on Login Form ---
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const passwordInput = document.getElementById('password');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.textContent = 'Hide';
            } else {
                passwordInput.type = 'password';
                this.textContent = 'Show';
            }
        });
    }

    // --- Post Interactions ---
    document.addEventListener('click', function(event) {
        const postContainer = event.target.closest('.post-container');
        if (!postContainer) return;

        const postId = postContainer.dataset.postId;
        let url = '';
        let targetSpan = null;

        if (event.target.matches('.like-btn')) {
            url = `/like_post/${postId}`;
            targetSpan = postContainer.querySelector('.likes-count');
        } else if (event.target.matches('.glow-btn')) {
            url = `/glow_post/${postId}`;
            targetSpan = postContainer.querySelector('.glows-count');
        } else if (event.target.matches('.share-btn')) {
            url = `/share_post/${postId}`;
            targetSpan = postContainer.querySelector('.shares-count');
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
                if (targetSpan && data.likes !== undefined) {
                    targetSpan.textContent = `${data.likes} Likes`;
                }
                if (targetSpan && data.glows !== undefined) {
                    targetSpan.textContent = `${data.glows} Glows`;
                }
                if (targetSpan && data.shares !== undefined) {
                    targetSpan.textContent = `${data.shares} Shares`;
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
                .then(response => {
                    if (response.ok) {
                        // Ideally, we would dynamically add the new comment to the UI
                        // For now, we just clear the input and hide the form
                        commentInput.value = '';
                        form.parentElement.style.display = 'none';
                        // And maybe update the comment count
                        const commentCounter = postContainer.querySelector('.comments-count');
                        const currentCount = parseInt(commentCounter.textContent.split(' ')[0]);
                        commentCounter.textContent = `${currentCount + 1} Comments`;
                    }
                });
            }
        }
    });
});
