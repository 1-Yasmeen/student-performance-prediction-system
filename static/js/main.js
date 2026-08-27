document.addEventListener("DOMContentLoaded", function () {

    console.log("App initialized");

    initializeTooltips();
    initializeAnimations();
    attachEventListeners();

    if (Array.isArray(window.studentsData)) {

        console.log(
            "studentsData loaded:",
            window.studentsData.length,
            "students"
        );

        populateUploadSummary(
            window.studentsData
        );

        populateClassSummary(
            window.studentsData
        );

        initializePerformanceSelection();

        createCharts(
            window.studentsData
        );

        initializePagination();

    } else {

        console.warn(
            "studentsData is not available."
        );

    }

});










// ============================================
// ANIMATIONS
// ============================================

function initializeAnimations() {
    const elements = document.querySelectorAll(
        ".card, .dashboard-card, .form-box"
    );

    elements.forEach((el, index) => {
        // Prevent the animation from being applied repeatedly
        if (el.dataset.animated === "true") {
            return;
        }

        el.dataset.animated = "true";

        el.style.opacity = "0";
        el.style.animation =
            `fadeIn 0.6s ease ${index * 0.1}s forwards`;
    });
}

// ============================================
// TOOLTIPS
// ============================================

function initializeTooltips() {
    const tooltips = document.querySelectorAll("[data-tooltip]");

    tooltips.forEach((el) => {
        el.addEventListener("mouseenter", showTooltip);
        el.addEventListener("mouseleave", hideTooltip);
    });
}

