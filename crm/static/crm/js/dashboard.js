document.addEventListener('DOMContentLoaded', () => {
    const dataNode = document.getElementById('dashboard-chart-data');

    if (!dataNode || !window.Chart) {
        return;
    }

    const data = JSON.parse(dataNode.textContent);
    const leadCanvas = document.getElementById('leadStatusChart');
    const taskCanvas = document.getElementById('taskStatusChart');

    if (leadCanvas) {
        new Chart(leadCanvas, {
            type: 'doughnut',
            data: {
                labels: data.lead_status_labels,
                datasets: [{
                    data: data.lead_status_values,
                    backgroundColor: ['#2563eb', '#0f9f6e', '#f59e0b', '#7c3aed', '#16a34a', '#e11d48'],
                    borderWidth: 0,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                },
                cutout: '68%',
            },
        });
    }

    if (taskCanvas) {
        new Chart(taskCanvas, {
            type: 'bar',
            data: {
                labels: data.task_status_labels,
                datasets: [{
                    label: 'Tasks',
                    data: data.task_status_values,
                    backgroundColor: ['#2563eb', '#f59e0b', '#0f9f6e'],
                    borderRadius: 6,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0,
                        },
                    },
                },
            },
        });
    }
});
