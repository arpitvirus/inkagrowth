document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-task-status-url]').forEach((select) => {
        select.addEventListener('change', async () => {
            const url = select.getAttribute('data-task-status-url');
            const originalValue = select.getAttribute('data-original-value') || select.value;
            const formData = new FormData();

            formData.append('status', select.value);
            select.disabled = true;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error('Status update failed');
                }

                select.setAttribute('data-original-value', select.value);
            } catch (error) {
                select.value = originalValue;
                window.alert('Could not update task status. Please try again.');
            } finally {
                select.disabled = false;
            }
        });
    });
});

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];

    for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(`${name}=`)) {
            return decodeURIComponent(trimmed.substring(name.length + 1));
        }
    }

    return '';
}
