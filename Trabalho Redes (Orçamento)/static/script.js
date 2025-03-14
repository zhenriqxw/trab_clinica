document.addEventListener("DOMContentLoaded", function () {
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }

    document.querySelectorAll("a").forEach(link => {
        link.addEventListener("mouseenter", () => {
            link.style.transition = "0.3s";
            link.style.opacity = "0.7";
        });
        link.addEventListener("mouseleave", () => {
            link.style.opacity = "1";
        });
    });

    document.querySelectorAll("a.delete-link").forEach(deleteLink => {
        deleteLink.addEventListener("click", function (event) {
            event.preventDefault();
            showConfirmModal(function(confirmed) {
                if (confirmed) {
                    window.location.href = deleteLink.href;
                }
            });
        });
    });

    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function (event) {
            let valid = true;
            form.querySelectorAll("input[required]").forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.style.border = "2px solid red";
                } else {
                    input.style.border = "";
                }
            });
            if (!valid) {
                event.preventDefault();
                alert("Por favor, preencha todos os campos obrigatórios!");
            }
        });
    });

    let darkModeButton = document.createElement("button");
    darkModeButton.id = "darkModeToggle"; 
    darkModeButton.textContent = "Modo Escuro";
    darkModeButton.style.position = "fixed";
    darkModeButton.style.top = "10px";
    darkModeButton.style.right = "10px";
    darkModeButton.style.padding = "10px";
    darkModeButton.style.backgroundColor = "#333";
    darkModeButton.style.color = "#fff";
    darkModeButton.style.border = "none";
    darkModeButton.style.cursor = "pointer";
    darkModeButton.style.borderRadius = "5px";
    darkModeButton.style.transition = "background-color 0.3s";
    document.body.appendChild(darkModeButton);
    
    darkModeButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        const darkModeEnabled = document.body.classList.contains("dark-mode");
        localStorage.setItem("darkMode", darkModeEnabled ? "enabled" : "disabled");
        darkModeButton.textContent = darkModeEnabled ? "Modo Claro" : "Modo Escuro";
    });

    if (localStorage.getItem("darkMode") === "enabled") {
        darkModeButton.textContent = "Modo Claro";
    }
    
    let darkModeStyle = document.createElement("style");
    darkModeStyle.innerHTML = `
        .dark-mode {
            background-color: #181818;
            color: #e0e0e0;
        }
        .dark-mode a {
            color: #81a1c1;
        }
        .dark-mode a:hover {
            color: #a3b3c9;
        }
        .dark-mode table {
            background-color: #222;
            color: #e0e0e0;
        }
        .dark-mode th {
            background-color: #2c2c2c;
            color: #81a1c1;
        }
        .dark-mode td {
            background-color: #333;
        }
        .dark-mode .budget {
            background: #333;
            color: #e0e0e0;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        }
        .dark-mode input, .dark-mode button {
            background-color: #444;
            color: #e0e0e0;
            border: 1px solid #555;
        }
        .dark-mode input:focus, .dark-mode button:focus {
            border-color: #81a1c1;
        }
        .dark-mode button {
            background-color: #5a5a5a;
        }
        .dark-mode button:hover {
            background-color: #333;
        }
        .dark-mode table, .dark-mode th, .dark-mode td {
            border: 1px solid #ffffff;
        }
        .dark-mode tr:nth-child(even) {
            background-color: #444;
            transition: background-color 0.2s;
        }
        .dark-mode tr:hover {
            background-color: #555;
            transition: background-color 0.2s;
        }
    `;
    document.head.appendChild(darkModeStyle);

    function showConfirmModal(callback) {
        const modal = document.getElementById("confirmModal");
        modal.style.display = "flex";
        document.getElementById("confirmYes").onclick = function () {
            modal.style.display = "none";
            callback(true);
        };
        document.getElementById("confirmNo").onclick = function () {
            modal.style.display = "none";
            callback(false);
        };
    }
});


