/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

// **Fungsi untuk mengambil data program dari backend**
async function fetchProgramData() {
    const response = await fetch('/get_program_data');
    const data = await response.json();
    return data;
}
async function searchPrograms() {
const query = document.getElementById('search-bar').value.trim();  // Ambil query dari input
const response = await fetch(`/search?q=${encodeURIComponent(query)}`);  // Kirim ke backend
const data = await response.json();  // Terima data JSON dari backend

renderPortfolioItems(data);  // Render hasil pencarian
}

function renderPortfolioItems(data) {
const portfolioContainer = document.getElementById('portfolio-items');
portfolioContainer.innerHTML = '';  // Bersihkan hasil sebelumnya

if (data.length === 0) {
    portfolioContainer.innerHTML = '<p class="text-center">No programs found.</p>';
    return;
}

// Tampilkan setiap item hasil pencarian
data.forEach((program) => {
    portfolioContainer.innerHTML += `
        <div class="col-lg-4 col-sm-6 mb-4">
            <div class="portfolio-item">
                <h4>${program.name}</h4>
                <p><strong>Location:</strong> ${program.location}</p>
                <p><strong>Status:</strong> ${program.status}</p>
                <p><strong>Participants:</strong> ${program.participants}</p>
                <p><strong>Budget:</strong> Rp.${program.budget}</p>
                <button class="btn btn-secondary" onclick="viewDetails('${program._id}')">View Details</button>
            </div>
        </div>
    `;
});
}

function viewDetails(id) {
// Arahkan ke halaman detail program
window.location.href = `/program/${id}`;
}

// Fungsi untuk menghitung rata-rata
function calculateAverage(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
}

// Fungsi untuk menghitung total berdasarkan kategori tertentu
function groupByAndSum(data, groupKey, sumKey) {
    return data.reduce((acc, curr) => {
        acc[curr[groupKey]] = (acc[curr[groupKey]] || 0) + curr[sumKey];
        return acc;
    }, {});
}

// 1. Chart: Jumlah Peserta per Program (Bar Chart)
function createParticipantsChart(ctx, data) {
    const labels = data.map(program => program.name);
    const participants = data.map(program => program.participants);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Participants',
                data: participants,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 2. Chart: Distribusi Anggaran (Pie Chart)
function createBudgetChart(ctx, data) {
    const labels = data.map(program => program.name);
    const budgets = data.map(program => program.budget);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Budget',
                data: budgets,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// 3. Chart: Status Program (Doughnut Chart)
function createStatusChart(ctx, data) {
    const statusCounts = groupByAndSum(data, 'status', 'participants');

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(statusCounts),
            datasets: [{
                label: 'Program Status',
                data: Object.values(statusCounts),
                backgroundColor: ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.5)', 'rgba(255, 206, 86, 0.5)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// 4. Chart: Program per Kategori (Horizontal Bar Chart)
function createProgramsPerCategoryChart(ctx, data) {
    const categoryCounts = groupByAndSum(data, 'category', 'participants');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(categoryCounts),
            datasets: [{
                label: 'Programs per Category',
                data: Object.values(categoryCounts),
                backgroundColor: 'rgba(255, 206, 86, 0.5)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y' // Horizontal bar chart
        }
    });
}

// 5. Chart: Lokasi Program (Bubble Chart)
function createProgramsPerLocationChart(ctx, data) {
    const datasets = data.map(program => ({
        label: program.location,
        data: [{ x: program.budget, y: program.participants, r: Math.sqrt(program.participants) }],
        backgroundColor: 'rgba(75, 192, 192, 0.5)'
    }));

    new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Budget' },
                    beginAtZero: true
                },
                y: {
                    title: { display: true, text: 'Participants' },
                    beginAtZero: true
                }
            }
        }
    });
}

