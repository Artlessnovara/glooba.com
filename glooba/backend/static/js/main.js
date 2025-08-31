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
});