function showTooltip(e) {
    hideTooltip();

    const element = e.currentTarget;
    const message = element.getAttribute("data-tooltip");

    if (!message) return;

    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    tooltip.textContent = message;

    const rect = element.getBoundingClientRect();

    tooltip.style.cssText = `
        position: fixed;
        left: ${rect.left + rect.width / 2}px;
        top: ${rect.bottom + 8}px;
        transform: translateX(-50%);
        background: #1e293b;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        z-index: 10000;
        pointer-events: none;
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;

    document.body.appendChild(tooltip);
}

function hideTooltip() {
    document.querySelectorAll(".tooltip").forEach((tooltip) => {
        tooltip.remove();
    });
}

// ============================================
// SEARCH & FILTER
// ============================================

function searchStudents() {
    const input = document.getElementById("studentSearch");
    const table = document.getElementById("studentTable");

    if (!input || !table) return;

    const filter = input.value.trim().toUpperCase();
    const rows = table.querySelectorAll("tbody tr");

    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");

        if (!cells.length) return;

        const studentID = cells[0];
        const text = studentID.textContent || "";

        if (text.toUpperCase().includes(filter)) {
            row.style.display = "";
            row.style.animation = "fadeIn 0.3s ease";
        } else {
            row.style.display = "none";
        }
    });

    showNoResultsMessage(table, filter);
}

function showNoResultsMessage(table, filter) {
    const existingMsg = document.getElementById("noResults");

    if (existingMsg) {
        existingMsg.remove();
    }

    if (!filter) return;

    const visibleRows = Array.from(
        table.querySelectorAll("tbody tr")
    ).filter((row) => row.style.display !== "none");

    if (visibleRows.length === 0) {
        const msg = document.createElement("div");

        msg.id = "noResults";
        msg.className = "alert alert-info";
        msg.textContent = `No results found for: ${filter}`;

        msg.style.cssText = `
            margin-top: 20px;
            animation: slideIn 0.3s ease;
        `;

        table.parentNode.appendChild(msg);
    }
}

// ============================================
// SUMMARY
// ============================================

function calculateSummary(students) {
    const counts = {
        high: 0,
        average: 0,
        low: 0
    };

    let totalConfidence = 0;

    students.forEach((student) => {
        const category = getPredictionCategory(
            student.prediction
        );

        counts[category]++;

        totalConfidence +=
            parseFloat(student.confidence) || 0;
    });

    const averageConfidence = students.length
        ? totalConfidence / students.length
        : 0;

    return {
        counts,
        averageConfidence
    };
}

function populateUploadSummary(students) {
    const summary = {
        overallTotal:
            document.getElementById("overallTotal"),

        highCount:
            document.getElementById("highCount"),

        averageCount:
            document.getElementById("averageCount"),

        lowCount:
            document.getElementById("lowCount"),

        averageConfidence:
            document.getElementById("averageConfidence")
    };

    if (!summary.overallTotal) return;

    const result = calculateSummary(students);

    summary.overallTotal.textContent = students.length;

    if (summary.highCount) {
        summary.highCount.textContent =
            result.counts.high;
    }

    if (summary.averageCount) {
        summary.averageCount.textContent =
            result.counts.average;
    }

    if (summary.lowCount) {
        summary.lowCount.textContent =
            result.counts.low;
    }

    if (summary.averageConfidence) {
        summary.averageConfidence.textContent =
            `${result.averageConfidence.toFixed(1)}%`;
    }
}

function populateClassSummary(students) {
    const summary = {
        classTotal:
            document.getElementById("classTotal"),

        classHighCount:
            document.getElementById("classHighCount"),

        classAverageCount:
            document.getElementById("classAverageCount"),

        classLowCount:
            document.getElementById("classLowCount"),

        classAverageConfidence:
            document.getElementById(
                "classAverageConfidence"
            )
    };

    if (!summary.classTotal) return;

    const result = calculateSummary(students);

    summary.classTotal.textContent = students.length;

    if (summary.classHighCount) {
        summary.classHighCount.textContent =
            result.counts.high;
    }

    if (summary.classAverageCount) {
        summary.classAverageCount.textContent =
            result.counts.average;
    }

    if (summary.classLowCount) {
        summary.classLowCount.textContent =
            result.counts.low;
    }

    if (summary.classAverageConfidence) {
        summary.classAverageConfidence.textContent =
            `${result.averageConfidence.toFixed(1)}%`;
    }
}

function updateSummary(data) {
    if (!Array.isArray(data)) return;

    if (document.getElementById("overallTotal")) {
        populateUploadSummary(data);
    }

    if (document.getElementById("classTotal")) {
        populateClassSummary(data);
    }
}

// ============================================
// FORM VALIDATION
// ============================================

function validateForm(formId) {
    const form = document.getElementById(formId);

    if (!form) return true;

    const inputs = form.querySelectorAll(
        "input[required], textarea[required], select[required]"
    );

    let isValid = true;

    inputs.forEach((input) => {
        if (!String(input.value).trim()) {
            input.style.borderColor = "#ef4444";
            input.style.boxShadow =
                "0 0 0 4px rgba(239, 68, 68, 0.1)";

            isValid = false;
        } else {
            input.style.borderColor = "#e2e8f0";
            input.style.boxShadow = "none";
        }
    });

    return isValid;
}

// ============================================
// LOADING STATES
// ============================================

function showLoading(buttonId) {
    const btn = document.getElementById(buttonId);

    if (!btn) return;

    btn.disabled = true;
    btn.style.opacity = "0.6";

    const originalText = btn.textContent;

    btn.setAttribute(
        "data-original-text",
        originalText
    );

    btn.textContent = "Loading...";
}

function hideLoading(buttonId) {
    const btn = document.getElementById(buttonId);

    if (!btn) return;

    btn.disabled = false;
    btn.style.opacity = "1";

    const originalText =
        btn.getAttribute("data-original-text");

    btn.textContent = originalText || "Submit";
}

// ============================================
// NOTIFICATIONS
// ============================================

function showNotification(message, type = "info") {
    const notification = document.createElement("div");

    notification.className = `alert alert-${type}`;
    notification.textContent = message;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation =
            "slideOut 0.3s ease";

        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// ============================================
// COPY TO CLIPBOARD
// ============================================

async function copyToClipboard(text, buttonId) {
    try {
        if (
            navigator.clipboard &&
            window.isSecureContext
        ) {
            await navigator.clipboard.writeText(text);
        } else {
            const textarea =
                document.createElement("textarea");

            textarea.value = text;
            textarea.style.position = "fixed";
            textarea.style.opacity = "0";

            document.body.appendChild(textarea);

            textarea.focus();
            textarea.select();

            document.execCommand("copy");

            textarea.remove();
        }

        const btn = document.getElementById(buttonId);

        if (btn) {
            const originalText = btn.textContent;

            btn.textContent = "Copied!";

            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        }
    } catch (error) {
        console.error("Clipboard error:", error);

        showNotification(
            "Unable to copy text.",
            "danger"
        );
    }
}

// ============================================
// SMOOTH SCROLL
// ============================================

function smoothScroll(elementId) {
    const element =
        document.getElementById(elementId);

    if (element) {
        element.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

// ============================================
// MODAL HANDLERS
// ============================================

function openModal(modalId) {
    const modal =
        document.getElementById(modalId);

    if (!modal) return;

    modal.style.display = "block";
    modal.style.animation =
        "fadeIn 0.3s ease";

    document.body.classList.add("modal-open");
}

function closeModal(modalId) {
    const modal =
        document.getElementById(modalId);

    if (!modal) return;

    modal.style.animation =
        "fadeOut 0.3s ease";

    setTimeout(() => {
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
    }, 300);
}

// ============================================
// TABLE SORTING
// ============================================

function sortTable(
    tableId,
    columnIndex,
    ascending = true
) {
    const table =
        document.getElementById(tableId);

    if (!table) return;

    const tbody = table.querySelector("tbody");

    if (!tbody) return;

    const rows = Array.from(
        tbody.querySelectorAll("tr")
    );

    rows.sort((a, b) => {
        const aCell = a.cells[columnIndex];
        const bCell = b.cells[columnIndex];

        if (!aCell || !bCell) return 0;

        const aValue = aCell.textContent.trim();
        const bValue = bCell.textContent.trim();

        const aNumber = parseFloat(
            aValue.replace("%", "")
        );

        const bNumber = parseFloat(
            bValue.replace("%", "")
        );

        const aIsNumber =
            !Number.isNaN(aNumber);

        const bIsNumber =
            !Number.isNaN(bNumber);

        if (aIsNumber && bIsNumber) {
            return ascending
                ? aNumber - bNumber
                : bNumber - aNumber;
        }

        return ascending
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });

    rows.forEach((row) => {
        tbody.appendChild(row);
    });
}

// ============================================
// PREDICTION HELPERS
// ============================================

function getPredictionCategory(prediction) {
    const normalized = String(prediction || "")
        .trim()
        .toLowerCase();

    if (
        normalized === "excellent" ||
        normalized === "good" ||
        normalized === "high"
    ) {
        return "high";
    }

    if (
        normalized === "average" ||
        normalized === "medium"
    ) {
        return "average";
    }

    if (
        normalized === "low" ||
        normalized === "poor"
    ) {
        return "low";
    }

    // Keep unknown values from breaking the summary.
    return "low";
}

function getDisplayLabel(category) {
    if (category === "all") {
        return "All Students";
    }

    return (
        category.charAt(0).toUpperCase() +
        category.slice(1)
    );
}

// ============================================
// SELECTION DETAILS
// ============================================

function updateSelectionDetails(category, rows) {
    const info =
        document.getElementById("performanceInfo");

    const breakdown =
        document.getElementById(
            "predictionBreakdown"
        );

    if (!info || !breakdown) return;

    const totalRows = document.querySelectorAll(
        "#studentTable tbody tr"
    ).length;

    const count = rows.length;

    const percentage = totalRows
        ? ((count / totalRows) * 100).toFixed(1)
        : "0.0";

    const displayLabel =
        getDisplayLabel(category);

    info.textContent =
        `${displayLabel}: ${count} student${count === 1 ? "" : "s"} — ${percentage}% of total.`;

    const predictions = rows.reduce(
        (acc, row) => {
            const prediction =
                row.dataset.prediction ||
                "Unknown";

            acc[prediction] =
                (acc[prediction] || 0) + 1;

            return acc;
        },
        {}
    );

    breakdown.innerHTML =
        Object.entries(predictions)
            .map(([prediction, value]) => {
                return `
                    <div class="prediction-breakdown-item">
                        <span>${escapeHTML(prediction)}</span>
                        <span>${value}</span>
                    </div>
                `;
            })
            .join("");
}


   
   


function filterPerformance(category) {
    const table =
        document.getElementById("studentTable");

    if (!table) return;

    const rows = Array.from(
        table.querySelectorAll("tbody tr")
    );

    // Reset pagination whenever the filter changes
    currentStudentPage = 1;

    // Update active filter button
    document
        .querySelectorAll(".performance-filter")
        .forEach((button) => {
            button.classList.toggle(
                "active",
                button.dataset.category === category
            );
        });

    // --------------------------------------------
    // Apply performance filter
    // --------------------------------------------

    rows.forEach((row) => {
        const prediction =
            row.dataset.prediction || "";

        const rowCategory =
            getPredictionCategory(prediction);

        const matches =
            category === "all" ||
            rowCategory === category;

        // IMPORTANT:
        // This records the filter state.
        // Pagination will decide which 50 are visible.
        row.dataset.filteredOut =
            matches ? "false" : "true";
    });

    // --------------------------------------------
    // IMPORTANT:
    // Get ALL students belonging to the selected
    // category, NOT just the 50 visible rows.
    // --------------------------------------------

    const filteredRows = rows.filter(
        (row) =>
            row.dataset.filteredOut !== "true"
    );

    const filtered = filteredRows.map(
        (row) => ({
            prediction:
                row.dataset.prediction || "",

            confidence:
                parseFloat(
                    row.dataset.confidence
                ) || 0
        })
    );

    // --------------------------------------------
    // CHART
    //
    // This receives ALL filtered students.
    // Pagination does NOT affect the chart.
    // --------------------------------------------

    updateCharts(filtered);

    // --------------------------------------------
    // DETAILS
    //
    // Also uses ALL filtered students.
    // --------------------------------------------

    updateSelectionDetails(
        category,
        filteredRows
    );

    // --------------------------------------------
    // TABLE PAGINATION
    //
    // Only the table is limited to 50 rows.
    // --------------------------------------------

    if (
        typeof updateStudentPagination ===
        "function"
    ) {
        updateStudentPagination();
    }
}

// ============================================
// CHART CREATION
// ============================================

function createCharts(data) {
    if (!Array.isArray(data)) {
        console.warn(
            "Chart data must be an array."
        );

        return;
    }

    if (typeof window.Chart === "undefined") {
        console.error(
            "Chart.js is not loaded. Make sure Chart.js is loaded before main.js."
        );

        return;
    }

    const performanceValues = {
        high: 0,
        average: 0,
        low: 0
    };

    const confidenceValues = {
        high: 0,
        average: 0,
        low: 0
    };

    data.forEach((student) => {
        const category =
            getPredictionCategory(
                student.prediction
            );

        performanceValues[category]++;

        confidenceValues[category] +=
            parseFloat(student.confidence) || 0;
    });

    const performanceLabels = [
        "High",
        "Average",
        "Low"
    ];

    const performanceCounts = [
        performanceValues.high,
        performanceValues.average,
        performanceValues.low
    ];

    const averageConfidences = [
        performanceValues.high
            ? confidenceValues.high /
              performanceValues.high
            : 0,

        performanceValues.average
            ? confidenceValues.average /
              performanceValues.average
            : 0,

        performanceValues.low
            ? confidenceValues.low /
              performanceValues.low
            : 0
    ];

    const perfCanvas =
        document.getElementById(
            "performanceChart"
        );

    const confCanvas =
        document.getElementById(
            "confidenceChart"
        );

    if (!perfCanvas || !confCanvas) {
        console.warn(
            "Chart canvas elements were not found."
        );

        return;
    }

    // Destroy existing charts.
    if (
        window.performanceChart &&
        typeof window.performanceChart.destroy ===
            "function"
    ) {
        window.performanceChart.destroy();
    }

    if (
        window.confidenceChart &&
        typeof window.confidenceChart.destroy ===
            "function"
    ) {
        window.confidenceChart.destroy();
    }

    // ========================================
    // PERFORMANCE CHART
    // ========================================

    window.performanceChart = new Chart(
        perfCanvas,
        {
            type: "doughnut",

            data: {
                labels: performanceLabels,

                datasets: [
                    {
                        data: performanceCounts,

                        backgroundColor: [
                            "#10b981",
                            "#f59e0b",
                            "#ef4444"
                        ],

                        borderColor: "#ffffff",
                        borderWidth: 2
                    }
                ]
            },

            options: {
    responsive: true,
    maintainAspectRatio: false,

    animation: {
        duration: 500
    },

    plugins: {
                    legend: {
                        position: "bottom"
                    }
                },

                onClick(event, elements) {
                    if (!elements.length) return;

                    const index =
                        elements[0].index;

                    const categories = [
                        "high",
                        "average",
                        "low"
                    ];

                    filterPerformance(
                        categories[index]
                    );
                }
            }
        }
    );

    // ========================================
    // CONFIDENCE CHART
    // ========================================

    window.confidenceChart = new Chart(
        confCanvas,
        {
            type: "bar",

            data: {
                labels: performanceLabels,

                datasets: [
                    {
                        label:
                            "Average Confidence",

                        data: averageConfidences,

                        backgroundColor: [
                            "#22c55e",
                            "#f59e0b",
                            "#ef4444"
                        ],

                        borderRadius: 8
                    }
                ]
            },

            options: {
    responsive: true,
    maintainAspectRatio: false,

    animation: {
        duration: 500
    },

    scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,

                        ticks: {
                            callback(value) {
                                return `${value}%`;
                            }
                        }
                    }
                },

                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        }
    );

    
}

function initializePerformanceSelection() {

    const table =
        document.getElementById("studentTable");

    if (!table) return;

    const rows = Array.from(
        table.querySelectorAll("tbody tr")
    );

    // Initially include every student
    rows.forEach((row) => {
        row.dataset.filteredOut = "false";
    });

    const allStudents = rows.map((row) => ({
        prediction:
            row.dataset.prediction || "",

        confidence:
            parseFloat(
                row.dataset.confidence
            ) || 0
    }));

    // Show initial class information
    updateSelectionDetails(
        "all",
        rows
    );

    // Update class summary
    populateClassSummary(
        allStudents
    );
}


// ============================================
// UPDATE CHARTS
// ============================================

function updateCharts(filtered) {
    const data = Array.isArray(filtered)
        ? filtered.map((item) => {
              if (!item) {
                  return {
                      prediction: "",
                      confidence: 0
                  };
              }

              // Supports:
              // { prediction, confidence }
              // and HTML table rows.
              if (item.dataset) {
                  return {
                      prediction:
                          item.dataset.prediction ||
                          "",

                      confidence:
                          parseFloat(
                              item.dataset.confidence
                          ) || 0
                  };
              }

              return {
                  prediction:
                      item.prediction || "",

                  confidence:
                      parseFloat(
                          item.confidence
                      ) || 0
              };
          })
        : [];

    if (
        window.performanceChart &&
        window.confidenceChart
    ) {
        const counts = {
            high: 0,
            average: 0,
            low: 0
        };

        const confidence = {
            high: 0,
            average: 0,
            low: 0
        };

        data.forEach((item) => {
            const category =
                getPredictionCategory(
                    item.prediction
                );

            counts[category]++;

            confidence[category] +=
                item.confidence || 0;
        });

        window.performanceChart.data.datasets[0]
            .data = [
                counts.high,
                counts.average,
                counts.low
            ];

        window.performanceChart.update();

        window.confidenceChart.data.datasets[0]
            .data = [
                counts.high
                    ? confidence.high /
                      counts.high
                    : 0,

                counts.average
                    ? confidence.average /
                      counts.average
                    : 0,

                counts.low
                    ? confidence.low /
                      counts.low
                    : 0
            ];

        window.confidenceChart.update();
    }

    updateSummary(data);
}

// ============================================
// EVENT LISTENERS
// ============================================

function attachEventListeners() {
    // Search
    const searchInput =
        document.getElementById(
            "studentSearch"
        );

    if (searchInput) {
        searchInput.addEventListener(
            "input",
            debounce(searchStudents, 150)
        );
    }

    // Form submissions
    const forms =
        document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener(
            "submit",
            function (e) {
                if (!validateForm(this.id)) {
                    e.preventDefault();

                    showNotification(
                        "Please fill in all required fields.",
                        "warning"
                    );
                }
            }
        );
    });

    // Change password
    const showPasswordBtn =
        document.getElementById(
            "showChangePassword"
        );

    if (showPasswordBtn) {
        showPasswordBtn.addEventListener(
            "click",
            () => {
                const panel =
                    document.getElementById(
                        "changePasswordPanel"
                    );

                if (panel) {
                    panel.classList.add(
                        "visible"
                    );
                }
            }
        );
    }

    const cancelPasswordBtn =
        document.getElementById(
            "cancelChangePassword"
        );

    if (cancelPasswordBtn) {
        cancelPasswordBtn.addEventListener(
            "click",
            () => {
                const panel =
                    document.getElementById(
                        "changePasswordPanel"
                    );

                if (panel) {
                    panel.classList.remove(
                        "visible"
                    );
                }
            }
        );
    }
}

// ============================================
// UTILITIES
// ============================================

function debounce(func, delay) {
    let timeoutId;

    return function (...args) {
        clearTimeout(timeoutId);

        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

function throttle(func, limit) {
    let lastFunc;
    let lastRan;

    return function (...args) {
        if (!lastRan) {
            func.apply(this, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);

            lastFunc = setTimeout(() => {
                if (
                    Date.now() - lastRan >=
                    limit
                ) {
                    func.apply(this, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
}

// ============================================
// API CALLS
// ============================================

async function fetchAPI(
    endpoint,
    options = {}
) {
    try {
        const response = await fetch(
            endpoint,
            {
                ...options,

                headers: {
                    "Content-Type":
                        "application/json",

                    ...(options.headers || {})
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP error! status: ${response.status}`
            );
        }

        return await response.json();
    } catch (error) {
        console.error(
            "API Error:",
            error
        );

        showNotification(
            "Error communicating with server.",
            "danger"
        );

        throw error;
    }
}