// 6. Chart: Rata-rata Anggaran per Kategori (Bar Chart)
function createAverageBudgetPerCategoryChart(ctx, data) {
    const categoryBudgets = groupByAndSum(data, 'category', 'budget');
    const categoryCounts = groupByAndSum(data, 'category', 'participants');
    const averageBudgets = Object.keys(categoryBudgets).map(category => categoryBudgets[category] / categoryCounts[category]);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(categoryBudgets),
            datasets: [{
                label: 'Average Budget',
                data: averageBudgets,
                backgroundColor: 'rgba(153, 102, 255, 0.5)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// 7. Chart: Perbandingan Peserta dan Anggaran (Line Chart)
function createParticipantsVsBudgetChart(ctx, data) {
    const labels = data.map(program => program.name);
    const participants = data.map(program => program.participants);
    const budgets = data.map(program => program.budget);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Participants',
                    data: participants,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    fill: true
                },
                {
                    label: 'Budget',
                    data: budgets,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// 8. Chart: Total Anggaran dan Total Peserta (Polar Area Chart)
function createTotalBudgetParticipantsChart(ctx, data) {
    const categories = [...new Set(data.map(program => program.category))];
    const categoryBudgets = groupByAndSum(data, 'category', 'budget');
    const categoryParticipants = groupByAndSum(data, 'category', 'participants');

    new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: categories,
            datasets: [
                {
                    label: 'Total Budget',
                    data: Object.values(categoryBudgets),
                    backgroundColor: 'rgba(75, 192, 192, 0.5)'
                },
                {
                    label: 'Total Participants',
                    data: Object.values(categoryParticipants),
                    backgroundColor: 'rgba(153, 102, 255, 0.5)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Inisialisasi semua chart
async function initCharts() {
    const data = await fetchProgramData();

    createParticipantsChart(document.getElementById('participantsChart').getContext('2d'), data);
    createBudgetChart(document.getElementById('budgetChart').getContext('2d'), data);
    createStatusChart(document.getElementById('statusChart').getContext('2d'), data);
    createProgramsPerCategoryChart(document.getElementById('categoryChart').getContext('2d'), data);
    createProgramsPerLocationChart(document.getElementById('locationChart').getContext('2d'), data);
    createAverageBudgetPerCategoryChart(document.getElementById('averageBudgetChart').getContext('2d'), data);
    createParticipantsVsBudgetChart(document.getElementById('participantsVsBudgetChart').getContext('2d'), data);
    createTotalBudgetParticipantsChart(document.getElementById('totalChart').getContext('2d'), data);
}

document.addEventListener('DOMContentLoaded', initCharts);

async function fetchPortfolioData() {
    const response = await fetch('/get_artikel_data'); // **Ambil data dari backend**
    const programs = await response.json();
    return programs;
}

function renderPortfolioItems(data) {
    const portfolioContainer = document.getElementById('portfolio-items');
    const modalContainer = document.getElementById('portfolioModals');

    portfolioContainer.innerHTML = ''; // **Bersihkan kontainer sebelum menambahkan item baru**
    modalContainer.innerHTML = '';

    data.forEach((program, index) => {
        // **Buat item portfolio**
        portfolioContainer.innerHTML += `
            <div class="col-lg-4 col-md-6">
                <div class="portfolio-card">
                    <div class="portfolio-title">${program.name}</div>
                    <div class="portfolio-subtitle">${program.location}</div>
                    <button class="portfolio-btn" data-bs-toggle="modal" data-bs-target="#portfolioModal${index}">
                        View Details
                    </button>
                </div>
            </div>
        `;

        // **Buat modal untuk setiap item**
        modalContainer.innerHTML += `
            <div class="portfolio-modal modal fade" id="portfolioModal${index}" tabindex="-1" role="dialog" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="close-modal" data-bs-dismiss="modal"><img src="../static/assets/img/close-icon.svg" alt="Close modal" /></div>
                        <div class="container">
                            <div class="row justify-content-center">
                                <div class="col-lg-8">
                                    <div class="modal-body">
                                        <h2 class="text-uppercase">${program.name}</h2>
                                        <p class="item-intro text-muted">Location: ${program.location}</p>
                                        <p>Participants: ${program.participants}</p>
                                        <p>Budget: Rp.${program.budget}</p>
                                        <p>Status: ${program.status}</p>
                                        <p>Detail: ${program.detail}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const portfolioData = await fetchPortfolioData(); // **Ambil data portfolio dari backend**
    renderPortfolioItems(portfolioData); // **Render data portfolio ke halaman**
});