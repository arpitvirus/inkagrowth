document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const sidebarToggles = document.querySelectorAll('[data-sidebar-toggle]');
    const sidebarClosers = document.querySelectorAll('[data-sidebar-close]');

    sidebarToggles.forEach((button) => {
        button.addEventListener('click', () => body.classList.add('sidebar-open'));
    });

    sidebarClosers.forEach((button) => {
        button.addEventListener('click', () => body.classList.remove('sidebar-open'));
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            body.classList.remove('sidebar-open');
        }
    });

    document.querySelectorAll('[data-confirm]').forEach((link) => {
        link.addEventListener('click', (event) => {
            const message = link.getAttribute('data-confirm') || 'Are you sure?';
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll('[data-toast-close]').forEach((button) => {
        button.addEventListener('click', () => dismissToast(button.closest('[data-toast]')));
    });

    setTimeout(() => {
        document.querySelectorAll('[data-toast]').forEach(dismissToast);
    }, 5500);

    if (window.lucide) {
        window.lucide.createIcons();
    }
});

function dismissToast(toast) {
    if (!toast) {
        return;
    }

    toast.classList.add('is-hiding');
    setTimeout(() => toast.remove(), 240);
}