// ============================================
// HTML ESCAPE
// ============================================

function escapeHTML(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// ============================================
// ADD KEYFRAME ANIMATIONS
// ============================================

const style = document.createElement("style");

style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(400px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }

        to {
            opacity: 0;
            transform: translateX(400px);
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
        }

        to {
            opacity: 0;
        }
    }

    .modal-open {
        overflow: hidden;
    }
`;

document.head.appendChild(style);

// ============================================
// EXPOSE FUNCTIONS FOR HTML ONCLICK
// ============================================

window.searchStudents = searchStudents;
window.validateForm = validateForm;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showNotification = showNotification;
window.copyToClipboard = copyToClipboard;
window.smoothScroll = smoothScroll;
window.openModal = openModal;
window.closeModal = closeModal;
window.sortTable = sortTable;
window.filterPerformance = filterPerformance;
window.fetchAPI = fetchAPI;

// ============================================
// CONSOLE GREETING
// ============================================

console.log(
    "%cStudent Performance Predictor",
    "font-size: 20px; font-weight: bold; color: #667eea;"
);

console.log(
    "%cInteractive & Modern Interface Ready!",
    "font-size: 14px; color: #764ba2;"
);
















// ============================================
// STUDENT TABLE PAGINATION
// ============================================

const STUDENTS_PER_PAGE = 50;
let currentStudentPage = 1;

function initializePagination() {
    const table = document.getElementById("studentTable");

    if (!table) return;

    createPaginationControls();
    updateStudentPagination();
}

function createPaginationControls() {
    const table = document.getElementById("studentTable");

    if (!table) return;

    // Prevent duplicate pagination controls
    if (document.getElementById("studentPagination")) {
        return;
    }

    const pagination = document.createElement("div");

    pagination.id = "studentPagination";
    pagination.className = "student-pagination";

    pagination.innerHTML = `
        <button
            type="button"
            id="previousStudentPage"
            class="pagination-button"
        >
            Previous
        </button>

        <span
            id="studentPageInfo"
            class="pagination-info"
        >
            Page 1
        </span>

        <button
            type="button"
            id="nextStudentPage"
            class="pagination-button"
        >
            Next
        </button>
    `;

    table.parentNode.appendChild(pagination);

    const previousButton =
        document.getElementById(
            "previousStudentPage"
        );

    const nextButton =
        document.getElementById(
            "nextStudentPage"
        );

    previousButton.addEventListener(
        "click",
        function () {
            if (currentStudentPage > 1) {
                currentStudentPage--;

                updateStudentPagination();
            }
        }
    );

    nextButton.addEventListener(
        "click",
        function () {
            const totalPages =
                getStudentTotalPages();

            if (currentStudentPage < totalPages) {
                currentStudentPage++;

                updateStudentPagination();
            }
        }
    );
}

function getFilteredStudentRows() {
    const table =
        document.getElementById("studentTable");

    if (!table) return [];

    const rows = Array.from(
        table.querySelectorAll("tbody tr")
    );

    /*
     * A row is considered filtered out only when
     * filterPerformance() marks it as filtered.
     *
     * Pagination does NOT modify this value.
     */
    return rows.filter(
        (row) =>
            row.dataset.filteredOut !== "true"
    );
}

function getStudentTotalPages() {
    const filteredRows =
        getFilteredStudentRows();

    return Math.max(
        1,
        Math.ceil(
            filteredRows.length /
            STUDENTS_PER_PAGE
        )
    );
}

function updateStudentPagination() {
    const table =
        document.getElementById("studentTable");

    if (!table) return;

    const rows = Array.from(
        table.querySelectorAll("tbody tr")
    );

    // Only rows belonging to the current filter
    const filteredRows =
        rows.filter(
            (row) =>
                row.dataset.filteredOut !==
                "true"
        );

    const totalStudents =
        filteredRows.length;

    const totalPages = Math.max(
        1,
        Math.ceil(
            totalStudents /
            STUDENTS_PER_PAGE
        )
    );

    // Keep page number valid
    if (currentStudentPage > totalPages) {
        currentStudentPage = totalPages;
    }

    if (currentStudentPage < 1) {
        currentStudentPage = 1;
    }

    const startIndex =
        (currentStudentPage - 1) *
        STUDENTS_PER_PAGE;

    const endIndex =
        startIndex +
        STUDENTS_PER_PAGE;

    // Hide every row first
    rows.forEach((row) => {
        row.style.display = "none";
    });

    // Show only the current page
    filteredRows
        .slice(startIndex, endIndex)
        .forEach((row) => {
            row.style.display = "";
        });

    updatePaginationControls(
        totalStudents,
        totalPages,
        startIndex,
        endIndex
    );
}

function updatePaginationControls(
    totalStudents,
    totalPages,
    startIndex,
    endIndex
) {
    const pageInfo =
        document.getElementById(
            "studentPageInfo"
        );

    const previousButton =
        document.getElementById(
            "previousStudentPage"
        );

    const nextButton =
        document.getElementById(
            "nextStudentPage"
        );

    if (!pageInfo) return;

    if (totalStudents === 0) {
        pageInfo.textContent =
            "No students";

        if (previousButton) {
            previousButton.disabled = true;
        }

        if (nextButton) {
            nextButton.disabled = true;
        }

        return;
    }

    const displayedStart =
        startIndex + 1;

    const displayedEnd =
        Math.min(
            endIndex,
            totalStudents
        );

    pageInfo.textContent =
        `Showing ${displayedStart}-${displayedEnd} of ${totalStudents} — Page ${currentStudentPage} of ${totalPages}`;

    if (previousButton) {
        previousButton.disabled =
            currentStudentPage <= 1;
    }

    if (nextButton) {
        nextButton.disabled =
            currentStudentPage >= totalPages;
    }
}













// added code
/* =========================================================
   MOBILE NAVIGATION
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const menuButton = document.getElementById("menuButton");
    const sidebar = document.getElementById("sidebar");


    if (menuButton && sidebar) {

        menuButton.addEventListener("click", function () {

            sidebar.classList.toggle("active");

        });

    }

});


// added code