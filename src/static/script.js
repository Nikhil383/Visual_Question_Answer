document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const placeholderText = document.querySelector('.placeholder-text');
    const submitBtn = document.getElementById('submitBtn');
    const questionInput = document.getElementById('questionInput');
    const loading = document.getElementById('loading');
    const answerBox = document.getElementById('answerBox');
    const answerText = document.getElementById('answerText');
    const errorBox = document.getElementById('errorBox');
    const errorText = document.getElementById('errorText');

    // Handle Image Upload Click
    imagePreview.addEventListener('click', () => {
        imageInput.click();
    });

    // Handle Drag and Drop
    imagePreview.addEventListener('dragover', (e) => {
        e.preventDefault();
        imagePreview.style.borderColor = 'var(--primary-color)';
    });

    imagePreview.addEventListener('dragleave', () => {
        imagePreview.style.borderColor = 'var(--border-color)';
    });

    imagePreview.addEventListener('drop', (e) => {
        e.preventDefault();
        imagePreview.style.borderColor = 'var(--border-color)';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageFile(file);
        }
    });

    // Handle File Selection
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageFile(file);
        }
    });

    function handleImageFile(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
            placeholderText.style.display = 'none';
            imagePreview.classList.add('has-image');
        };
        reader.readAsDataURL(file);
    }

    // Handle Submit
    submitBtn.addEventListener('click', async () => {
        const imageFile = imageInput.files[0];
        const question = questionInput.value.trim();

        // Reset state
        errorBox.style.display = 'none';
        answerBox.style.display = 'none';

        if (!imageFile && !imagePreview.classList.contains('has-image')) {
            showError("Please upload an image first.");
            return;
        }

        // Note: For drag and drop without input update, we might need to store the file object separately
        // But for now typical flow updates input or we can adapt to separate state if needed.
        // Assuming input is updated or we rely on 'imageInput.files[0]' 
        // If image was dragged, we need to manually assign it to input or keep ref?
        // Actually, let's keep it simple: input handles standard case. 
        // If DragDrop populated preview but not input.files, we need to fix. 
        // Let's make handleImageFile assign to DataTransfer for input if possible or keep file ref.

        if (!imageFile) {
            // If drag drop happened, we might not have it in files.
            // Simplest fix for this demo: Require user to click to upload or ensure drop updates input.
            // Let's assume standard click for now, or just trust imageInput has it.
            // If drop:
        }

        if (!question) {
            showError("Please ask a question.");
            return;
        }

        loading.style.display = 'flex';

        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
        formData.append('question', question);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            loading.style.display = 'none';

            if (response.ok) {
                answerText.textContent = data.answer;
                answerBox.style.display = 'block';
            } else {
                showError(data.error || "An error occurred.");
            }
        } catch (err) {
            loading.style.display = 'none';
            showError("Failed to connect to the server.");
        }
    });

    function showError(msg) {
        errorText.textContent = msg;
        errorBox.style.display = 'block';
    }

    // Improve Drag Drop to update input files - optional but good for UX
    // (A bit complex safely across browsers, but okay for demo to just use internal var if we wanted)
    // Here we'll rely on the user picking the file via dialog if drop doesn't populate input (it won't by default).
    // Let's quickly add a little helper to set the input files on drop if possible, or just store the file.

    let droppedFile = null;
    imagePreview.addEventListener('drop', (e) => {
        droppedFile = e.dataTransfer.files[0];
        // Try to assign to input (modern browsers allow this)
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(droppedFile);
        imageInput.files = dataTransfer.files;
    });

});
